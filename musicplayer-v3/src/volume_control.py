#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

class VolumeControl(object):
    def __init__(self):
        pygame.mixer.init()

    def get_volume(self):
        return pygame.mixer.music.get_volume() * 100

    def set_volume(self, percent):
        percent = max(0, min(100, int(percent)))
        pygame.mixer.music.set_volume(percent / 100.0)
