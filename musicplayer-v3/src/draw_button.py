#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame


def draw_button(screen, rect, image):
    """Dibuja un boton (imagen escalada) en la pantalla."""
    if image:
        screen.blit(image, (rect.x, rect.y))
    else:
        pygame.draw.rect(screen, (200, 200, 200), rect)
