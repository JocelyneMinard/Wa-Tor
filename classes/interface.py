# interface.py (Part 1 - Initialization & Internal Core Classes)
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
# interface.py (Part 2 - Simulation Launcher & Movement Processing Loops)
    def turn_fish(self, x, y, world_turn: int):
        fish = self.grid[y][x]
        if fish is None: return
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
            self.affect_entity(x, y, None)
            return

        fish_cells, empty_cells = self.check_cells(x, y)

        if fish_cells:
            nx, ny = random.choice(fish_cells)
            shark.energy = min(shark.energy + 5, 12)
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

def main():
    pygame.init()
    
    # Double buffer mode and hardware acceleration flags
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags) 
    pygame.display.set_caption("Wa-Tor Standalone Ecosystem & Dashboard 📊")
    clock = pygame.time.Clock()
    
    # Vector font assets initialization
    font_bold = pygame.font.SysFont("Segoe UI", 14, bold=True)
    font_value = pygame.font.SysFont("Consolas", 14, bold=False)
    font_energy = pygame.font.SysFont("Consolas", 11, bold=True)
    font_emoji = pygame.font.SysFont(["segoe ui emoji", "apple color emoji", "noto color emoji", "Arial"], int(CELL_SIZE * 0.65))

    # Grid mapping module deployment
    grid_instance = Grid(GRID_SIZE)
    world_turn = 0
    paused = False
    
    tick_count = 0
    logic_delay = 14  # Refresh gap intervals between computation calculations
    wave_grid = [[random.uniform(0, 100) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # Dynamic random allocations (45 Fish models / 18 Shark trackers)
    for _ in range(45):
        rx, ry = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid_instance.check_cell(rx, ry) is None: 
            grid_instance.affect_entity(rx, ry, Fish(rx, ry))

    for _ in range(18):
        rx, ry = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid_instance.check_cell(rx, ry) is None: 
            grid_instance.affect_entity(rx, ry, Shark(rx, ry))

    running = True
    while running:
        current_fps = int(clock.get_fps())
        tick_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_UP:    # Speeds up current timeline updates pace
                    logic_delay = max(1, logic_delay - 2)
                elif event.key == pygame.K_DOWN:  # Extends step update intervals pace
                    logic_delay = min(60, logic_delay + 2)

        # ENGINE TICK EXECUTION PROCESS SEQUENCE
        if not paused:
            if tick_count >= logic_delay:
                tick_count = 0
                world_turn += 1
                
                fishes_to_update = []
                sharks_to_update = []
                for y in range(GRID_SIZE):
                    for x in range(GRID_SIZE):
                        cell = grid_instance.grid[y][x]
                        if isinstance(cell, Fish): fishes_to_update.append((x, y))
                        elif isinstance(cell, Shark): sharks_to_update.append((x, y))
                            
                for sx, sy in sharks_to_update:
                    if isinstance(grid_instance.grid[sy][sx], Shark): 
                        grid_instance.turn_shark(sx, sy, world_turn)
                for fx, fy in fishes_to_update:
                    if isinstance(grid_instance.grid[fy][fx], Fish): 
                        grid_instance.turn_fish(fx, fy, world_turn)
# interface.py (Part 3 - Liquid Vector Canvas Blit & Dashboard HUD telemetry)
        # Computing metric counts on-the-fly
        count_fish, count_shark = 0, 0
        for row in grid_instance.grid:
            for cell in row:
                if isinstance(cell, Fish): count_fish += 1
                elif isinstance(cell, Shark): count_shark += 1
        
        total_cells = GRID_SIZE * GRID_SIZE
        fish_percent = (count_fish / total_cells) * 100 if total_cells > 0 else 0
        shark_percent = (count_shark / total_cells) * 100 if total_cells > 0 else 0

        # --- DRAW VISUAL CANVAS FRAME ---
        screen.fill(COLOR_BG) 

        # Render background oceanic mesh layout using trigonometric wave maps
        time_ms = pygame.time.get_ticks() * 0.003
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
                
                wave_factor = math.sin(time_ms + wave_grid[y][x]) * 15
                sea_blue = max(110, min(150, int(130 + wave_factor)))
                sea_green = max(130, min(170, int(150 + wave_factor * 0.5)))
                
                pygame.draw.rect(screen, (14, sea_green, sea_blue), rect, border_radius=4)
                
                cell_content = grid_instance.check_cell(x, y)
                if isinstance(cell_content, Fish):
                    shadow = font_emoji.render("🐟", True, (218, 165, 32, 100))
                    screen.blit(shadow, shadow.get_rect(center=(rect.centerx + 2, rect.centery + 2)))
                    emoji = font_emoji.render("🐟", True, (255, 255, 255))
                    screen.blit(emoji, emoji.get_rect(center=rect.center))
                    
                elif isinstance(cell_content, Shark):
                    shadow = font_emoji.render("🦈", True, (139, 0, 0, 100))
                    screen.blit(shadow, shadow.get_rect(center=(rect.centerx + 2, rect.centery + 2)))
                    emoji = font_emoji.render("🦈", True, (255, 255, 255))
                    screen.blit(emoji, emoji.get_rect(center=rect.center))
                    
                    # Core predator vitality circle metric bubble tracking remaining health properties
                    energy_color = (239, 68, 68) if cell_content.energy <= 3 else (34, 197, 94)
                    pygame.draw.circle(screen, (30, 41, 59), (rect.right - 12, rect.bottom - 12), 8)
                    energy_surface = font_energy.render(str(cell_content.energy), True, energy_color)
                    screen.blit(energy_surface, energy_surface.get_rect(center=(rect.right - 12, rect.bottom - 12)))

        # Mask layer displayed when active status drops to pause state
        if paused:
            veil = pygame.Surface((GAME_SIZE, GAME_SIZE), pygame.SRCALPHA)
            veil.fill(COLOR_PAUSE_VEIL)
            screen.blit(veil, (0, 0))
            pause_font = pygame.font.SysFont("Segoe UI", 24, bold=True)
            pause_surface = pause_font.render("||  SIMULATION PAUSED", True, (252, 165, 165))
            screen.blit(pause_surface, pause_surface.get_rect(center=(GAME_SIZE // 2, GAME_SIZE // 2)))

        # --- MODULE DASHBOARD TELEMETRY GRIDS ---
        metrics = [
            {"label": "Chronons (Turns)", "val": f"{world_turn:05d}", "color": (147, 197, 253)},
            {"label": "Fish Population", "val": f"{count_fish:03d} (🐟)", "color": (253, 224, 71)},
            {"label": "Shark Population", "val": f"{count_shark:03d} (🦈)", "color": (248, 113, 113)},
            {"label": "Engine Velocity", "val": f"{60//logic_delay} step/s", "color": (167, 139, 250)},
            {"label": "Prey Density", "val": f"{fish_percent:.1f} %", "color": (52, 211, 153)},
            {"label": "Predator Density", "val": f"{shark_percent:.1f} %", "color": (251, 146, 60)},
            {"label": "Hardware Render", "val": f"{current_fps} FPS", "color": (34, 211, 238)},
            {"label": "Input Keybindings", "val": "SPACE | UP/DOWN", "color": (148, 163, 184)}
        ]

        box_w = WINDOW_WIDTH // 4
        box_h = 60
        start_y = GAME_SIZE + 15

        for i, item in enumerate(metrics):
            col = i % 4
            row = i // 4
            bx = col * box_w + 8
            by = start_y + row * box_h + 4

            tile_rect = pygame.Rect(bx, by, box_w - 16, box_h - 8)
            pygame.draw.rect(screen, COLOR_PANEL, tile_rect, border_radius=6)
            pygame.draw.rect(screen, COLOR_BORDER, tile_rect, 1, border_radius=6)

            lbl_surf = font_bold.render(item["label"], True, (148, 163, 184))
            val_surf = font_value.render(item["val"], True, item["color"])
            
            screen.blit(lbl_surf, (bx + 10, by + 8))
            screen.blit(val_surf, (bx + 10, by + 26))

        pygame.display.flip() 
        clock.tick()  

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
