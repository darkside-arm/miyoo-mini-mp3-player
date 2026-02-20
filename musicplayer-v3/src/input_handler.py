#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import config

try:
    from src.profile import PROFILES, ACTIVE_PROFILE
except ImportError:
    from profile import PROFILES, ACTIVE_PROFILE

profile_config = PROFILES[ACTIVE_PROFILE]


class InputHandler(object):
    def __init__(self, player):
        self.player = player
        self.mode = "player"

        # Teclas del joystick desde el perfil activo
        self.btn_menu = profile_config.get("BUTTON_MENU")
        self.btn_a = profile_config.get("BUTTON_A")
        self.btn_b = profile_config.get("BUTTON_B")
        self.btn_y = profile_config.get("BUTTON_Y")
        self.btn_x = profile_config.get("BUTTON_X")
        self.btn_start = profile_config.get("BUTTON_START")

    def set_mode(self, mode):
        self.mode = mode

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key

            # QUIT: Escape, Q, o BUTTON_MENU
            if key in (pygame.K_ESCAPE, pygame.K_q, self.btn_menu):
                return "QUIT"

            # PLAY/PAUSE o SELECT: Space o BUTTON_A
            if key in (pygame.K_SPACE, self.btn_a):
                if self.mode == "playlist":
                    return "SELECT_ITEM"
                self.player.toggle_play_pause()

            # BUTTON_START (K_RETURN): Select en playlist, Toggle repeat en player
            elif key == self.btn_start or key == pygame.K_RETURN:
                if self.mode == "playlist":
                    return "SELECT_ITEM"
                self.player.toggle_repeat_mode()
                return "TOGGLE_REPEAT"

            elif key == pygame.K_RIGHT:
                if self.mode == "playlist":
                    return "NAV_RIGHT"
                self.player.next_track()
                return "NEXT_TRACK"

            elif key == pygame.K_LEFT:
                if self.mode == "playlist":
                    return "NAV_LEFT"
                self.player.prev_track()
                return "PREV_TRACK"

            elif key == pygame.K_UP:
                if self.mode == "playlist":
                    return "NAV_UP"
                current_vol = self.player.get_volume()
                #self.player.set_volume(current_vol + 0.1)

            elif key == pygame.K_DOWN:
                if self.mode == "playlist":
                    return "NAV_DOWN"
                current_vol = self.player.get_volume()
                #self.player.set_volume(current_vol - 0.1)

            # TOGGLE PLAYLIST: P o BUTTON_B
            elif key in (pygame.K_p, self.btn_b):
                return "TOGGLE_PLAYLIST"

            # PLAY_DIR / PREV_TRACK: Y o BUTTON_Y
            elif key in (pygame.K_y, self.btn_y):
                if self.mode == "playlist":
                    return "PLAY_DIR"
                self.player.prev_track()
                return "PREV_TRACK"

            # NEXT_TRACK: X o BUTTON_X
            elif key in (pygame.K_x, self.btn_x):
                if self.mode == "player":
                    self.player.next_track()
                    return "NEXT_TRACK"

        return None

    def cleanup(self):
        pass
