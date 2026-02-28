import pygame
import constantes
import math
class Weapon():
    def __init__(self, image, imagen_bala):
        self.imagen_bala=imagen_bala
        self.imagen_original = image
        self.angulo = 0
        self.imagen = self.imagen_original
        self.rect = self.imagen.get_rect()

    def update(self, personaje):

        BALA= None
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
        # vector desde el centro hacia el "mango"
        pivot_offset = pygame.math.Vector2(0.1, -39)
        # rotar ese vector
        rotated_offset = pivot_offset.rotate(-self.angulo)
        # nueva posición final
        nueva_pos = base_pos + rotated_offset
        # crear rect centrado en nueva posición
        self.rect = self.imagen.get_rect(center=nueva_pos)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    #DETECTAR EL MOVIMIENTO 
    #if.hace e comando pedido lanza la empanada and+= False.
        #bala=Bullet(self.imagen_bala,self.personaje.en x y y self. angle)
        #self.dispara= True
        #return bala
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle, damage=10):
        super().__init__()

        self.imagen_original = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect(center=(x, y))

        self.damage = damage

        self.velocidad = constantes.VELOCIDAD_BALAS

        # Vector de movimiento
        self.delta_x = math.cos(math.radians(self.angulo)) * self.velocidad
        self.delta_y = -math.sin(math.radians(self.angulo)) * self.velocidad
        
    def update(self):
        self.rect = self.rect.move(self.delta_x, self.delta_y)

        # Si sale de pantalla, se elimina
        if (
            self.rect.right < 0
            or self.rect.left > constantes.ANCHO_VENTANA
            or self.rect.bottom < 0
            or self.rect.top > constantes.ALTO_VENTANA
        ):
            self.kill()
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        