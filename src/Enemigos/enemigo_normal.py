import pygame
import math

class Enemigo_normal:
    def __init__(self, x, y, animaciones, velocidad=2):
        self.animaciones = animaciones
        self.frame = 0

        self.imagen_original = self.animaciones[self.frame]
        self.imagen = self.imagen_original

        self.rect = self.imagen.get_rect(center=(x, y))
        self.velocidad = velocidad
        self.angulo = 0

    def update(self, jugador):

        # --- Calcular dirección ---
        direccion = pygame.math.Vector2(
            jugador.rect.centerx - self.rect.centerx,
            jugador.rect.centery - self.rect.centery
        )

        if direccion.length() != 0:
            direccion = direccion.normalize()

        # --- Movimiento ---
        nuevo_x = self.rect.centerx + direccion.x * self.velocidad
        nuevo_y = self.rect.centery + direccion.y * self.velocidad
        self.rect = self.imagen.get_rect(center=(nuevo_x, nuevo_y))        
        # --- Calcular ángulo ---
        self.angulo = math.degrees(math.atan2(-direccion.y, direccion.x))

        # --- Animación ---
        self.frame += 0.1
        if self.frame >= len(self.animaciones):
            self.frame = 0

        self.imagen_original = self.animaciones[int(self.frame)]

        # --- Rotar imagen ---
        angulo_ajustado = self.angulo + 255

        self.imagen = pygame.transform.rotate(self.imagen_original, angulo_ajustado)
        # Mantener el centro
        self.rect = self.imagen.get_rect(center=self.rect.center)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
    import math

    def orientar_hacia(self, jugador):
        direccion = pygame.math.Vector2(
            jugador.rect.centerx - self.rect.centerx,
            jugador.rect.centery - self.rect.centery
        )

        if direccion.length() != 0:
            direccion = direccion.normalize()

        angulo = math.degrees(math.atan2(-direccion.y, direccion.x))

        centro = self.rect.center

        self.imagen = pygame.transform.rotate(self.imagen_original, angulo)
        self.rect = self.imagen.get_rect(center=centro)