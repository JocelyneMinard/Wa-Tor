# interface.py
import pygame
import random
import sys
import math

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

# --- INTERNAL STANDALONE LOGIC CLASSES ---

class Fish:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.px = x  # position at the start of the turn (for smooth animation)
        self.py = y

    def reproduce(self, nx: int, ny: int, world_turn: int):
        old_x, old_y = self.x, self.y
        self.x, self.y = nx, ny
        if world_turn > 0 and world_turn % 8 == 0:
            return Fish(old_x, old_y)
        return None

class Shark:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.px = x
        self.py = y
        self.energy = 8

    def reproduce(self, nx: int, ny: int, world_turn: int):
        old_x, old_y = self.x, self.y
        self.x, self.y = nx, ny
        if world_turn > 0 and world_turn % 12 == 0:
            return Shark(old_x, old_y)
        return None

class Grid:
    def __init__(self, size: int) -> None:
        self.size = size
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.removed = []  # entities eaten / starved this turn (drawing only)

    def affect_entity(self, x, y, entity):
        self.grid[y][x] = entity

    def check_cell(self, x, y):
        return self.grid[y][x]

    def check_cells(self, x, y):
        possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        adjacent_cells = []
        for dx, dy in possible_moves:
            nx = (x + dx) % self.size
            ny = (y + dy) % self.size
            adjacent_cells.append((nx, ny))

        empty_cells = []
        fish_cells = []
        for cx, cy in adjacent_cells:
            content = self.check_cell(cx, cy)
            if content is None:
                empty_cells.append((cx, cy))
            elif isinstance(content, Fish):
                fish_cells.append((cx, cy))
        return empty_cells, fish_cells

    def turn_fish(self, x, y, world_turn: int):
        fish = self.grid[y][x]
        if fish is None:
            return
        empty_cells, _ = self.check_cells(x, y)
        if empty_cells:
            nx, ny = random.choice(empty_cells)
            baby = fish.reproduce(nx, ny, world_turn)
            self.affect_entity(nx, ny, fish)
            self.affect_entity(x, y, baby)

    def turn_shark(self, x, y, world_turn: int):
        shark = self.grid[y][x]
        if shark is None:
            return

        shark.energy -= 1
        if shark.energy <= 0:
            self.removed.append(shark)
            self.affect_entity(x, y, None)
            return

        # FIX: check_cells returns (empty_cells, fish_cells) in this order
        empty_cells, fish_cells = self.check_cells(x, y)

        if fish_cells:
            nx, ny = random.choice(fish_cells)
            self.removed.append(self.grid[ny][nx])
            shark.energy = min(shark.energy + 5, 12)
            shark.x, shark.y = nx, ny
            self.affect_entity(nx, ny, shark)
            self.affect_entity(x, y, None)
            if world_turn > 0 and world_turn % 12 == 0:
                baby = Shark(x, y)
                self.affect_entity(x, y, baby)
            return

        if empty_cells:
            nx, ny = random.choice(empty_cells)
            baby = shark.reproduce(nx, ny, world_turn)
            self.affect_entity(nx, ny, shark)
            self.affect_entity(x, y, baby)

# --- MAIN ENGINE CONTROL LOOP ---

TARGET_FPS = 60
START_FULLSCREEN = True  # False = start in a normal window
EMOJI_RATIO = 0.6  # emoji size relative to a cell (0.6 = 60%)
WAVE_LEVELS = range(-15, 16)  # integer wave amplitudes -> cached sea tiles

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
    grid_instance = Grid(GRID_SIZE)
    world_turn = 0
    paused = False

    tick_count = 0
    logic_delay = 14
    wave_grid = [[random.uniform(0, 100) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    for _ in range(45):
        rx, ry = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid_instance.check_cell(rx, ry) is None:
            grid_instance.affect_entity(rx, ry, Fish(rx, ry))

    for _ in range(18):
        rx, ry = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid_instance.check_cell(rx, ry) is None:
            grid_instance.affect_entity(rx, ry, Shark(rx, ry))

    # Metrics only change when the simulation ticks, so compute them there
    def count_population():
        f = s = 0
        for row in grid_instance.grid:
            for cell in row:
                if isinstance(cell, Fish):
                    f += 1
                elif isinstance(cell, Shark):
                    s += 1
        return f, s

    count_fish, count_shark = count_population()
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
                world_turn += 1
                grid_instance.removed.clear()

                fishes_to_update = []
                sharks_to_update = []
                for y in range(GRID_SIZE):
                    for x in range(GRID_SIZE):
                        cell = grid_instance.grid[y][x]
                        if cell is not None:
                            cell.px, cell.py = x, y  # remember where it was before moving
                        if isinstance(cell, Fish):
                            fishes_to_update.append((x, y))
                        elif isinstance(cell, Shark):
                            sharks_to_update.append((x, y))

                for sx, sy in sharks_to_update:
                    if isinstance(grid_instance.grid[sy][sx], Shark):
                        grid_instance.turn_shark(sx, sy, world_turn)
                for fx, fy in fishes_to_update:
                    if isinstance(grid_instance.grid[fy][fx], Fish):
                        grid_instance.turn_fish(fx, fy, world_turn)

                count_fish, count_shark = count_population()

        fish_percent = (count_fish / total_cells) * 100
        shark_percent = (count_shark / total_cells) * 100

        # --- DRAW VISUAL CANVAS FRAME ---
        # Animation progress inside the current turn (0 -> 1), frozen while paused
        anim_p = min(1.0, (tick_count + 1) / logic_delay)

        time_ms = pygame.time.get_ticks() * 0.003
        grid_cells = grid_instance.grid
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
            for ent in grid_instance.removed:
                is_fish = isinstance(ent, Fish)
                img = fish_img if is_fish else shark_img
                shd = fish_shadow if is_fish else shark_shadow
                img.set_alpha(fade)
                shd.set_alpha(fade)
                for ax, ay in origins(ent.px, ent.py):
                    screen.blit(shd, shd.get_rect(center=(ax + center + 2, ay + center + 2)))
                    screen.blit(img, img.get_rect(center=(ax + center, ay + center)))
                img.set_alpha(255)
                shd.set_alpha(255)

        # Living entities, gliding from their previous cell to the current one
        for y in range(GRID_SIZE):
            row_cells = grid_cells[y]
            for x in range(GRID_SIZE):
                cell_content = row_cells[x]
                if cell_content is None:
                    continue
                gx = interp(cell_content.px, x)
                gy = interp(cell_content.py, y)
                is_fish = isinstance(cell_content, Fish)
                img = fish_img if is_fish else shark_img
                shd = fish_shadow if is_fish else shark_shadow
                bubble = None if is_fish else get_energy_bubble(cell_content.energy)
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
            f"{world_turn:05d}",
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