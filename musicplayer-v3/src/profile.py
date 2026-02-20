#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- PERFILES DE CONSTRUCCIÓN ---
import pygame


PROFILES = {
    "r36t max": {
        "WINDOW_WIDTH": 700,
        "WINDOW_HEIGHT": 680,
        "BUTTON_B": 1,
        "BUTTON_A": 0,
        "BUTTON_X": 2,
        "BUTTON_Y": 3,
        "BUTTON_MENU": 9,
        "BUTTON_DUP": 14,
        "BUTTON_DDOWN": 15,
        "SEARCH_DIRS": ["music", "/storage/roms/music"]
    },
    "r36t": {
        "WINDOW_WIDTH": 640,
        "WINDOW_HEIGHT": 480,
        "BUTTON_B": 0,  # Ejemplo: botones invertidos
        "BUTTON_A": 1,
        "BUTTON_X": 3,
        "BUTTON_Y": 4,
        "BUTTON_MENU": 10,
        "BUTTON_DUP": 14,
        "BUTTON_DDOWN": 15,
        "SEARCH_DIRS": ["music", "/storage/roms/music"]
    },

    "r36s ultra": {
        "WINDOW_WIDTH": 700,
        "WINDOW_HEIGHT": 680,
        "BUTTON_B": 0,  # Ejemplo: botones invertidos
        "BUTTON_A": 1,
        "BUTTON_X": 3,
        "BUTTON_Y": 4,
        "BUTTON_MENU": 10,
        "BUTTON_DUP": 13,
        "BUTTON_DDOWN": 14,
        "SEARCH_DIRS": ["music", "/storage/roms/music"]
    },

    "miyoo mini v3": {
        "WINDOW_WIDTH": 640,
        "WINDOW_HEIGHT": 480,
        "BUTTON_B": pygame.K_LCTRL,  # Ejemplo: botones invertidos
        "BUTTON_A": pygame.K_SPACE,
        "BUTTON_X": pygame.K_LSHIFT,
        "BUTTON_Y": pygame.K_LALT,
        "BUTTON_MENU": pygame.K_HOME,
        "BUTTON_START": pygame.K_RETURN,
        "BUTTON_DUP": pygame.K_UP,
        "BUTTON_DDOWN": pygame.K_DOWN,
        "SEARCH_DIRS": ["music", "/mnt/SDCARD/Media/Music/"]
    }

}

# Selecciona el perfil activo aquí
ACTIVE_PROFILE = "miyoo mini v3"
