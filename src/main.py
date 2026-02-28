import pygame
import constantes
from personaje import Personaje
from weapon import Weapon
import os

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



# -------- CREACIÓN DE OBJETOS --------
#Juagdor
jugador = Personaje(50, 50, animaciones)
#Arma
pistola = Weapon(imagen_pistola)


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
    dx = 0
    dy = 0
    velocidad = 5

    if keys[pygame.K_a]:
        dx = -velocidad
    if keys[pygame.K_d]:
        dx = velocidad
    if keys[pygame.K_w]:
        dy = -velocidad
    if keys[pygame.K_s]:
        dy = velocidad

    jugador.movimiento(dx, dy)
    jugador.update()
    pistola.update(jugador)
    screen.fill((30, 30, 30))
    jugador.dibujar(screen)
    pistola.dibujar(screen)

    pygame.display.update()

pygame.quit()