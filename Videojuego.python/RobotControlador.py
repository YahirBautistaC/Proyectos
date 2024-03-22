# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 14:27:59 2023

@author: Yahir
"""

import pygame  # Importar el módulo pygame para el desarrollo del juego

class RobotControlador:
    def __init__(self):
        # Variables de estado del robot
        self.disparo_activo = False  # Indica si el robot está disparando
        self.disparo_x = 0  # Coordenada x del disparo del robot
        self.disparo_y = 0  # Coordenada y del disparo del robot
        self.velocidad_disparo = 100000  # Ajustar la velocidad de disparo aquí
    
    def actualizar(self, delta_tiempo, modelo):
        modelo.temporizador -= delta_tiempo  # Actualizar el temporizador del modelo
        
        if modelo.temporizador < 0:
            modelo.temporizador += modelo.tiempo_reiniciador_temporizador  # Reiniciar el temporizador
            modelo.frame += 1  # Avanzar al siguiente frame
            modelo.frame %= 2  # Asegurar que el frame se mantenga en el rango de 0 a 1
        
        teclas = pygame.key.get_pressed()  # Obtener el estado de las teclas presionadas
        
        if teclas[pygame.K_RIGHT]:  # Si la tecla derecha está presionada
            modelo.x += modelo.pixelporseg * (delta_tiempo / 1000)  # Mover el modelo hacia la derecha
        elif teclas[pygame.K_LEFT]:  # Si la tecla izquierda está presionada
            modelo.x -= modelo.pixelporseg * (delta_tiempo / 1000)  # Mover el modelo hacia la izquierda
        elif teclas[pygame.K_UP]:  # Si la tecla arriba está presionada
            modelo.y -= modelo.pixelporseg * (delta_tiempo / 1000)  # Mover el modelo hacia arriba
        elif teclas[pygame.K_DOWN]:  # Si la tecla abajo está presionada
            modelo.y += modelo.pixelporseg * (delta_tiempo / 1000)  # Mover el modelo hacia abajo
        
        if modelo.x <= 0:  # Si el modelo se sale por la izquierda de la ventana
            modelo.x = 0  # Mantener el modelo en el límite izquierdo
        if modelo.y <= 0:  # Si el modelo se sale por arriba de la ventana
            modelo.y = 0  # Mantener el modelo en el límite superior
        if modelo.x >= 800 - 32:  # Si el modelo se sale por la derecha de la ventana
            modelo.x = 800 - 32  # Mantener el modelo en el límite derecho
        if modelo.y >= 700 - 32:  # Si el modelo se sale por abajo de la ventana
            modelo.y = 700 - 32  # Mantener el modelo en el límite inferior
        
        # Manejar disparo
        if teclas[pygame.K_SPACE]:  # Si la tecla de espacio está presionada
            if not self.disparo_activo:  # Si no hay un disparo activo en este momento
                self.disparo_activo = True  # Activar el disparo
                self.disparo_x = modelo.x + 16  # Establecer la coordenada x del disparo
                self.disparo_y = modelo.y  # Establecer la coordenada y del disparo
        
        if self.disparo_activo:  # Si hay un disparo activo
            self.disparo_y -= self.velocidad_disparo * (delta_tiempo / 100000)  # Mover el disparo hacia arriba
            
            if self.disparo_y <= 0:  # Si el disparo se sale por arriba de la ventana
                self.disparo_activo = False  # Desactivar el disparo