                                # INTERFACE (PART 1 - SETUP & CINEMATIC INTRO)
import pygame
import random
import sys
import math

# --- GRAPHICAL STYLE & WINDOW CONFIGURATION ---
CELL_SIZE = 54  # Pixel width and height for an individual grid square
DASHBOARD_HEIGHT = 180  # Reserved vertical space at the bottom for statistics

# RBG LIGHT
COLOR_BG = (10, 15, 30)          # Abyssal Midnight Blue background
COLOR_TEXT_MAIN = (241, 245, 249)# Off-white for sharp typography
COLOR_TEXT_MUTED = (100, 116, 139)# Slate Grey-Blue for minor labels
COLOR_PAUSE_VEIL = (8, 12, 24, 210) # Transparent overlay dark coat

CYAN_NEON = (6, 182, 212)
GOLD_NEON = (234, 179, 8)
RED_NEON = (239, 68, 68)
PURPLE_NEON = (139, 92, 246)
GREEN_NEON = (34, 197, 94)
PANEL_BG = (20, 30, 55)
PANEL_BORDER = (40, 60, 95)

def get_average_shark_stamina(grid_instance) -> float:
    """Scans the external grid to compute the average stamina level of active sharks."""
    total_stamina = 0
    shark_count = 0
    for row in grid_instance.grid:
        for cell in row:
            if cell is not None and (cell.__class__.__name__ == "Shark" or (hasattr(cell, "get_type") and cell.get_type() == "shark")):
                stamina = getattr(cell, 'stamina', 0)
                total_stamina += stamina
                shark_count += 1
    return round(total_stamina / shark_count, 1) if shark_count > 0 else 0.0

def run_intro_animation(screen, virtual_surface, clock, base_width, base_height, game_size):
    """Animates a cinematic underwater diving sequence before initializing the main engine."""
    intro_running = True
    start_time = pygame.time.get_ticks()
    duration = 2500  # Animation frame life-span clock tracker (2.5 seconds)
    
    bubbles = [{"x": random.randint(0, base_width), "y": random.randint(base_height, base_height + 200), "speed": random.uniform(4, 9), "radius": random.randint(2, 5)} for _ in range(60)]
    font_intro = pygame.font.SysFont("Segoe UI", 20, bold=True)
    font_sub = pygame.font.SysFont("Consolas", 12)

    while intro_running:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(1.0, elapsed / duration)
        if progress >= 1.0: intro_running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        virtual_surface.fill((10, 15, 30))
        current_g = int(180 - (progress * 140))
        current_b = int(240 - (progress * 140))
        water_layer = pygame.Surface((base_width, base_height))
        water_layer.fill((10, current_g, current_b))
        virtual_surface.blit(water_layer, (0, 0))

        for b in bubbles:
            b["y"] -= b["speed"]
            wave_x = b["x"] + math.sin(b["y"] * 0.05) * 5
            pygame.draw.circle(virtual_surface, (255, 255, 255, 160), (int(wave_x), int(b["y"])), b["radius"])
            if b["y"] < -20:
                b["y"] = base_height + random.randint(0, 50)
                b["x"] = random.randint(0, base_width)

        text_alpha = max(0, min(255, int(progress * 255) if progress < 0.8 else int((1.0 - progress) * 5 * 255)))
        title_surf = font_intro.render("INITIALIZING WA-TOR CORE", True, CYAN_NEON)
        sub_surf = font_sub.render(f"READING EXTERNAL MATRIX DATA... {int(progress*100)}%", True, COLOR_TEXT_MAIN)
        title_surf.set_alpha(text_alpha)
        sub_surf.set_alpha(text_alpha)
        
        virtual_surface.blit(title_surf, title_surf.get_rect(center=(base_width // 2, base_height // 2 - 20)))
        virtual_surface.blit(sub_surf, sub_surf.get_rect(center=(base_width // 2, base_height // 2 + 15)))

        screen.fill((0, 0, 0))
        screen_w, screen_height = screen.get_size()
        scale_factor = min(screen_w / base_width, screen_height / base_height)
        new_w, new_h = int(base_width * scale_factor), int(base_height * scale_factor)
        scaled_surf = pygame.transform.smoothscale(virtual_surface, (new_w, new_h))
        screen.blit(scaled_surf, ((screen_w - new_w) // 2, (screen_height - new_h) // 2))
        pygame.display.flip()
        clock.tick(60)

                            # INTERFACE (PART 2 - LAUNCH & LOOP LISTENING TO WORLD GRID DATA)

def launch_interface(grid_instance):
    """
    Main graphical loop receiving the fully populated grid directly from world.py.
    No local population spawning or entity update methods are managed here.
    """
    pygame.init()
    
    # Read grid dimensions natively from the instance provided by world
    grid_size = grid_instance.size
    game_size = grid_size * CELL_SIZE
    base_width = game_size
    base_height = game_size + DASHBOARD_HEIGHT
    
    base_flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    screen = pygame.display.set_mode((base_width, base_height), base_flags) 
    pygame.display.set_caption("Wa-Tor Oceanic Command Core v3.0 🌌")
    clock = pygame.time.Clock()
    
    virtual_surface = pygame.Surface((base_width, base_height))
    is_fullscreen = False
    
    # Launch intro animation using the real sizes
    run_intro_animation(screen, virtual_surface, clock, base_width, base_height, game_size)

    font_title = pygame.font.SysFont("Segoe UI", 12, bold=True)
    font_value = pygame.font.SysFont("Consolas", 15, bold=True)
    font_pause = pygame.font.SysFont("Segoe UI", 26, bold=True)
    font_emoji = pygame.font.SysFont(["segoe ui emoji", "apple color emoji", "noto color emoji"], int(CELL_SIZE * 0.65))

    world_turn, tick_count, logic_delay = 0, 0, 14
    paused = False
    
    wave_map = [[random.uniform(0, 50) for _ in range(grid_size)] for _ in range(grid_size)]
    particles = [{"x": random.randint(0, base_width), "y": random.randint(0, game_size), "speed": random.uniform(0.2, 0.8), "radius": random.randint(1, 3)} for _ in range(40)]
    
    # Cosmetic environment assets completely disconnected from simulation code
    boat_data = {"active": False, "x": 0, "y": 0, "speed": 1.5, "emoji": "🚢", "target_y": 0}
    rain_ripples = []
    jellyfish_glow = {"active": False, "time": 0.0, "alpha": 0, "pulse_speed": 0.04}

    running = True
    while running:
        current_fps = int(clock.get_fps())
        time_ms = pygame.time.get_ticks()
        tick_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: paused = not paused
                elif event.key == pygame.K_UP: logic_delay = max(2, logic_delay - 2)
                elif event.key == pygame.K_DOWN: logic_delay = min(50, logic_delay + 2)
                elif event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    screen = pygame.display.set_mode((0, 0), base_flags | pygame.FULLSCREEN) if is_fullscreen else pygame.display.set_mode((base_width, base_height), base_flags)
                    
        # EXTERNAL SIMULATION TRIGGER (Synchronized with world.py data)
        if not paused:
            if tick_count >= logic_delay:
                tick_count = 0
                world_turn += 1
                # Trigger the updates ONLY via your world logic file methods if available, 
                # otherwise world.py loop handles its own pacing.
                if hasattr(grid_instance, 'update') or hasattr(grid_instance, 'update_grid'):
                    getattr(grid_instance, 'update', getattr(grid_instance, 'update_grid', lambda: None))()

                        # INTERFACE (PART 3 - PASSIVE GRID SCAN & RENDERING LOOP)
        if not paused:
            # 1. Surface vessel cosmetic spawn tracker
            if not boat_data["active"] and random.random() < 0.003:
                boat_data["active"] = True; boat_data["x"] = -60; boat_data["target_y"] = random.randint(0, grid_size - 1)
                boat_data["y"] = boat_data["target_y"] * CELL_SIZE + (CELL_SIZE // 4); boat_data["emoji"] = random.choice(["🚢", "🛥️", "⛵"])
            if boat_data["active"]:
                boat_data["x"] += boat_data["speed"]
                if boat_data["x"] > base_width + 60: boat_data["active"] = False