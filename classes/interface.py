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

# --- RGB COLOR ASSET ---
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
                # Updated lookup to point directly to the local 'stamina' class attribute
                stamina = getattr(cell, 'stamina', 0)
                total_stamina += stamina
                shark_count += 1
    return round(total_stamina / shark_count, 1) if shark_count > 0 else 0.0

def run_intro_animation(screen, virtual_surface, clock, base_flags):
    """Animates a cinematic underwater diving sequence before initializing the main engine."""
    intro_running = True
    start_time = pygame.time.get_ticks()
    duration = 2500  # Animation frame life-span clock tracker (2.5 seconds)

