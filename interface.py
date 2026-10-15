# interface.py
"""
EN: Graphical (pygame) version of the Wa-Tor simulation.
    This file does NOT contain the simulation rules: they live in classes/world.py.
    Here we only (1) read config.ini, (2) call World / Grid, and (3) draw the result
    with smooth animations and a dashboard.

FR: Version graphique (pygame) de la simulation Wa-Tor.
    Ce fichier ne contient PAS les règles de la simulation : elles sont dans classes/world.py.
    Ici on fait seulement (1) lire config.ini, (2) appeler World / Grid, et (3) dessiner
    le résultat avec des animations fluides et un tableau de bord.

Controls / Commandes :
    SPACE  : pause / resume            | pause / reprise
    UP     : faster simulation         | simulation plus rapide
    DOWN   : slower simulation         | simulation plus lente
    F11    : toggle fullscreen         | plein écran on/off
    ESC    : quit                      | quitter
"""

# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------
import configparser  # EN: read the config.ini file | FR: lire le fichier config.ini
import io  # EN: in-memory text buffer used to silence prints | FR: tampon texte en mémoire pour masquer les print
import math  # EN: sine function for the sea waves | FR: fonction sinus pour les vagues
import os  # EN: build the path to config.ini | FR: construire le chemin vers config.ini
import random  # EN: random starting phase of each wave | FR: phase de départ aléatoire de chaque vague
import sys  # EN: exit the program cleanly | FR: quitter proprement le programme
from contextlib import redirect_stdout  # EN: temporarily redirect print() | FR: rediriger temporairement print()
from typing import Any, Callable, Optional  # EN: type annotations | FR: annotations de type

import pygame  # EN: window, drawing, events, fonts | FR: fenêtre, dessin, événements, polices

from classes.grid import Grid  # EN: the grid (cells + styles) | FR: la grille (cases + styles)
from classes.world import World  # EN: the simulation engine | FR: le moteur de simulation

# ---------------------------------------------------------------------------
# CONFIG (read from config.ini) / LECTURE DE config.ini
# ---------------------------------------------------------------------------
# EN: absolute path of config.ini, located next to this file
# FR: chemin absolu de config.ini, placé à côté de ce fichier
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
config = configparser.ConfigParser()

# EN: look next to this file first, then in the current folder; utf-8 is needed for the emojis
# FR: cherche d'abord à côté du fichier, puis dans le dossier courant ; utf-8 est nécessaire pour les emojis
if not config.read([CONFIG_PATH, "config.ini"], encoding="utf-8"):
    raise FileNotFoundError("config.ini introuvable / not found (put it next to interface.py)")

# EN: values read from config.ini | FR: valeurs lues dans config.ini
GRID_SIZE = config.getint("DEFAULT", "grid_size")  # EN: cells per side | FR: cases par côté
FISH_INIT = config.getint("DEFAULT", "population_init_fish")  # EN: starting fish | FR: poissons au départ
SHARK_INIT = config.getint("DEFAULT", "population_init_shark")  # EN: starting sharks | FR: requins au départ
SEA_STYLE = config.get("GRID", "style_sea")  # EN: sea symbol (console) | FR: symbole de la mer (console)
FISH_EMOJI = config.get("GRID", "style_fish")  # EN: fish emoji | FR: emoji du poisson
SHARK_EMOJI = config.get("GRID", "style_shark")  # EN: shark emoji | FR: emoji du requin

# ---------------------------------------------------------------------------
# GRAPHICAL SCREEN CONFIGURATION / CONFIGURATION DE L'ÉCRAN
# ---------------------------------------------------------------------------
# EN: the game area stays about 750 px wide whatever grid_size is: cells shrink when the grid grows
# FR: la zone de jeu reste d'environ 750 px quelle que soit grid_size : les cases rétrécissent
CELL_SIZE = max(10, min(50, 750 // GRID_SIZE))  # EN: size of one cell in px | FR: taille d'une case en px
GAME_SIZE = GRID_SIZE * CELL_SIZE  # EN: width/height of the game area | FR: largeur/hauteur de la zone de jeu
DASHBOARD_HEIGHT = 160  # EN: height of the bottom panel | FR: hauteur du panneau du bas
WINDOW_WIDTH = max(GAME_SIZE, 750)  # EN: keep room for the 4 dashboard columns | FR: garder la place des 4 colonnes
WINDOW_HEIGHT = GAME_SIZE + DASHBOARD_HEIGHT  # EN: game area + dashboard | FR: zone de jeu + tableau de bord

# EN: colour palette (RGB, or RGBA when there is a 4th value = transparency)
# FR: palette de couleurs (RVB, ou RVBA quand il y a une 4e valeur = transparence)
COLOR_BG = (15, 23, 42)  # EN: dashboard background | FR: fond du tableau de bord
COLOR_TEXT = (241, 245, 249)  # EN: main text | FR: texte principal
COLOR_PAUSE_VEIL = (15, 23, 42, 180)  # EN: semi-transparent veil when paused | FR: voile semi-transparent en pause
COLOR_PANEL = (30, 41, 59)  # EN: dashboard tiles | FR: tuiles du tableau de bord
COLOR_BORDER = (71, 85, 105)  # EN: tile borders | FR: bordures des tuiles

# ---------------------------------------------------------------------------
# ENGINE SETTINGS / RÉGLAGES DU MOTEUR
# ---------------------------------------------------------------------------
TARGET_FPS = 60  # EN: frames drawn per second | FR: images dessinées par seconde
START_FULLSCREEN = False  # EN: False = start in a normal window | FR: False = démarrer en fenêtre normale
EMOJI_RATIO = 0.6  # EN: emoji size relative to a cell (0.6 = 60%) | FR: taille de l'emoji par rapport à la case
WAVE_LEVELS = range(-15, 16)  # EN: wave amplitudes -> cached sea tiles | FR: amplitudes des vagues -> tuiles en cache

# EN: shark energy bubble, scaled with the cell size
# FR: bulle d'énergie du requin, adaptée à la taille des cases
BUBBLE_SIZE = max(10, int(CELL_SIZE * 0.32))
ENERGY_FONT_SIZE = max(8, int(CELL_SIZE * 0.22))


def quiet(func: Callable[..., Any], *args: Any) -> Any:
    """
    EN: Call `func(*args)` while hiding everything it prints, and return its result.
        World and Grid print the grid in the console at every turn; in the graphical
        version we do not want that.
    FR: Appelle `func(*args)` en masquant tout ce qu'elle affiche, et renvoie son résultat.
        World et Grid affichent la grille dans la console à chaque tour ; dans la
        version graphique on ne le veut pas.
    """
    # EN: send print() to a throw-away buffer during the call | FR: envoie print() dans un tampon jetable pendant l'appel
    with redirect_stdout(io.StringIO()):
        return func(*args)


def launch_interface(external_grid: Optional[Grid] = None) -> None:
    """
    EN: Open the pygame window and run the simulation until the user quits.
        Steps: 1) create the window and fonts, 2) pre-render images,
        3) build the dashboard, 4) create the World, 5) main loop
        (events -> simulation turn -> drawing -> dashboard).
    FR: Ouvre la fenêtre pygame et lance la simulation jusqu'à ce que l'utilisateur quitte.
        Étapes : 1) créer la fenêtre et les polices, 2) pré-dessiner les images,
        3) construire le tableau de bord, 4) créer le World, 5) boucle principale
        (événements -> tour de simulation -> dessin -> tableau de bord).

    Args:
        external_grid:
            EN: optional existing Grid to use; if None, a new one is created from config.ini.
            FR: Grid existante optionnelle ; si None, une nouvelle est créée depuis config.ini.
    """
    # ======================================================================
    # STEP 1 - WINDOW AND FONTS / ÉTAPE 1 - FENÊTRE ET POLICES
    # ======================================================================
    pygame.init()  # EN: start all pygame modules | FR: démarre tous les modules pygame

    # EN: HWSURFACE + DOUBLEBUF = hardware drawing with double buffering (smoother)
    # FR: HWSURFACE + DOUBLEBUF = dessin matériel avec double tampon (plus fluide)
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    if START_FULLSCREEN:
        flags |= pygame.FULLSCREEN
    try:
        # EN: SCALED keeps the layout and stretches it to the screen (aspect ratio kept)
        # FR: SCALED garde la mise en page et l'étire à l'écran (proportions conservées)
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags | pygame.SCALED, vsync=1)
    except Exception:
        # EN: fallback if SCALED / vsync is not supported | FR: solution de secours si SCALED / vsync n'est pas supporté
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)
    pygame.display.set_caption("Wa-Tor Standalone Ecosystem & Dashboard")
    clock = pygame.time.Clock()  # EN: used to limit and measure FPS | FR: sert à limiter et mesurer les FPS

    # EN: fonts (the first available name in the list is used)
    # FR: polices (le premier nom disponible dans la liste est utilisé)
    font_bold = pygame.font.SysFont("Segoe UI", 14, bold=True)  # EN: dashboard labels | FR: titres du tableau de bord
    font_value = pygame.font.SysFont("Consolas", 14, bold=False)  # EN: dashboard values | FR: valeurs du tableau de bord
    font_energy = pygame.font.SysFont("Consolas", ENERGY_FONT_SIZE, bold=True)  # EN: shark energy number | FR: énergie du requin
    font_emoji = pygame.font.SysFont(
        ["segoe ui emoji", "apple color emoji", "noto color emoji", "Arial"], int(CELL_SIZE * 0.65)
    )  # EN: emoji rendering | FR: rendu des emojis
    pause_font = pygame.font.SysFont("Segoe UI", 24, bold=True)  # EN: pause text | FR: texte de pause

    # ======================================================================
    # STEP 2 - PRE-RENDERED ASSETS / ÉTAPE 2 - IMAGES PRÉ-DESSINÉES
    # (built once, blitted every frame / créées une fois, collées à chaque image)
    # ======================================================================
    def make_emoji(char: str, color: tuple) -> pygame.Surface:
        """
        EN: Render an emoji as an image whose largest side equals EMOJI_RATIO of a cell
            (lower EMOJI_RATIO = smaller emojis).
        FR: Dessine un emoji sous forme d'image dont le plus grand côté vaut EMOJI_RATIO d'une case
            (EMOJI_RATIO plus petit = emojis plus petits).
        """
        surf = font_emoji.render(char, True, color).convert_alpha()  # EN: text -> image | FR: texte -> image
        target = int(CELL_SIZE * EMOJI_RATIO)  # EN: wanted size in px | FR: taille voulue en px
        w, h = surf.get_size()
        factor = target / max(w, h)  # EN: scale factor | FR: facteur d'échelle
        return pygame.transform.smoothscale(surf, (max(1, int(w * factor)), max(1, int(h * factor))))

    # EN: emojis come from config.ini; the "shadow" version is a dark, transparent copy drawn behind
    # FR: les emojis viennent de config.ini ; la version "shadow" est une copie sombre et transparente dessinée derrière
    fish_img = make_emoji(FISH_EMOJI, (255, 255, 255))
    fish_shadow = make_emoji(FISH_EMOJI, (218, 165, 32, 100))
    shark_img = make_emoji(SHARK_EMOJI, (255, 255, 255))
    shark_shadow = make_emoji(SHARK_EMOJI, (139, 0, 0, 100))

    # EN: sea tiles: one image per wave level, instead of drawing one rounded rectangle per cell per frame
    # FR: tuiles de mer : une image par niveau de vague, au lieu de dessiner un rectangle arrondi par case à chaque image
    sea_tiles = {}
    for lvl in WAVE_LEVELS:
        sea_blue = max(110, min(150, int(130 + lvl)))  # EN: blue varies with the wave | FR: le bleu varie avec la vague
        sea_green = max(130, min(170, int(150 + lvl * 0.5)))  # EN: green varies a bit | FR: le vert varie un peu
        tile = pygame.Surface((CELL_SIZE - 1, CELL_SIZE - 1), pygame.SRCALPHA)  # EN: -1 leaves a thin gap | FR: -1 laisse un fin espace
        pygame.draw.rect(tile, (14, sea_green, sea_blue), tile.get_rect(), border_radius=4)
        sea_tiles[lvl] = tile.convert_alpha()

    # EN: shark energy bubbles, cached by energy value so they are drawn only once per value
    # FR: bulles d'énergie des requins, mises en cache par valeur d'énergie pour n'être dessinées qu'une fois
    energy_cache = {}

    def get_energy_bubble(energy: int) -> pygame.Surface:
        """
        EN: Return the small round badge showing a shark's energy
            (red if energy <= 3, green otherwise).
        FR: Renvoie le petit badge rond affichant l'énergie d'un requin
            (rouge si énergie <= 3, vert sinon).
        """
        key = energy
        bubble = energy_cache.get(key)  # EN: already built? | FR: déjà créée ?
        if bubble is None:
            half_b = BUBBLE_SIZE // 2
            bubble = pygame.Surface((BUBBLE_SIZE, BUBBLE_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(bubble, (30, 41, 59), (half_b, half_b), half_b)  # EN: dark disc | FR: disque sombre
            color = (239, 68, 68) if energy <= 3 else (34, 197, 94)  # EN: red = danger | FR: rouge = danger
            txt = font_energy.render(str(energy), True, color)
            bubble.blit(txt, txt.get_rect(center=(half_b, half_b)))  # EN: number centred | FR: nombre centré
            bubble = bubble.convert_alpha()
            energy_cache[key] = bubble
        return bubble

    # EN: pause veil (dark layer over the game) + "paused" text
    # FR: voile de pause (couche sombre sur le jeu) + texte "pause"
    veil = pygame.Surface((GAME_SIZE, GAME_SIZE), pygame.SRCALPHA)
    veil.fill(COLOR_PAUSE_VEIL)
    veil = veil.convert_alpha()
    pause_surface = pause_font.render("||  SIMULATION PAUSED", True, (252, 165, 165))
    pause_rect = pause_surface.get_rect(center=(GAME_SIZE // 2, GAME_SIZE // 2))

    # ======================================================================
    # STEP 3 - DASHBOARD / ÉTAPE 3 - TABLEAU DE BORD
    # EN: static tiles and labels are drawn once; only the values are re-rendered
    # FR: les tuiles et titres statiques sont dessinés une fois ; seules les valeurs sont redessinées
    # ======================================================================
    box_w = WINDOW_WIDTH // 4  # EN: 4 columns | FR: 4 colonnes
    box_h = 60  # EN: height of a row | FR: hauteur d'une ligne
    start_y = GAME_SIZE + 15  # EN: first row, just under the game area | FR: première ligne, juste sous le jeu
    label_texts = ["Chronons (Turns)", "Fish Population", "Shark Population", "Engine Velocity",
                   "Prey Density", "Predator Density", "Hardware Render", "Input Keybindings"]
    dashboard_bg = pygame.Surface((WINDOW_WIDTH, DASHBOARD_HEIGHT))
    dashboard_bg.fill(COLOR_BG)
    tile_positions = []  # EN: (x, y) of each tile on screen | FR: (x, y) de chaque tuile à l'écran
    for i, label in enumerate(label_texts):
        col = i % 4  # EN: column index | FR: numéro de colonne
        row = i // 4  # EN: row index | FR: numéro de ligne
        bx = col * box_w + 8
        by = start_y + row * box_h + 4
        tile_rect = pygame.Rect(bx, by, box_w - 16, box_h - 8)
        local_rect = tile_rect.move(0, -GAME_SIZE)  # EN: position inside dashboard_bg | FR: position dans dashboard_bg
        pygame.draw.rect(dashboard_bg, COLOR_PANEL, local_rect, border_radius=6)  # EN: tile | FR: tuile
        pygame.draw.rect(dashboard_bg, COLOR_BORDER, local_rect, 1, border_radius=6)  # EN: border | FR: bordure
        lbl = font_bold.render(label, True, (148, 163, 184))
        dashboard_bg.blit(lbl, (local_rect.x + 10, local_rect.y + 8))
        tile_positions.append((bx, by))
    dashboard_bg = dashboard_bg.convert()

    # EN: one colour per dashboard value | FR: une couleur par valeur du tableau de bord
    value_colors = [(147, 197, 253), (253, 224, 71), (248, 113, 113), (167, 139, 250),
                    (52, 211, 153), (251, 146, 60), (34, 211, 238), (148, 163, 184)]
    value_cache = {}  # EN: (tile index, text) -> image | FR: (numéro de tuile, texte) -> image

    def get_value_surface(index: int, text: str) -> pygame.Surface:
        """
        EN: Return the image of a dashboard value, rendering it only if the text is new
            (cache cleared when it grows past 500 entries).
        FR: Renvoie l'image d'une valeur du tableau de bord, en ne la dessinant que si le texte est nouveau
            (cache vidé s'il dépasse 500 entrées).
        """
        key = (index, text)
        surf = value_cache.get(key)
        if surf is None:
            if len(value_cache) > 500:
                value_cache.clear()
            surf = font_value.render(text, True, value_colors[index])
            value_cache[key] = surf
        return surf

    # ======================================================================
    # STEP 4 - SIMULATION STATE / ÉTAPE 4 - ÉTAT DE LA SIMULATION
    # EN: the simulation itself lives in classes/world.py: the interface only calls and draws it
    # FR: la simulation vit dans classes/world.py : l'interface ne fait que l'appeler et la dessiner
    # ======================================================================
    grid_instance = external_grid if external_grid is not None else Grid(GRID_SIZE, SEA_STYLE, FISH_EMOJI, SHARK_EMOJI)
    world = quiet(World, grid_instance, GRID_SIZE, FISH_INIT, SHARK_INIT)  # EN: places the starting fish/sharks | FR: place les poissons/requins de départ
    paused = False

    tick_count = 0  # EN: frames since the last simulation turn | FR: images depuis le dernier tour de simulation
    logic_delay = 14  # EN: frames per turn (smaller = faster) | FR: images par tour (plus petit = plus rapide)
    # EN: random wave phase per cell so the sea does not move in sync | FR: phase de vague aléatoire par case pour que la mer ne bouge pas en bloc
    wave_grid = [[random.uniform(0, 100) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # EN: for the smooth animation (drawing only): where each entity was at the start of the turn,
    #     and which entities disappeared this turn (eaten fish, dead sharks) -> (is_fish, x, y)
    # FR: pour l'animation fluide (dessin uniquement) : où se trouvait chaque entité au début du tour,
    #     et quelles entités ont disparu ce tour (poissons mangés, requins morts) -> (is_fish, x, y)
    prev_pos = {}
    removed = []

    count_fish = len(world.fish_dict)  # EN: current fish count | FR: nombre actuel de poissons
    count_shark = len(world.shark_dict)  # EN: current shark count | FR: nombre actuel de requins
    total_cells = GRID_SIZE * GRID_SIZE
    sin = math.sin  # EN: local alias = a bit faster in the loop | FR: alias local = un peu plus rapide dans la boucle

    # ======================================================================
    # STEP 5 - MAIN LOOP / ÉTAPE 5 - BOUCLE PRINCIPALE
    # ======================================================================
    running = True
    while running:
        current_fps = int(clock.get_fps())  # EN: measured FPS | FR: FPS mesurés

        # ---- 5.1 EVENTS (keyboard, window) / ÉVÉNEMENTS (clavier, fenêtre) ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # EN: window closed | FR: fenêtre fermée
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # EN: pause / resume | FR: pause / reprise
                    paused = not paused
                elif event.key == pygame.K_F11:  # EN: fullscreen | FR: plein écran
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:  # EN: quit | FR: quitter
                    running = False
                elif event.key == pygame.K_UP:  # EN: faster | FR: plus rapide
                    logic_delay = max(1, logic_delay - 2)
                elif event.key == pygame.K_DOWN:  # EN: slower | FR: plus lent
                    logic_delay = min(60, logic_delay + 2)

        # ---- 5.2 SIMULATION TURN / TOUR DE SIMULATION ----
        if not paused:
            tick_count += 1
            if tick_count >= logic_delay:  # EN: time for a new turn | FR: c'est l'heure d'un nouveau tour
                tick_count = 0

                # EN: remember positions before the turn (for the animation)
                # FR: mémorise les positions avant le tour (pour l'animation)
                fish_before = list(world.fish_dict.values())
                sharks_before = list(world.shark_dict.values())
                prev_pos = {id(e): (e.x, e.y) for e in fish_before + sharks_before}

                # EN: one turn of the simulation, played by World
                # FR: un tour de simulation, joué par World
                world.turn += 1
                quiet(world.move_entities)

                # EN: entities that are gone after the turn (not in the dictionaries any more)
                # FR: entités disparues après le tour (plus présentes dans les dictionnaires)
                alive = {id(e) for e in world.fish_dict.values()} | {id(e) for e in world.shark_dict.values()}
                removed = [(True, *prev_pos[id(e)]) for e in fish_before if id(e) not in alive]
                removed += [(False, *prev_pos[id(e)]) for e in sharks_before if id(e) not in alive]

                count_fish = len(world.fish_dict)
                count_shark = len(world.shark_dict)

        # EN: densities = share of cells occupied | FR: densités = part de cases occupées
        fish_percent = (count_fish / total_cells) * 100
        shark_percent = (count_shark / total_cells) * 100

        # ---- 5.3 DRAWING / DESSIN ----
        # EN: animation progress inside the current turn (0 -> 1), frozen while paused
        # FR: progression de l'animation dans le tour en cours (0 -> 1), figée en pause
        anim_p = min(1.0, (tick_count + 1) / logic_delay)

        # EN: sea background: each cell picks a wave level from a sine wave
        # FR: fond de mer : chaque case choisit un niveau de vague avec un sinus
        time_ms = pygame.time.get_ticks() * 0.003
        for y in range(GRID_SIZE):
            wave_row = wave_grid[y]
            py = y * CELL_SIZE
            for x in range(GRID_SIZE):
                lvl = int(sin(time_ms + wave_row[x]) * 15)
                screen.blit(sea_tiles[lvl], (x * CELL_SIZE, py))

        half = GRID_SIZE / 2

        def interp(prev: float, cur: float) -> float:
            """
            EN: Position between `prev` and `cur` according to anim_p, taking the shortest
                path on the wrapping (toroidal) grid.
            FR: Position entre `prev` et `cur` selon anim_p, en prenant le chemin le plus court
                sur la grille qui boucle (torique).
            """
            d = cur - prev
            if d > half:  # EN: shorter to go around the edge | FR: plus court de passer par le bord
                d -= GRID_SIZE
            elif d < -half:
                d += GRID_SIZE
            return (prev + d * anim_p) % GRID_SIZE

        def origins(gx: float, gy: float) -> list:
            """
            EN: Pixel origin(s) of a sprite. Returns two (or four) positions while the sprite
                crosses the screen edge, so it appears on both sides.
            FR: Origine(s) en pixels d'un sprite. Renvoie deux (ou quatre) positions quand le sprite
                traverse le bord de l'écran, pour qu'il apparaisse des deux côtés.
            """
            ox = gx * CELL_SIZE
            oy = gy * CELL_SIZE
            xs = (ox, ox - GAME_SIZE) if ox > GAME_SIZE - CELL_SIZE else (ox,)
            ys = (oy, oy - GAME_SIZE) if oy > GAME_SIZE - CELL_SIZE else (oy,)
            return [(ax, ay) for ax in xs for ay in ys]

        center = (CELL_SIZE - 1) // 2  # EN: centre of a cell in px | FR: centre d'une case en px

        # EN: entities eaten / starved this turn fade out where they were
        # FR: les entités mangées / mortes de faim ce tour s'effacent là où elles étaient
        fade = int(255 * (1.0 - anim_p))
        if fade > 0:
            for is_fish, rx, ry in removed:
                img = fish_img if is_fish else shark_img
                shd = fish_shadow if is_fish else shark_shadow
                img.set_alpha(fade)  # EN: transparency | FR: transparence
                shd.set_alpha(fade)
                for ax, ay in origins(rx, ry):
                    screen.blit(shd, shd.get_rect(center=(ax + center + 2, ay + center + 2)))  # EN: shadow offset by 2 px | FR: ombre décalée de 2 px
                    screen.blit(img, img.get_rect(center=(ax + center, ay + center)))
                img.set_alpha(255)  # EN: restore full opacity | FR: rétablit l'opacité complète
                shd.set_alpha(255)

        # EN: living entities (read from World), gliding from their previous cell to the current one
        # FR: entités vivantes (lues dans World), glissant de leur case précédente à la case actuelle
        living = [(e, True) for e in world.fish_dict.values()]
        living += [(e, False) for e in world.shark_dict.values()]
        for ent, is_fish in living:
            prev_x, prev_y = prev_pos.get(id(ent), (ent.x, ent.y))  # EN: new-born = no previous position | FR: nouveau-né = pas de position précédente
            gx = interp(prev_x, ent.x)
            gy = interp(prev_y, ent.y)
            img = fish_img if is_fish else shark_img
            shd = fish_shadow if is_fish else shark_shadow
            bubble = None if is_fish else get_energy_bubble(ent.get_stamina())  # EN: only sharks have energy | FR: seuls les requins ont de l'énergie
            for ax, ay in origins(gx, gy):
                screen.blit(shd, shd.get_rect(center=(ax + center + 2, ay + center + 2)))
                screen.blit(img, img.get_rect(center=(ax + center, ay + center)))
                if bubble is not None:
                    screen.blit(bubble, (ax + CELL_SIZE - BUBBLE_SIZE - 4, ay + CELL_SIZE - BUBBLE_SIZE - 4))

        # EN: pause veil and text on top of everything | FR: voile et texte de pause par-dessus tout
        if paused:
            screen.blit(veil, (0, 0))
            screen.blit(pause_surface, pause_rect)

        # ---- 5.4 DASHBOARD / TABLEAU DE BORD ----
        screen.blit(dashboard_bg, (0, GAME_SIZE))  # EN: static background | FR: fond statique
        values = [
            f"{world.turn:05d}",  # EN: turn number | FR: numéro du tour
            f"{count_fish:03d} ({FISH_EMOJI})",  # EN: fish count | FR: nombre de poissons
            f"{count_shark:03d} ({SHARK_EMOJI})",  # EN: shark count | FR: nombre de requins
            f"{60//logic_delay} step/s",  # EN: turns per second | FR: tours par seconde
            f"{fish_percent:.1f} %",  # EN: fish density | FR: densité de poissons
            f"{shark_percent:.1f} %",  # EN: shark density | FR: densité de requins
            f"{current_fps} FPS",  # EN: frames per second | FR: images par seconde
            "SPACE | UP/DOWN",  # EN: reminder of the keys | FR: rappel des touches
        ]
        for i, text in enumerate(values):
            bx, by = tile_positions[i]
            screen.blit(get_value_surface(i, text), (bx + 10, by + 26))

        # ---- 5.5 END OF FRAME / FIN DE L'IMAGE ----
        pygame.display.flip()  # EN: show the finished frame | FR: affiche l'image terminée
        clock.tick(TARGET_FPS)  # EN: wait to hold TARGET_FPS | FR: attend pour tenir TARGET_FPS

    # EN: clean exit when the loop stops | FR: sortie propre quand la boucle s'arrête
    pygame.quit()
    sys.exit()


# EN: run the graphical version only when this file is executed directly (python interface.py)
# FR: lance la version graphique seulement quand ce fichier est exécuté directement (python interface.py)
if __name__ == "__main__":
    launch_interface()