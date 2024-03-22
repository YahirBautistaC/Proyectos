@author: Yahir
"""

import pygame
import sys
import random
from RobotModelo import RobotModelo
from RobotVista import RobotVista
from RobotControlador import RobotControlador
from AlienModelo import AlienModelo
from AlienVista import AlienVista
from RadarVista import RadarVista

# Inicialización de pygame
pygame.init()

# Creación de la ventana del juego y asignación de un nombre
pygame.display.set_caption("Invasores del espacio")
pantalla = pygame.display.set_mode((800, 700))

# Creación de un objeto Clock para controlar el tiempo
reloj = pygame.time.Clock()

# Definición de la clase DisparoModelo
class DisparoModelo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 500

    def actualizar(self, delta_tiempo):
        desplazamiento = self.velocidad * (delta_tiempo / 1000)
        self.y -= desplazamiento

# Definición de la clase DisparoVista
class DisparoVista:
    def __init__(self, ruta_imagen):
        self.imagen = pygame.image.load(ruta_imagen)

    def dibujar(self, pantalla, modelo):
        pantalla.blit(self.imagen, (modelo.x, modelo.y))

# Creación de instancias de objetos

# Modelo, vista y controlador del robot
robot_modelo = RobotModelo(350, 600, 300, 10)
robot_vista = RobotVista('robotframes.png')
robot_controlador = RobotControlador()

# Listas para almacenar modelos y vistas de los aliens
alien_modelos = []
alien_vistas = []

# Creación de 5 instancias de modelos y vistas de aliens
for _ in range(20):
    alien_modelo = AlienModelo(random.randint(0, 800 - 32), random.randint(0, 700 - 32), 0, 500)
    alien_vista = AlienVista('alien.png', 'blip3.png')
    alien_modelos.append(alien_modelo)
    alien_vistas.append(alien_vista)

# Instancia de la vista del radar
radar_vista = RadarVista('radar.png', 'blip.png', 'blip2.png', 'blip3.png', 'blip4.png')

# Variables para el disparo actual
disparo_modelo = None
disparo_vista = None

# Variable para la posición original del robot
posicion_original = (350, 600)

# Creación de una instancia de fuente de texto
fuente = pygame.font.Font(None, 36)

# Variable para almacenar el tiempo transcurrido
tiempo_transcurrido = 0
tiempo_inicial = pygame.time.get_ticks()

# Variable para almacenar si el juego está activo o no
juego_activo = False

# Función para formatear el tiempo en minutos:segundos
def formatear_tiempo(tiempo):
    segundos = int(tiempo / 1000)
    minutos = segundos // 60
    segundos = segundos % 60
    return f"{minutos:02d}:{segundos:02d}"

# Página inicial
pantalla.fill((0, 0, 0))
texto_inicio = fuente.render("Evita ser tocado por los aliens ¡Muevete!", True, (255, 255, 255))
pantalla.blit(texto_inicio, (170, 100))
texto_continuar = fuente.render("Presiona Enter para continuar", True, (255, 255, 255))
pantalla.blit(texto_continuar, (230, 150))
texto_continuar = fuente.render("Presiona 'R' para reiniciar", True, (255, 255, 255))
pantalla.blit(texto_continuar, (230, 200))
pygame.display.update()

# Bucle principal del juego
while True:
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                juego_activo = True
            elif evento.key == pygame.K_r and not juego_activo:
                # Reiniciar el juego
                robot_modelo = RobotModelo(350, 600, 300, 5)
                robot_vista = RobotVista('robotframes.png')
                robot_controlador = RobotControlador()

                alien_modelos = []
                alien_vistas = []

                for _ in range(20):
                    alien_modelo = AlienModelo(random.randint(0, 800 - 32), random.randint(0, 700 - 32), 0, 500)
                    alien_vista = AlienVista('alien.png', 'blip3.png')
                    alien_modelos.append(alien_modelo)
                    alien_vistas.append(alien_vista)

                disparo_modelo = None
                disparo_vista = None

                tiempo_transcurrido = 0
                tiempo_inicial = pygame.time.get_ticks()

                juego_activo = True

    if juego_activo:
        # Actualización del controlador del robot
        robot_controlador.actualizar(reloj.get_time(), robot_modelo)

        # Actualización de modelos de aliens y detección de colisiones con el robot
        for alien_modelo in alien_modelos:
            alien_modelo.actualizar(reloj.get_time())
            if robot_modelo.sin_vidas():
                # Detener el juego si el robot se queda sin vidas
                juego_activo = False
                break
            if pygame.Rect(alien_modelo.x, alien_modelo.y, 32, 32).colliderect(
                pygame.Rect(robot_modelo.x, robot_modelo.y, 32, 32)
            ):
                robot_modelo.perder_vida()
                robot_modelo.x = posicion_original[0]
                robot_modelo.y = posicion_original[1]
                break

        # Disparo del robot
        if pygame.key.get_pressed()[pygame.K_SPACE] and disparo_modelo is None:
            disparo_modelo = DisparoModelo(robot_modelo.x + 16, robot_modelo.y)
            disparo_vista = DisparoVista('blip4.png')

        # Actualización del disparo y eliminación si sale de la pantalla
        if disparo_modelo is not None:
            disparo_modelo.actualizar(reloj.get_time())
            if disparo_modelo.y < 0:
                disparo_modelo = None
                disparo_vista = None

        # Actualización del tiempo transcurrido solo si el juego está activo
        if juego_activo:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = tiempo_actual - tiempo_inicial

        # Dibujado en pantalla
        pantalla.fill((0, 0, 0))

        # Dibujado del robot
        robot_vista.dibujar(pantalla, robot_modelo)

        # Dibujado de las vidas del robot
        vidas_texto = fuente.render(f"Vidas: {robot_modelo.vidas}", True, (255, 255, 255))
        pantalla.blit(vidas_texto, (350, 10))

        # Dibujado del cronómetro
        if juego_activo:
            tiempo_texto = fuente.render(formatear_tiempo(tiempo_transcurrido), True, (255, 255, 255))
        else:
            tiempo_texto = fuente.render("GAME OVER", True, (255, 255, 255))
        pantalla.blit(tiempo_texto, (630, 10))

        # Dibujado de los aliens
        for alien_vista, alien_modelo in zip(alien_vistas, alien_modelos):
            alien_vista.dibujar(pantalla, alien_modelo)

        # Dibujado del disparo
        if disparo_modelo is not None:
            disparo_vista.dibujar(pantalla, disparo_modelo)

        # Dibujado del radar
        radar_vista.dibujar(pantalla, robot_modelo, alien_modelos, disparo_modelo)

        # Actualización de la pantalla
        pygame.display.update()

        # Control de FPS (30 cuadros por segundo)
        reloj.tick(30)
