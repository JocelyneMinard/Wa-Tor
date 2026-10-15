# interface.py
import io
import math
import random
import sys
from contextlib import redirect_stdout

import pygame

from classes.grid import Grid
from classes.world import World

# --- GRAPHICAL SCREEN CONFIGURATION ---
CELL_SIZE = 50
GRID_SIZE = 15
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

# --- MAIN ENGINE CONTROL LOOP ---

TARGET_FPS = 60
START_FULLSCREEN = False  # False = start in a normal window
EMOJI_RATIO = 0.6  # emoji size relative to a cell (0.6 = 60%)
WAVE_LEVELS = range(-15, 16)  # integer wave amplitudes -> cached sea tiles


def quiet(func, *args):
    # World and Grid print the grid in the console at every turn:
    # we silence that output in the graphical version
    with redirect_stdout(io.StringIO()):
        return func(*args)


def launch_interface(external_grid=None):
    pygame.init()

    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    if START_FULLSCREEN:
        flags |= pygame.FULLSCREEN
    try:
        # SCALED keeps the 750x910 layout and stretches it to the screen (aspect ratio kept)
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags | pygame.SCALED, vsync=1)
    except Exception:
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)
    pygame.display.set_caption("Wa-Tor Standalone Ecosystem & Dashboard")
    clock = pygame.time.Clock()

    font_bold = pygame.font.SysFont("Segoe UI", 14, bold=True)
    font_value = pygame.font.SysFont("Consolas", 14, bold=False)
    font_energy = pygame.font.SysFont("Consolas", 11, bold=True)
    font_emoji = pygame.font.SysFont(["segoe ui emoji", "apple color emoji", "noto color emoji", "Arial"], int(CELL_SIZE * 0.65))
    pause_font = pygame.font.SysFont("Segoe UI", 24, bold=True)

    # ---------- PRE-RENDERED ASSETS (built once, blitted every frame) ----------
    # Emojis are rescaled so the largest side equals EMOJI_RATIO of a cell
    # (lower EMOJI_RATIO = smaller emojis)
    def make_emoji(char, color):
        surf = font_emoji.render(char, True, color).convert_alpha()
        target = int(CELL_SIZE * EMOJI_RATIO)
        w, h = surf.get_size()
        factor = target / max(w, h)
        return pygame.transform.smoothscale(surf, (max(1, int(w * factor)), max(1, int(h * factor))))

    fish_img = make_emoji("🐟", (255, 255, 255))
    fish_shadow = make_emoji("🐟", (218, 165, 32, 100))
    shark_img = make_emoji("🦈", (255, 255, 255))
    shark_shadow = make_emoji("🦈", (139, 0, 0, 100))

    # Sea tiles: one surface per wave level instead of drawing 225 rounded rects per frame
    sea_tiles = {}
    for lvl in WAVE_LEVELS:
        sea_blue = max(110, min(150, int(130 + lvl)))
        sea_green = max(130, min(170, int(150 + lvl * 0.5)))
        tile = pygame.Surface((CELL_SIZE - 1, CELL_SIZE - 1), pygame.SRCALPHA)
        pygame.draw.rect(tile, (14, sea_green, sea_blue), tile.get_rect(), border_radius=4)
        sea_tiles[lvl] = tile.convert_alpha()

    # Shark energy bubbles cached by (energy value, low/high color)
    energy_cache = {}
    def get_energy_bubble(energy):
        key = energy
        bubble = energy_cache.get(key)
        if bubble is None:
            bubble = pygame.Surface((16, 16), pygame.SRCALPHA)
            pygame.draw.circle(bubble, (30, 41, 59), (8, 8), 8)
            color = (239, 68, 68) if energy <= 3 else (34, 197, 94)
            txt = font_energy.render(str(energy), True, color)
            bubble.blit(txt, txt.get_rect(center=(8, 8)))
            bubble = bubble.convert_alpha()
            energy_cache[key] = bubble
        return bubble

    # Pause veil + text
    veil = pygame.Surface((GAME_SIZE, GAME_SIZE), pygame.SRCALPHA)
    veil.fill(COLOR_PAUSE_VEIL)
    veil = veil.convert_alpha()
    pause_surface = pause_font.render("||  SIMULATION PAUSED", True, (252, 165, 165))
    pause_rect = pause_surface.get_rect(center=(GAME_SIZE // 2, GAME_SIZE // 2))

    # Dashboard: static tiles/labels drawn once, only values re-rendered when they change
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
    def get_value_surface(index, text):
        key = (index, text)
        surf = value_cache.get(key)
        if surf is None:
            if len(value_cache) > 500:
                value_cache.clear()
            surf = font_value.render(text, True, value_colors[index])
            value_cache[key] = surf
        return surf

    # ---------- SIMULATION STATE ----------
    # The simulation itself lives in classes/world.py: the interface only calls it and draws it
    grid_instance = external_grid if external_grid is not None else Grid(GRID_SIZE)
    world = quiet(World, grid_instance, GRID_SIZE)
    paused = False

    tick_count = 0
    logic_delay = 14
    wave_grid = [[random.uniform(0, 100) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # For the smooth animation (drawing only): where each entity was at the start of the turn,
    # and which entities disappeared this turn (eaten fish, dead sharks) -> (is_fish, x, y)
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

        # ENGINE TICK EXECUTION PROCESS SEQUENCE
        if not paused:
            tick_count += 1
            if tick_count >= logic_delay:
                tick_count = 0

                # Remember positions before the turn (for the animation)
                fish_before = list(world.fish_dict.values())
                sharks_before = list(world.shark_dict.values())
                prev_pos = {id(e): (e.x, e.y) for e in fish_before + sharks_before}

                # One turn of the simulation, played by World
                world.turn += 1
                quiet(world.move_entities)

                # Entities that are gone after the turn
                alive = {id(e) for e in world.fish_dict.values()} | {id(e) for e in world.shark_dict.values()}
                removed = [(True, *prev_pos[id(e)]) for e in fish_before if id(e) not in alive]
                removed += [(False, *prev_pos[id(e)]) for e in sharks_before if id(e) not in alive]

                count_fish = len(world.fish_dict)
                count_shark = len(world.shark_dict)

        fish_percent = (count_fish / total_cells) * 100
        shark_percent = (count_shark / total_cells) * 100

        # --- DRAW VISUAL CANVAS FRAME ---
        # Animation progress inside the current turn (0 -> 1), frozen while paused
        anim_p = min(1.0, (tick_count + 1) / logic_delay)

        time_ms = pygame.time.get_ticks() * 0.003
        for y in range(GRID_SIZE):
            wave_row = wave_grid[y]
            py = y * CELL_SIZE
            for x in range(GRID_SIZE):
                lvl = int(sin(time_ms + wave_row[x]) * 15)
                screen.blit(sea_tiles[lvl], (x * CELL_SIZE, py))

        half = GRID_SIZE / 2

        def interp(prev, cur):
            # shortest path on the wrapping (toroidal) grid
            d = cur - prev
            if d > half:
                d -= GRID_SIZE
            elif d < -half:
                d += GRID_SIZE
            return (prev + d * anim_p) % GRID_SIZE

        def origins(gx, gy):
            # pixel origin(s) of a sprite; drawn twice while crossing the screen edge
            ox = gx * CELL_SIZE
            oy = gy * CELL_SIZE
            xs = (ox, ox - GAME_SIZE) if ox > GAME_SIZE - CELL_SIZE else (ox,)
            ys = (oy, oy - GAME_SIZE) if oy > GAME_SIZE - CELL_SIZE else (oy,)
            return [(ax, ay) for ax in xs for ay in ys]

        center = (CELL_SIZE - 1) // 2

        # Entities eaten / starved this turn: fade out where they were
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

        # Living entities (read from World), gliding from their previous cell to the current one
        living = [(e, True) for e in world.fish_dict.values()]
        living += [(e, False) for e in world.shark_dict.values()]
        for ent, is_fish in living:
            prev_x, prev_y = prev_pos.get(id(ent), (ent.x, ent.y))
            gx = interp(prev_x, ent.x)
            gy = interp(prev_y, ent.y)
            img = fish_img if is_fish else shark_img
            shd = fish_shadow if is_fish else shark_shadow
            bubble = None if is_fish else get_energy_bubble(ent.get_stamina())
            for ax, ay in origins(gx, gy):
                screen.blit(shd, shd.get_rect(center=(ax + center + 2, ay + center + 2)))
                screen.blit(img, img.get_rect(center=(ax + center, ay + center)))
                if bubble is not None:
                    screen.blit(bubble, (ax + CELL_SIZE - 1 - 12 - 8, ay + CELL_SIZE - 1 - 12 - 8))

        if paused:
            screen.blit(veil, (0, 0))
            screen.blit(pause_surface, pause_rect)

        # --- DASHBOARD ---
        screen.blit(dashboard_bg, (0, GAME_SIZE))
        values = [
            f"{world.turn:05d}",
            f"{count_fish:03d} (🐟)",
            f"{count_shark:03d} (🦈)",
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