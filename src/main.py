import pygame
import constantes
from personaje import Personaje
import personaje
from weapon import Weapon
from cocina import Cocina
from Enemigos.enemigo_normal import Enemigo_normal
import os
import random


pygame.init()
pygame.display.set_caption("NOMBRE JUEGO")

screen = pygame.display.set_mode(
    (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA)
)

reloj = pygame.time.Clock()


def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (int(w * scale), int(h * scale)))


# -------- CARGA DE RECURSOS --------
#PERSONAJE
animaciones = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

for i in range(8):
    img_path = os.path.join(
        BASE_DIR,
        "..",
        "assets",
        "Images",
        "characters",
        "Player",
        f"Personaje_Principal-{i}.png"
    )

    img = pygame.image.load(img_path).convert_alpha()
    img = escalar_img(img, constantes.SCALA_PERSONAJE)

    animaciones.append(img)
#ARMA
img_path = os.path.join(BASE_DIR,"..","assets","Images","weapons","Empanada.png")
imagen_pistola = pygame.image.load(img_path).convert_alpha()
imagen_pistola = escalar_img(imagen_pistola, constantes.SCALA_ARMA)
#BALAS
img_balas = os.path.join(BASE_DIR,"..","assets","Images","weapons","Empanada.png")
imagen_balas = pygame.image.load(img_balas).convert_alpha()
imagen_balas = escalar_img(imagen_pistola, constantes.SCALA_ARMA)

# ENEMIGO
enemigos = []
animaciones_enemigo=[]
spawn_cooldown = 2000  # milisegundos (2 segundos)
ultimo_spawn = pygame.time.get_ticks()
for i in range(7):
    img_enemigo_path = os.path.join(
        BASE_DIR,
        "..",
        "assets",
        "Images",
        "enemigos",
        "enemigos_normales",
        f"cliente-{i}.png"
    )

    imagen_enemigo = pygame.image.load(img_enemigo_path).convert_alpha()
    imagen_enemigo = escalar_img(imagen_enemigo, constantes.SCALA_ENEMIGO)
    animaciones_enemigo.append(imagen_enemigo)
enemigo = Enemigo_normal(400, 300, animaciones_enemigo, velocidad=2)

def spawn_enemigo(jugador):
    import random
    lado = random.choice(["top", "bottom", "left", "right"])

    if lado == "top":
        x = random.randint(0, constantes.ANCHO_VENTANA)
        y = -50
    elif lado == "bottom":
        x = random.randint(0, constantes.ANCHO_VENTANA)
        y = constantes.ALTO_VENTANA + 50
    elif lado == "left":
        x = -50
        y = random.randint(0, constantes.ALTO_VENTANA)
    else:
        x = constantes.ANCHO_VENTANA + 50
        y = random.randint(0, constantes.ALTO_VENTANA)

    enemigo = Enemigo_normal(x, y, animaciones_enemigo, velocidad=2)

    enemigo.orientar_hacia(jugador)

    return enemigo

#cocina
animaciones_cocina = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

for i in range(9):
    img_path = os.path.join(
        BASE_DIR,
        "..",
        "assets",
        "Images",
        "characters",
        "Cocina",
        f"Cocina-{i}.png"
    )

    img = pygame.image.load(img_path).convert_alpha()
    img = escalar_img(img, constantes.SCALA_COCINA)

    animaciones_cocina.append(img)


# -------- CREACIÓN DE OBJETOS --------
#Juagdor
jugador = Personaje(300, 250, animaciones) # Ubicacion principal personaje
#Arma
pistola = Weapon(imagen_pistola,imagen_balas)
grupos_balas = pygame.sprite.Group()
#cocina
cocina = Personaje(210, 120, animaciones_cocina)
#Barra de vida 
def dibujar_barra_vida(pantalla, vida_actual, vida_max, x=20, y=20):

    ancho_barra = 200
    alto_barra = 20

    porcentaje = vida_actual / vida_max
    ancho_actual = ancho_barra * porcentaje

    # Fondo gris
    pygame.draw.rect(pantalla, (50, 50, 50), (x, y, ancho_barra, alto_barra))

    # Vida verde
    pygame.draw.rect(pantalla, (0, 255, 0), (x, y, ancho_actual, alto_barra))

    # Borde
    pygame.draw.rect(pantalla, (255, 255, 255), (x, y, ancho_barra, alto_barra), 2)
# -------- GAME LOOP --------

run = True
while run:

    reloj.tick(constantes.FPS)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Movimiento con teclado
    keys = pygame.key.get_pressed()
    dx = 50
    dy = 50
    velocidad = 5
    #Spawn enemigos
    tiempo_actual = pygame.time.get_ticks()

    if tiempo_actual - ultimo_spawn > spawn_cooldown:
        enemigos.append(spawn_enemigo(jugador))
        ultimo_spawn = tiempo_actual

    jugador.update()
    for enemigo in enemigos:
        enemigo.update(jugador)
    bala= pistola.update(jugador)
    if bala:
        grupos_balas.add(bala)
    for bala in grupos_balas:
        bala.update()
    
    screen.fill((30, 30, 30))
    cocina.dibujar(screen)
    for bala in grupos_balas:
        bala.dibujar(screen)
    for enemigo in enemigos:
        enemigo.dibujar(screen)
            # Colisión enemigo vs jugador
        if enemigo.hitbox.colliderect(jugador.hitbox):
            if enemigo.hitbox.colliderect(jugador.hitbox):
                jugador.recibir_dano(enemigo.dano)
    jugador.dibujar(screen)
    
    dibujar_barra_vida(screen, jugador.vida, jugador.vida_max)
    pistola.dibujar(screen)
    pygame.display.update()

pygame.quit()