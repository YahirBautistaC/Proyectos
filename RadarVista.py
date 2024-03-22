# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 14:26:36 2023

@author: Yahir
"""

import pygame  # Importar la biblioteca Pygame

class RadarVista:
    def __init__(self, imagen_radar, imagen_blip_robot, imagen_blip_alien, imagen_blip_alien_down, imagen_blip_disparo):
        self.imagen_radar = pygame.image.load(imagen_radar)  # Cargar imagen del radar
        self.imagen_blip_robot = pygame.image.load(imagen_blip_robot)  # Cargar imagen del blip del robot
        self.imagen_blip_alien = pygame.image.load(imagen_blip_alien)  # Cargar imagen del blip de los aliens
        self.imagen_blip_alien_down = pygame.image.load(imagen_blip_alien_down)  # Cargar imagen del blip de los aliens caídos
        self.imagen_blip_disparo = pygame.image.load(imagen_blip_disparo)  # Cargar imagen del blip del disparo

    def dibujar(self, pantalla, modelo_robot, lista_alien, modelo_disparo):
        pantalla.blit(self.imagen_radar, (0, 0))  # Dibujar la imagen del radar en la pantalla en la posición (0, 0)

        # Dibujar blip del robot
        x_robot = (modelo_robot.x / 12.8) + 1  # Calcular la posición x del blip del robot en función de las coordenadas del modelo del robot
        y_robot = (modelo_robot.y / 12.8) + 1  # Calcular la posición y del blip del robot en función de las coordenadas del modelo del robot
        pantalla.blit(self.imagen_blip_robot, (x_robot, y_robot))  # Dibujar la imagen del blip del robot en la pantalla en la posición calculada

        # Dibujar blip de los aliens
        for alien in lista_alien:  # Iterar sobre la lista de aliens
            x_alien = (alien.x / 12.8) + 1  # Calcular la posición x del blip del alien en función de las coordenadas del alien
            y_alien = (alien.y / 12.8) + 1  # Calcular la posición y del blip del alien en función de las coordenadas del alien
            if alien.frame == 2:  # Verificar el valor de "frame" del alien para determinar qué imagen de blip utilizar
                pantalla.blit(self.imagen_blip_alien_down, (x_alien, y_alien))  # Dibujar la imagen del blip del alien caído en la pantalla en la posición calculada
            else:
                pantalla.blit(self.imagen_blip_alien, (x_alien, y_alien))  # Dibujar la imagen del blip del alien en la pantalla en la posición calculada

        # Dibujar blip del disparo
        if modelo_disparo is not None:  # Verificar si hay un modelo de disparo válido
            x_disparo = (modelo_disparo.x / 12.8) + 1  # Calcular la posición x del blip del disparo en función de las coordenadas del modelo de disparo
            y_disparo = (modelo_disparo.y / 12.8) + 1  # Calcular la posición y del blip del disparo en función de las coordenadas del modelo de disparo
            pantalla.blit(self.imagen_blip_disparo, (x_disparo, y_disparo))  # Dibujar la imagen del blip del disparo en la pantalla en la posición calculada