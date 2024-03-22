# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 14:38:07 2023

@author: Yahir
"""

import random  # Importa el módulo random para generar números aleatorios

class AlienModelo:
    def __init__(self, x, y, frame, tiempo_reiniciador_cronometro):
        self.x = x  # Posición en el eje x del modelo de Alien
        self.y = y  # Posición en el eje y del modelo de Alien
        self.frame = frame  # El número de frame actual del modelo de Alien
        self.tiempo_reiniciador_cronometro = tiempo_reiniciador_cronometro // 0.5  # El tiempo entre reinicios del cronómetro dividido por 2
        self.cronometro = 0  # El valor actual del cronómetro
        self.velocidad = random.randint(150, 300)  # Velocidad aleatoria del Alien, entre 150 y 300
        self.disparo_modelo = None  # Modelo de disparo del Alien (inicialmente nulo)

    def actualizar(self, delta_tiempo):
        self.cronometro += delta_tiempo  # Aumenta el valor del cronómetro por el delta de tiempo
        if self.cronometro >= self.tiempo_reiniciador_cronometro:  # Si el cronómetro supera el tiempo de reinicio
            self.cronometro = 0  # Reinicia el cronómetro
            self.frame += 1  # Incrementa el número de frame en 1
            self.frame %= 4  # Hace un bucle circular para los frames, asegurándose de que no sea mayor que 3
            self.mover()  # Llama al método mover() para actualizar la posición del Alien

        if self.disparo_modelo is None and random.random() < 0.01:  # Si no hay un disparo actual y un número aleatorio es menor a 0.01
            self.disparar()  # Llama al método disparar() para crear un nuevo disparo del Alien

        if self.disparo_modelo is not None:  # Si hay un disparo actual
            self.disparo_modelo.actualizar(delta_tiempo)  # Llama al método actualizar() del disparo para actualizar su posición
            if self.disparo_modelo.y > 700:  # Si el disparo ha salido de la pantalla
                self.disparo_modelo = None  # Elimina el disparo asignándole el valor None

    def mover(self):
        self.x += self.velocidad  # Actualiza la posición en el eje x del Alien según su velocidad

        if self.x <= 0 or self.x >= 640 - 32:  # Si el Alien ha alcanzado los límites de la pantalla
            self.velocidad *= -1  # Invierte la dirección de la velocidad (rebote)

    def disparar(self):
        self.disparo_modelo = DisparoAlienModelo(self.x + 12, self.y + 32)  # Crea un nuevo objeto DisparoAlienModelo con una posición inicial relativa al Alien

class DisparoAlienModelo:
    def __init__(self, x, y):
        self.x = x  # Posición en el eje x del disparo del Alien
        self.y = y  # Posición en el eje y del disparo del Alien
        self.velocidad = 300  # Velocidad del disparo del Alien

    def actualizar(self, delta_tiempo):
        self.y += self.velocidad * (delta_tiempo / 1000)  # Actualiza la posición en el eje y del disparo del Alien basado en la velocidad y el delta de tiempo