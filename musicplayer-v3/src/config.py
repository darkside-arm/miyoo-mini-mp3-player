#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pygame

try:
    from src.profile import PROFILES, ACTIVE_PROFILE
except ImportError:
    from profile import PROFILES, ACTIVE_PROFILE

profile_config = PROFILES[ACTIVE_PROFILE]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
ASSETS_DIR = os.path.join(SCRIPT_DIR, 'assets')

# Pantalla
WIDTH = profile_config["WINDOW_WIDTH"]
HEIGHT = profile_config["WINDOW_HEIGHT"]
CAPTION = "Music Player"

# Botones de joystick
BUTTON_B = profile_config["BUTTON_B"]
BUTTON_A = profile_config["BUTTON_A"]
BUTTON_X = profile_config["BUTTON_X"]
BUTTON_Y = profile_config["BUTTON_Y"]
BUTTON_MENU = profile_config["BUTTON_MENU"]
BUTTON_DUP = profile_config.get("BUTTON_DUP", 14)
BUTTON_DDOWN = profile_config.get("BUTTON_DDOWN", 15)
BUTTON_SIZE = (80, 80)

# Colores RGB
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
ACCENT = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

# Fuentes (se inicializan en init_pygame)
FONT_LARGE = None
FONT_MEDIUM = None
FONT_SMALL = None


def load_font(size):
    font_path = os.path.join(ASSETS_DIR, 'PublicPixel.ttf')
    if os.path.exists(font_path):
        return pygame.font.Font(font_path, size)
    print("Warning: Font not found at %s" % font_path)
    return pygame.font.Font(None, size)


def init_pygame():
    global FONT_LARGE, FONT_MEDIUM, FONT_SMALL
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    # Inicializar pygame con audio real (SDL_mixer auto-detecta parametros)
    pygame.display.init()
    pygame.font.init()
    pygame.mixer.init()
    



    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(CAPTION)

    FONT_LARGE = load_font(24)
    FONT_MEDIUM = load_font(22)
    FONT_SMALL = load_font(18)

    return screen
