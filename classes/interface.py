import pygame
import random
import sys
import math

# --- LOGIC MODULE IMPORTS ---
# Importing core logic classes from separate local source files
from grid import Grid
from fish import Fish
from shark import Shark

# --- GRAPHICAL STYLE & WINDOW CONFIGURATION ---
CELL_SIZE = 54  # Pixel width and height for an individual grid square
GRID_SIZE = 15  # Fixed number of cells on each axis of the sea matrix
GAME_SIZE = GRID_SIZE * CELL_SIZE
DASHBOARD_HEIGHT = 180  # Reserved vertical space at the bottom for statistics
BASE_WIDTH = GAME_SIZE
BASE_HEIGHT = GAME_SIZE + DASHBOARD_HEIGHT

# --- RGB COLOR ---
COLOR_BG = (10, 15, 30)          # Abyssal Midnight Blue background
COLOR_TEXT_MAIN = (241, 245, 249)# Off-white for sharp typography
COLOR_TEXT_MUTED = (100, 116, 139)# Slate Grey-Blue for minor labels
COLOR_PAUSE_VEIL = (8, 12, 24, 210) # Transparent overlay dark coat

# Neon Theme Assets for HUD Interface
CYAN_NEON = (6, 182, 212)
GOLD_NEON = (234, 179, 8)
RED_NEON = (239, 68, 68)
PURPLE_NEON = (139, 92, 246)
GREEN_NEON = (34, 197, 94)
PANEL_BG = (20, 30, 55)
PANEL_BORDER = (40, 60, 95)

def get_average_shark_stamina(grid_instance) -> float:
    """Scans the grid externally to compute the average stamina level of all active sharks."""
    total_stamina = 0
    shark_count = 0
    for row in grid_instance.grid:
        for cell in row:
            if cell.__class__.__name__ == "Shark" or (hasattr(cell, "get_type") and cell.get_type() == "shark"):
                stamina = getattr(cell, 'stamina', 0)
                total_stamina += stamina
                shark_count += 1
    return round(total_stamina / shark_count, 1) if shark_count > 0 else 0.0

def run_intro_animation(screen, virtual_surface, clock):
    """Animates a cinematic underwater diving sequence before initializing the main engine."""
    intro_running = True
    start_time = pygame.time.get_ticks()
    duration = 2500  # Animation frame life-span clock tracker (2.5 seconds)
    
    # Pre-populating rising air bubble particle dictionaries
    bubbles = [{"x": random.randint(0, BASE_WIDTH), "y": random.randint(BASE_HEIGHT, BASE_HEIGHT + 200), "speed": random.uniform(4, 9), "radius": random.randint(2, 5)} for _ in range(60)]
    
    font_intro = pygame.font.SysFont("Segoe UI", 20, bold=True)
    font_sub = pygame.font.SysFont("Consolas", 12)

    while intro_running:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(1.0, elapsed / duration)
        if progress >= 1.0: 
            intro_running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

        virtual_surface.fill((10, 15, 30))
        
        # Color interpolation matrix mimicking daylight loss during descent
        current_g = int(180 - (progress * 140))
        current_b = int(240 - (progress * 140))
        water_layer = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
        water_layer.fill((10, current_g, current_b))
        virtual_surface.blit(water_layer, (0, 0))

        # Iterating bubbles with mathematical sine dispersion
        for b in bubbles:
            b["y"] -= b["speed"]
            wave_x = b["x"] + math.sin(b["y"] * 0.05) * 5
            pygame.draw.circle(virtual_surface, (255, 255, 255, 160), (int(wave_x), int(b["y"])), b["radius"])
            if b["y"] < -20:
                b["y"] = BASE_HEIGHT + random.randint(0, 50)
                b["x"] = random.randint(0, BASE_WIDTH)

        text_alpha = max(0, min(255, int(progress * 255) if progress < 0.8 else int((1.0 - progress) * 5 * 255)))
        title_surf = font_intro.render("INITIALIZING WA-TOR CORE", True, CYAN_NEON)
        sub_surf = font_sub.render(f"DIVING UNDER SURFACE... {int(progress*100)}%", True, COLOR_TEXT_MAIN)
        title_surf.set_alpha(text_alpha)
        sub_surf.set_alpha(text_alpha)
        
        virtual_surface.blit(title_surf, title_surf.get_rect(center=(BASE_WIDTH // 2, BASE_HEIGHT // 2 - 20)))
        virtual_surface.blit(sub_surf, sub_surf.get_rect(center=(BASE_WIDTH // 2, BASE_HEIGHT // 2 + 15)))

        # Dynamic fullscreen view aspect-ratio resolution scaling mapping
        screen.fill((0, 0, 0))
        screen_w, screen_height = screen.get_size()
        scale_factor = min(screen_w / BASE_WIDTH, screen_height / BASE_HEIGHT)
        new_w, new_h = int(BASE_WIDTH * scale_factor), int(BASE_HEIGHT * scale_factor)
        scaled_surf = pygame.transform.smoothscale(virtual_surface, (new_w, new_h))
        screen.blit(scaled_surf, ((screen_w - new_w) // 2, (screen_height - new_h) // 2))
        
        pygame.display.flip()
        clock.tick(60)
