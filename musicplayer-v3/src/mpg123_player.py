#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pygame


class Mpg123Player:
    """Reproductor de audio usando SDL_mixer (pygame.mixer.music)"""

    def __init__(self):
        # Inicializar SDL_mixer dejando que SDL negocie con el driver de audio
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        init_info = pygame.mixer.get_init()
        if init_info:
            print("SDL_mixer init: freq=%d, format=%d, channels=%d" % init_info)
        self.current_file = None
        self.is_playing = False
        self.is_paused = False
        self.volume = 1.0
        pygame.mixer.music.set_volume(self.volume)

    def load(self, filename):
        """Carga un archivo de audio"""
        self.stop()
        try:
            if not os.path.exists(filename):
                print("Error: El archivo no existe: %s" % filename)
                return False
            pygame.mixer.music.load(filename)
            self.current_file = filename
            return True
        except Exception as e:
            print("Error cargando archivo: %s" % str(e))
            return False

    def play(self):
        """Inicia o resume la reproduccion"""
        if self.is_playing and self.is_paused:
            self.unpause()
            return

        if self.is_playing:
            return

        if not self.current_file:
            print("No hay archivo cargado")
            return

        try:
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
        except Exception as e:
            print("Error reproduciendo: %s" % str(e))
            self.is_playing = False

    def pause(self):
        """Pausa la reproduccion"""
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True

    def unpause(self):
        """Resume la reproduccion"""
        if self.is_playing and self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False

    def stop(self):
        """Detiene la reproduccion"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False

    def get_busy(self):
        """Retorna True si esta reproduciendo"""
        return pygame.mixer.music.get_busy()

    def set_volume(self, volume):
        """Establece el volumen (0.0 a 1.0)"""
        #self.volume = max(0.0, min(1.0, volume))
        #pygame.mixer.music.set_volume(self.volume)
        pass

    def get_volume(self):
        """Obtiene el volumen actual"""
        return self.volume
