import pygame
import constantes
class Weapon():
    def __init__(self, image):
        self.imagen_original = image
        self.angulo = 0
        self.imagen = self.imagen_original
        self.rect = self.imagen.get_rect()

def update(self, personaje):

    offset_x = 30
    offset_y = 10

    if personaje.flip:
        offset_x = -30

    # punto base en el personaje
    base_pos = pygame.math.Vector2(
        personaje.rect.centerx + offset_x,
        personaje.rect.centery + offset_y
    )
    # rotación
    self.angulo += 2
    # vector desde el centro hacia el "mango"
    pivot_offset = pygame.math.Vector2(-20, 0)
    # rotar ese vector
    rotated_offset = pivot_offset.rotate(-self.angulo)
    # nueva posición final
    nueva_pos = base_pos + rotated_offset
    # rotar imagen
    self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
    # crear rect centrado en nueva posición
    self.rect = self.imagen.get_rect(center=nueva_pos)

def dibujar(self, pantalla):
    pantalla.blit(self.imagen, self.rect)
    pygame.draw.rect(pantalla,constantes.COLOR_ARMA, self.rect,1)
        