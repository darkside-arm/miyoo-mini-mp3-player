#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pygame
import config


class PlaylistScreen(object):
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.selected_index = 0
        self.scroll_offset = 0
        self.font = pygame.font.Font(None, 30)

        # Cargar iconos de carpeta y archivo mp3
        icon_size = (18, 18)
        self.icon_folder = None
        self.icon_file = None
        folder_icon_path = os.path.join(config.ASSETS_DIR, 'fold.png')
        file_icon_path = os.path.join(config.ASSETS_DIR, 'filemp3.png')
        try:
            if os.path.exists(folder_icon_path):
                self.icon_folder = pygame.image.load(folder_icon_path).convert_alpha()
                self.icon_folder = pygame.transform.scale(self.icon_folder, icon_size)
        except Exception as e:
            print("Error cargando icono carpeta: %s" % e)
        try:
            if os.path.exists(file_icon_path):
                self.icon_file = pygame.image.load(file_icon_path).convert_alpha()
                self.icon_file = pygame.transform.scale(self.icon_file, icon_size)
        except Exception as e:
            print("Error cargando icono mp3: %s" % e)

        # Marquee state
        self.marquee_offset = 0
        self.marquee_direction = 1
        self.marquee_wait = 60
        self.marquee_index = -1  # indice del item con marquee activo

    def move_up(self):
        if self.selected_index > 0:
            self.selected_index -= 1
            if self.selected_index < self.scroll_offset:
                self.scroll_offset = self.selected_index
            self._reset_marquee()

    def move_down(self):
        if self.selected_index < len(self.player.browser_items) - 1:
            self.selected_index += 1
            item_height = 40
            max_items = (config.HEIGHT - 100) // item_height
            if self.selected_index >= self.scroll_offset + max_items:
                self.scroll_offset = self.selected_index - max_items + 1
            self._reset_marquee()

    def _reset_marquee(self):
        self.marquee_offset = 0
        self.marquee_direction = 1
        self.marquee_wait = 60
        self.marquee_index = -1

    def get_selected_item(self):
        if 0 <= self.selected_index < len(self.player.browser_items):
            return self.player.browser_items[self.selected_index]
        return None


    def render(self):
        self.screen.fill((50, 0, 0))
        start_x = 50
        start_y = 50
        item_height = 40
        max_items = (config.HEIGHT - 100) // item_height
        visible_items = self.player.browser_items[self.scroll_offset : self.scroll_offset + max_items]
        for i, item in enumerate(visible_items):
            real_index = self.scroll_offset + i
            y = start_y + i * item_height
            color = (255,255,0) if real_index == self.selected_index else (200,200,200)
            name = item.get('name', '')

            # Dibujar icono segun tipo
            icon = None
            icon_y_offset = 0
            if item.get('type') == 'dir' and self.icon_folder:
                icon = self.icon_folder
                icon_y_offset = -4
            elif item.get('type') == 'file' and self.icon_file:
                icon = self.icon_file

            text_offset = start_x
            if icon:
                icon_y = y + (item_height - 18) // 2 - 10 + icon_y_offset
                self.screen.blit(icon, (start_x, icon_y))
                text_offset = start_x + 24  # 18px icono + 6px espacio

            text = self.font.render(name, True, color)
            text_w = text.get_width()
            text_h = text.get_height()
            max_text_width = config.WIDTH - text_offset - 20

            is_selected = (real_index == self.selected_index)

            if is_selected and text_w > max_text_width:
                # Marquee para texto seleccionado que no entra
                if self.marquee_index != real_index:
                    self.marquee_index = real_index
                    self.marquee_offset = 0
                    self.marquee_direction = 1
                    self.marquee_wait = 60

                overflow = text_w - max_text_width
                if self.marquee_wait > 0:
                    self.marquee_wait -= 1
                else:
                    self.marquee_offset += self.marquee_direction
                    if self.marquee_offset >= overflow:
                        self.marquee_offset = overflow
                        self.marquee_direction = -1
                        self.marquee_wait = 60
                    elif self.marquee_offset <= 0:
                        self.marquee_offset = 0
                        self.marquee_direction = 1
                        self.marquee_wait = 60

                clip_rect = pygame.Rect(text_offset, y, max_text_width, item_height)
                self.screen.set_clip(clip_rect)
                self.screen.blit(text, (text_offset - self.marquee_offset, y))
                self.screen.set_clip(None)
            else:
                self.screen.blit(text, (text_offset, y))

        # Leyenda simple
        #legend = self.font.render('A: Play current directory', True, (255,255,255))
        #self.screen.blit(legend, (start_x, config.HEIGHT - 60))

    def cleanup(self):
        pass
