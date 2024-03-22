# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 14:25:05 2023

@author: Yahir
"""

import pygame

class RobotVista:
    def __init__(self, ruta_imagen):
        self.imagen = pygame.image.load(ruta_imagen)  # Carga la imagen del robot desde la ruta proporcionada
        
    def dibujar(self, pantalla, modelo):
        area = pygame.Rect(modelo.frame * 32, 0, 32, 32)  # Crea un rectángulo en la imagen basado en el atributo 'modelo.frame'
        pantalla.blit(self.imagen, (modelo.x, modelo.y), area)  # Dibuja la imagen del robot en la pantalla en la posición (modelo.x, modelo.y) utilizando el área definida