# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 15:20:12 2023

@author: Yahir
"""

import pygame

class AlienVista:
    def __init__(self, ruta_imagen, ruta_imagen_disparo):
        self.imagen = pygame.image.load(ruta_imagen)
        self.imagen_disparo = pygame.image.load(ruta_imagen_disparo)

    def dibujar(self, pantalla, modelo):
        area = pygame.Rect(modelo.frame * 32, 0, 32, 32)
        pantalla.blit(self.imagen, (modelo.x, modelo.y), area)

        if modelo.disparo_modelo is not None:
            pantalla.blit(self.imagen_disparo, (modelo.disparo_modelo.x, modelo.disparo_modelo.y))