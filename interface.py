"""Graphical version of the Wa-Tor simulation (pygame).
Version graphique de la simulation Wa-Tor (pygame).

EN: This file does NOT contain any simulation rule. It only calls the other files:
    - config.ini            : grid size, starting populations, emojis (read with configparser)
    - classes/grid.py       : Grid(...)  -> the ocean grid
    - classes/world.py      : World(...) -> world.move_entities() plays one turn,
                              world.fish_dict / world.shark_dict hold the living entities,
                              world.turn is the turn counter
    - classes/fish.py and classes/shark.py : entity.get_x(), entity.get_y(),
                              and shark.get_stamina() (the shark's energy)
    Everything else here is drawing (sea, emojis, animations, dashboard).

FR: Ce fichier ne contient AUCUNE règle de simulation. Il appelle seulement les autres fichiers :
    - config.ini            : taille de la grille, populations de départ, émojis (lu avec configparser)
    - classes/grid.py       : Grid(...)  -> la grille de l'océan
    - classes/world.py      : World(...) -> world.move_entities() joue un tour,
                              world.fish_dict / world.shark_dict contiennent les entités vivantes,
                              world.turn est le compteur de tours
    - classes/fish.py et classes/shark.py : entity.get_x(), entity.get_y(),
                              et shark.get_stamina() (l'énergie du requin)
    Tout le reste ici n'est que du dessin (mer, émojis, animations, tableau de bord).
"""
import configparser
import io
import math
import os
import random
import sys
from contextlib import redirect_stdout
from typing import Any, Callable, Optional

import pygame

from classes.grid import Grid
from classes.world import World

# --- CONFIGURATION (read from config.ini) ---
# EN: same file and same keys as main.py (console version).
# FR: même fichier et mêmes clés que main.py (version console).
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")


def load_config() -> configparser.ConfigParser:
    """Read config.ini (next to this file, or in the current folder).
    Lit config.ini (à côté de ce fichier, ou dans le dossier courant)."""
    config = configparser.ConfigParser()
    config.read([CONFIG_FILE, "config.ini"], encoding="utf-8")
    return config


config = load_config()
GRID_SIZE = config.getint("DEFAULT", "grid_size", fallback=30)
FISH_NUMBER = config.getint("DEFAULT", "population_init_fish", fallback=351)
SHARK_NUMBER = config.getint("DEFAULT", "population_init_shark", fallback=12)
STYLE_SEA = config.get("GRID", "style_sea", fallback="██")
STYLE_FISH = config.get("GRID", "style_fish", fallback="🐟")
STYLE_SHARK = config.get("GRID", "style_shark", fallback="🦈")

# --- GRAPHICAL SCREEN CONFIGURATION ---
# EN: the game area is about 750 px wide whatever the grid size (cells shrink when the grid grows).
# FR: la zone de jeu fait environ 750 px de large quelle que soit la grille (les cases rétrécissent).
CELL_SIZE = max(10, 750 // GRID_SIZE)
GAME_SIZE = GRID_SIZE * CELL_SIZE
DASHBOARD_HEIGHT = 160
WINDOW_WIDTH = GAME_SIZE
WINDOW_HEIGHT = GAME_SIZE + DASHBOARD_HEIGHT

# Modern Cinematic Interface Palette (UI Slate & Cyan)
COLOR_BG = (15, 23, 42)
COLOR_TEXT = (241, 245, 249)
COLOR_PAUSE_VEIL = (15, 23, 42, 180)
COLOR_PANEL = (30, 41, 59)
COLOR_BORDER = (71, 85, 105)

TARGET_FPS = 60
START_FULLSCREEN = False  # False = start in a normal window / False = démarrer en fenêtre
EMOJI_RATIO = 0.6  # emoji size relative to a cell / taille de l'émoji par rapport à une case
WAVE_LEVELS = range(-15, 16)  # integer wave amplitudes -> cached sea tiles / niveaux de vagues en cache


def quiet(func: Callable[..., Any], *args: Any) -> Any:
    """Call func(*args) without letting it print in the console.
    Appelle func(*args) sans laisser la fonction écrire dans la console.

    EN: World and Grid print the whole grid at every turn (console version); we hide it here.
    FR: World et Grid affichent toute la grille à chaque tour (version console) ; on la cache ici.
    """
    with redirect_stdout(io.StringIO()):
        return func(*args)


def launch_interface(external_grid: Optional[Grid] = None) -> None:
    """Open the window and run the simulation until the user quits.
    Ouvre la fenêtre et lance la simulation jusqu'à ce que l'utilisateur quitte."""
    pygame.init()

    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    if START_FULLSCREEN:
        flags |= pygame.FULLSCREEN
    try:
        # SCALED keeps the layout and stretches it to the screen (aspect ratio kept)
        # SCALED garde la mise en page et l'étire à l'écran (proportions conservées)
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags | pygame.SCALED, vsync=1)
    except Exception:
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)
    pygame.display.set_caption("Wa-Tor Standalone Ecosystem & Dashboard")
    clock = pygame.time.Clock()

    # Shark energy badge size follows the cell size / la pastille d'énergie suit la taille des cases
    badge = max(10, CELL_SIZE // 2)

    font_bold = pygame.font.SysFont("Segoe UI", 14, bold=True)
    font_value = pygame.font.SysFont("Consolas", 14, bold=False)
    font_energy = pygame.font.SysFont("Consolas", max(8, int(badge * 0.7)), bold=True)
    font_emoji = pygame.font.SysFont(["segoe ui emoji", "apple color emoji", "noto color emoji", "Arial"], int(CELL_SIZE * 0.65))
    pause_font = pygame.font.SysFont("Segoe UI", 24, bold=True)

    # ---------- PRE-RENDERED ASSETS (built once, blitted every frame) ----------
    # EN: Emojis are rescaled so the largest side equals EMOJI_RATIO of a cell.
    # FR: Les émojis sont redimensionnés pour que leur plus grand côté fasse EMOJI_RATIO d'une case.
    def make_emoji(char: str, color: tuple) -> pygame.Surface:
        surf = font_emoji.render(char, True, color).convert_alpha()
        target = int(CELL_SIZE * EMOJI_RATIO)
        w, h = surf.get_size()
        factor = target / max(w, h)
        return pygame.transform.smoothscale(surf, (max(1, int(w * factor)), max(1, int(h * factor))))

    # EN: the emojis come from config.ini (style_fish / style_shark), like in the console version.
    # FR: les émojis viennent de config.ini (style_fish / style_shark), comme en version console.
    fish_img = make_emoji(STYLE_FISH, (255, 255, 255))
    fish_shadow = make_emoji(STYLE_FISH, (218, 165, 32, 100))
    shark_img = make_emoji(STYLE_SHARK, (255, 255, 255))
    shark_shadow = make_emoji(STYLE_SHARK, (139, 0, 0, 100))

    # EN: Sea tiles: one surface per wave level instead of drawing GRID_SIZE² rounded rects per frame.
    # FR: Cases de mer : une surface par niveau de vague au lieu de dessiner GRID_SIZE² rectangles par image.
    sea_tiles = {}
    for lvl in WAVE_LEVELS:
        sea_blue = max(110, min(150, int(130 + lvl)))
        sea_green = max(130, min(170, int(150 + lvl * 0.5)))
        tile = pygame.Surface((CELL_SIZE - 1, CELL_SIZE - 1), pygame.SRCALPHA)
        pygame.draw.rect(tile, (14, sea_green, sea_blue), tile.get_rect(), border_radius=0)
        sea_tiles[lvl] = tile.convert_alpha()

    # EN: Shark energy badges, cached by energy value. FR: pastilles d'énergie, en cache par valeur.
    energy_cache = {}
    def get_energy_bubble(energy: int) -> pygame.Surface:
        bubble = energy_cache.get(energy)
        if bubble is None:
            bubble = pygame.Surface((badge, badge), pygame.SRCALPHA)
            pygame.draw.circle(bubble, (30, 41, 59), (badge // 2, badge // 2), badge // 2)
            color = (239, 68, 68) if energy <= 3 else (34, 197, 94)
            txt = font_energy.render(str(energy), True, color)
            bubble.blit(txt, txt.get_rect(center=(badge // 2, badge // 2)))
            bubble = bubble.convert_alpha()
            energy_cache[energy] = bubble
        return bubble

    # Pause veil + text / Voile de pause + texte
    veil = pygame.Surface((GAME_SIZE, GAME_SIZE), pygame.SRCALPHA)
    veil.fill(COLOR_PAUSE_VEIL)
    veil = veil.convert_alpha()
    pause_surface = pause_font.render("||  SIMULATION PAUSED", True, (252, 165, 165))
    pause_rect = pause_surface.get_rect(center=(GAME_SIZE // 2, GAME_SIZE // 2))

    # EN: Dashboard: static tiles/labels drawn once, only values re-rendered when they change.
    # FR: Tableau de bord : tuiles et titres dessinés une fois, seules les valeurs sont refaites.
    box_w = WINDOW_WIDTH // 4
    box_h = 60
    start_y = GAME_SIZE + 15
    label_texts = ["Chronons (Turns)", "Fish Population", "Shark Population", "Engine Velocity",
                   "Prey Density", "Predator Density", "Hardware Render", "Input Keybindings"]
    dashboard_bg = pygame.Surface((WINDOW_WIDTH, DASHBOARD_HEIGHT))
    dashboard_bg.fill(COLOR_BG)
    tile_positions = []
    for i, label in enumerate(label_texts):
        col = i % 4
        row = i // 4
        bx = col * box_w + 8
        by = start_y + row * box_h + 4
        tile_rect = pygame.Rect(bx, by, box_w - 16, box_h - 8)
        local_rect = tile_rect.move(0, -GAME_SIZE)
        pygame.draw.rect(dashboard_bg, COLOR_PANEL, local_rect, border_radius=6)
        pygame.draw.rect(dashboard_bg, COLOR_BORDER, local_rect, 1, border_radius=6)
        lbl = font_bold.render(label, True, (148, 163, 184))
        dashboard_bg.blit(lbl, (local_rect.x + 10, local_rect.y + 8))
        tile_positions.append((bx, by))
    dashboard_bg = dashboard_bg.convert()
    value_colors = [(147, 197, 253), (253, 224, 71), (248, 113, 113), (167, 139, 250),
                    (52, 211, 153), (251, 146, 60), (34, 211, 238), (148, 163, 184)]
    value_cache = {}
    def get_value_surface(index: int, text: str) -> pygame.Surface:
        key = (index, text)
        surf = value_cache.get(key)
        if surf is None:
            if len(value_cache) > 500:
                value_cache.clear()
            surf = font_value.render(text, True, value_colors[index])
            value_cache[key] = surf
        return surf

    # ---------- SIMULATION STATE ----------
    # EN: 1) Grid(...) from classes/grid.py, 2) World(...) from classes/world.py: it places the
    #     starting fish and sharks. The interface never moves anything itself.
    # FR: 1) Grid(...) de classes/grid.py, 2) World(...) de classes/world.py : il place les poissons
    #     et les requins de départ. L'interface ne déplace jamais rien elle-même.
    grid_instance = external_grid if external_grid is not None else Grid(GRID_SIZE, STYLE_SEA, STYLE_FISH, STYLE_SHARK)
    world = quiet(World, grid_instance, GRID_SIZE, FISH_NUMBER, SHARK_NUMBER)
    paused = False

    tick_count = 0
    logic_delay = 14  # frames between two turns / images entre deux tours
    wave_grid = [[random.uniform(0, 100) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # EN: Drawing only: where each entity was at the start of the turn (to glide smoothly), and
    #     which entities disappeared this turn (eaten fish, dead sharks) -> (is_fish, x, y).
    # FR: Dessin uniquement : où était chaque entité au début du tour (pour glisser en douceur), et
    #     quelles entités ont disparu ce tour (poissons mangés, requins morts) -> (is_fish, x, y).
    prev_pos = {}
    removed = []

    count_fish = len(world.fish_dict)
    count_shark = len(world.shark_dict)
    total_cells = GRID_SIZE * GRID_SIZE
    sin = math.sin

    running = True
    while running:
        current_fps = int(clock.get_fps())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    logic_delay = max(1, logic_delay - 2)
                elif event.key == pygame.K_DOWN:
                    logic_delay = min(60, logic_delay + 2)

        # ENGINE TICK / TOUR DE SIMULATION
        if not paused:
            tick_count += 1
            if tick_count >= logic_delay:
                tick_count = 0

                # EN: remember positions before the turn, using the entities' own get_x()/get_y().
                # FR: on mémorise les positions avant le tour, avec les get_x()/get_y() des entités.
                fish_before = list(world.fish_dict.values())
                sharks_before = list(world.shark_dict.values())
                prev_pos = {id(e): (e.get_x(), e.get_y()) for e in fish_before + sharks_before}

                # EN: ONE turn of the simulation, exactly like main.py does:
                #     world.turn += 1 then world.move_entities().
                # FR: UN tour de simulation, exactement comme main.py :
                #     world.turn += 1 puis world.move_entities().
                world.turn += 1
                quiet(world.move_entities)

                # EN: entities that are gone after the turn (eaten or starved).
                # FR: entités qui ont disparu après le tour (mangées ou mortes de faim).
                alive = {id(e) for e in world.fish_dict.values()} | {id(e) for e in world.shark_dict.values()}
                removed = [(True, *prev_pos[id(e)]) for e in fish_before if id(e) not in alive]
                removed += [(False, *prev_pos[id(e)]) for e in sharks_before if id(e) not in alive]

                # EN: populations = size of World's dictionaries. FR: populations = taille des dictionnaires de World.
                count_fish = len(world.fish_dict)
                count_shark = len(world.shark_dict)

        fish_percent = (count_fish / total_cells) * 100
        shark_percent = (count_shark / total_cells) * 100

        # --- DRAW VISUAL CANVAS FRAME / DESSIN DE L'IMAGE ---
        # EN: Animation progress inside the current turn (0 -> 1), frozen while paused.
        # FR: Avancement de l'animation dans le tour (0 -> 1), figé pendant la pause.
        anim_p = min(1.0, (tick_count + 1) / logic_delay)

        time_ms = pygame.time.get_ticks() * 0.003
        for y in range(GRID_SIZE):
            wave_row = wave_grid[y]
            py = y * CELL_SIZE
            for x in range(GRID_SIZE):
                lvl = int(sin(time_ms + wave_row[x]) * 15)
                screen.blit(sea_tiles[lvl], (x * CELL_SIZE, py))

        half = GRID_SIZE / 2

        def interp(prev: float, cur: float) -> float:
            # EN: shortest path on the wrapping (toroidal) grid. FR: plus court chemin sur la grille torique.
            d = cur - prev
            if d > half:
                d -= GRID_SIZE
            elif d < -half:
                d += GRID_SIZE
            return (prev + d * anim_p) % GRID_SIZE

        def origins(gx: float, gy: float) -> list:
            # EN: pixel origin(s) of a sprite; drawn twice while crossing the screen edge.
            # FR: origine(s) en pixels d'un sprite ; dessiné deux fois quand il traverse un bord.
            ox = gx * CELL_SIZE
            oy = gy * CELL_SIZE
            xs = (ox, ox - GAME_SIZE) if ox > GAME_SIZE - CELL_SIZE else (ox,)
            ys = (oy, oy - GAME_SIZE) if oy > GAME_SIZE - CELL_SIZE else (oy,)
            return [(ax, ay) for ax in xs for ay in ys]

        center = (CELL_SIZE - 1) // 2

        # EN: Entities eaten / starved this turn fade out where they were.
        # FR: Les entités mangées / mortes ce tour disparaissent en fondu là où elles étaient.
        fade = int(255 * (1.0 - anim_p))
        if fade > 0:
            for is_fish, rx, ry in removed:
                img = fish_img if is_fish else shark_img
                shd = fish_shadow if is_fish else shark_shadow
                img.set_alpha(fade)
                shd.set_alpha(fade)
                for ax, ay in origins(rx, ry):
                    screen.blit(shd, shd.get_rect(center=(ax + center + 2, ay + center + 2)))
                    screen.blit(img, img.get_rect(center=(ax + center, ay + center)))
                img.set_alpha(255)
                shd.set_alpha(255)

        # EN: Living entities, read from World's dictionaries (fish first, sharks drawn on top),
        #     gliding from their previous cell to the current one.
        # FR: Entités vivantes, lues dans les dictionnaires de World (poissons d'abord, requins par-dessus),
        #     qui glissent de leur case précédente à la case actuelle.
        living = [(e, True) for e in world.fish_dict.values()]
        living += [(e, False) for e in world.shark_dict.values()]
        for ent, is_fish in living:
            cur_x, cur_y = ent.get_x(), ent.get_y()
            prev_x, prev_y = prev_pos.get(id(ent), (cur_x, cur_y))  # newborn: no previous cell / nouveau-né : pas de case précédente
            gx = interp(prev_x, cur_x)
            gy = interp(prev_y, cur_y)
            img = fish_img if is_fish else shark_img
            shd = fish_shadow if is_fish else shark_shadow
            # EN: the shark's energy comes from shark.get_stamina(). FR: l'énergie vient de shark.get_stamina().
            bubble = None if is_fish else get_energy_bubble(ent.get_stamina())
            for ax, ay in origins(gx, gy):
                screen.blit(shd, shd.get_rect(center=(ax + center + 2, ay + center + 2)))
                screen.blit(img, img.get_rect(center=(ax + center, ay + center)))
                if bubble is not None:
                    screen.blit(bubble, (ax + CELL_SIZE - badge, ay + CELL_SIZE - badge))

        if paused:
            screen.blit(veil, (0, 0))
            screen.blit(pause_surface, pause_rect)

        # --- DASHBOARD / TABLEAU DE BORD ---
        screen.blit(dashboard_bg, (0, GAME_SIZE))
        values = [
            f"{world.turn:05d}",
            f"{count_fish:03d} ({STYLE_FISH})",
            f"{count_shark:03d} ({STYLE_SHARK})",
            f"{60//logic_delay} step/s",
            f"{fish_percent:.1f} %",
            f"{shark_percent:.1f} %",
            f"{current_fps} FPS",
            "SPACE | UP/DOWN",
        ]
        for i, text in enumerate(values):
            bx, by = tile_positions[i]
            screen.blit(get_value_surface(i, text), (bx + 10, by + 26))

        pygame.display.flip()
        clock.tick(TARGET_FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    launch_interface()