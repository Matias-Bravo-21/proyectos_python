#import necesarios
import pygame
import random
import math
import sys
import os

#inicializar pygame
pygame.init()

#establecemos el tamaño de la pantalla
screen_width = 800 #establecemos ancho
screen_height = 600 #establecemos altura
screen=pygame.display.set_mode((screen_width,screen_height))

#funcion para obtener la ruta de los recursos
def resource_path(relative_path):
    try:
        base_path =sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
#cargar imagen de fondo
asset_background = resource_path("assets/images/background.png")
background = pygame.image.load(asset_background)

#cargar icono de ventana
asset_icon = resource_path("assets/images/ufo.png")
icon = pygame.image.load(asset_icon)

#cargar sonido de fondo
asset_sound = resource_path("assets/audio/background_music.mp3")
background_sound = pygame.mixer.music.load(asset_sound)

#cargar al jugador
asset_playerimg = resource_path("assets/images/space-invaders.png")
playerimg = pygame.image.load(asset_playerimg)

#cargar imagen de la bala
asset_bulletimg = resource_path("assets/images/bullet.png")
bulletimg = pygame.image.load(asset_bulletimg)

#cargar fuente para texto game over
asset_over_font = resource_path("assets/fonts/RAVIE.TTF")
over_font = pygame.font.Font(asset_over_font)

#cargar fuente para texto de puntaje
asset_score = resource_path("assets/fonts/comicbd.TTF")
score = pygame.font.Font(asset_score)

#establecer titulo de ventana
pygame.display.set_caption("replica space invader xd")

#establecer icono de ventana
pygame.display.set_icon(icon)

#reproducir musica de fondo
pygame.mixer.music.play(-1)

#crear reloj que controla velocidad del juego
clock = pygame.time.Clock()

#posicion inicial del jugador
playerX =370
playerY = 470
player_change = 0
player_change = 0

#lista que almacena posiciones del enemigo
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10

#se inicializan las variables que guardan las cords del enemigo
for i in range(no_of_enemies):
    pass