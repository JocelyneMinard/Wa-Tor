import pygame
import random
import sys
import math

# --- LOGIC MODULE IMPORTS ---
from grid import Grid
from fish import Fish
from shark import Shark

# --- GRAPHICAL STYLE & WINDOW CONFIGURATION ---
CELL_SIZE = 54  # Enhanced grid cell pixel density
GRID_SIZE = 15  
GAME_SIZE = GRID_SIZE * CELL_SIZE
DASHBOARD_HEIGHT = 180  
BASE_WIDTH = GAME_SIZE
BASE_HEIGHT = GAME_SIZE + DASHBOARD_HEIGHT

