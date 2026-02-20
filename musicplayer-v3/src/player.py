#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import pygame
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

try:
    from src.profile import PROFILES, ACTIVE_PROFILE
    from src.mpg123_player import Mpg123Player
except ImportError:
    from profile import PROFILES, ACTIVE_PROFILE
    from mpg123_player import Mpg123Player

profile_config = PROFILES[ACTIVE_PROFILE]


class MusicPlayer(object):
    def __init__(self):
        self.playlist = []
        self.current_track_index = 0
        self.is_paused = False
        self.is_playing = False
        self.repeat_mode = 0 # 0: No repeat, 1: Repeat all, 2: Repeat one
        self.current_path = os.getcwd()
        self.browser_items = []
        
        self.mpg_player = Mpg123Player()
        self.mpg_player.set_volume(0.90)  # Volumen inicial al 90%

        # Buscar directorio de musica del perfil
        search_dirs = profile_config.get("SEARCH_DIRS", ["music", "/storage/roms/music"])
        for d in search_dirs:
            if os.path.exists(str(d)):
                self.current_path = os.path.abspath(str(d))
                break

        self.update_browser_items()

        # Cargar playlist inicial
        for d in search_dirs:
            d = str(d)
            if os.path.exists(d):
                pattern = os.path.join(d, "*.mp3")
                for f in glob.glob(pattern):
                    abs_path = os.path.abspath(f)
                    if abs_path not in self.playlist:
                        self.playlist.append(abs_path)
        if self.playlist:
            self.current_track_index = 0
            print("Cargadas %d canciones." % len(self.playlist))
        else:
            print("No se encontraron archivos .mp3.")

    def update_browser_items(self):
        self.browser_items = []
        try:
            items = os.listdir(self.current_path)
            dirs = []
            files = []
            for item in items:
                full_path = os.path.join(self.current_path, item)
                if os.path.isdir(full_path):
                    dirs.append(item)
                elif item.lower().endswith('.mp3'):
                    files.append(item)
            dirs.sort()
            files.sort()
            parent = os.path.dirname(self.current_path)
            if parent and parent != self.current_path:
                self.browser_items.append({'name': '..', 'type': 'dir', 'path': parent})
            for item in dirs:
                full_path = os.path.join(self.current_path, item)
                self.browser_items.append({'name': item, 'type': 'dir', 'path': full_path})
            for item in files:
                full_path = os.path.join(self.current_path, item)
                display_name = item
                try:
                    audio = MP3(full_path, ID3=EasyID3)
                    if 'title' in audio:
                        display_name = audio['title'][0]
                except:
                    pass
                self.browser_items.append({'name': display_name, 'type': 'file', 'path': full_path})
        except Exception as e:
            print("Error listando directorio %s: %s" % (self.current_path, e))

    def play_from_directory(self):
        new_playlist = [item['path'] for item in self.browser_items if item['type'] == 'file']
        if new_playlist:
            self.stop_music()
            self.playlist = new_playlist
            self.current_track_index = 0
            self.play_music()
            print("Reproduciendo directorio: %s" % self.current_path)
        else:
            print("No hay archivos mp3 en este directorio")

    def play_music(self):
        if self.playlist:
            track_path = self.playlist[self.current_track_index]
            if not os.path.isfile(track_path):
                print("Archivo no encontrado: %s" % track_path)
                return
            try:
                self.mpg_player.stop()
                if self.mpg_player.load(track_path):
                    self.mpg_player.play()
                    self.is_playing = True
                    self.is_paused = False
                else:
                    print("Error cargando archivo")
                    self.is_playing = False
            except Exception as e:
                print("Error al reproducir: %s" % e)
                self.is_playing = False

    def pause_music(self):
        if self.is_playing:
            self.mpg_player.pause()
            self.is_paused = True
            self.is_playing = False

    def stop_music(self):
        self.mpg_player.stop()
        self.is_playing = False
        self.is_paused = False

    def next_track(self):
        if self.playlist:
            self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
            self.is_paused = False
            self.play_music()

    def prev_track(self):
        if self.playlist:
            self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
            self.is_paused = False
            self.play_music()

    def toggle_play_pause(self):
        if not self.playlist:
            return
        if self.is_playing:
            self.pause_music()
        elif self.is_paused:
            self.mpg_player.unpause()
            self.is_playing = True
            self.is_paused = False
        else:
            self.play_music()
            
    def set_volume(self, vol_percent):
        # vol_percent is 0.0 to 1.0
        self.mpg_player.set_volume(max(0.0, min(1.0, vol_percent)))

    def get_volume(self):
        return self.mpg_player.get_volume()
        
    def get_current_track_name(self):
        if self.playlist and 0 <= self.current_track_index < len(self.playlist):
            track_path = self.playlist[self.current_track_index]
            try:
                audio = MP3(track_path, ID3=EasyID3)
                if 'title' in audio:
                    return audio['title'][0]
            except Exception:
                pass
            return os.path.basename(track_path)
        return None
        
    def get_current_track_cover(self):
        if self.playlist and 0 <= self.current_track_index < len(self.playlist):
            track_path = self.playlist[self.current_track_index]
            if not os.path.isfile(track_path):
                return None
            try:
                audio = MP3(track_path)
                if audio.tags:
                    for tag in audio.tags.values():
                        if hasattr(tag, 'FrameID') and tag.FrameID == 'APIC':
                            return tag.data
            except Exception:
                pass
        return None

    def get_status_text(self):
        status = "Stopped"
        if self.is_paused:
            status = "Paused"
        elif self.is_playing:
            status = "Playing"
        repeat_texts = ["No repeat", "Repeat all", "Repeat this one"]
        return "%s / %s" % (status, repeat_texts[self.repeat_mode])

    def toggle_repeat_mode(self):
        # Cycle: No repeat (0) -> Repeat this one (2) -> Repeat all (1) -> No repeat (0)
        cycle = {0: 2, 2: 1, 1: 0}
        self.repeat_mode = cycle[self.repeat_mode]


