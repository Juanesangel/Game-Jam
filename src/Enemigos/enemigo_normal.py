import pygame
import math

class Enemigo_normal:
    def __init__(self, x, y, animaciones, velocidad=2.0):
        self.animaciones = animaciones
        self.frame = 0.0
        self.pedido = ""  # <--- Definido para evitar error de atributo desconocido

        self.imagen_original = self.animaciones[int(self.frame)]
        self.imagen = self.imagen_original
        self.rect = self.imagen.get_rect(center=(x, y))

        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.6, self.rect.height * 0.6)
        self.hitbox.center = self.rect.center

        self.dano = 10
        self.velocidad = float(velocidad) # <--- Ahora acepta floats como 1.5
        self.angulo = 0.0

    def update(self, jugador):
        direccion = pygame.math.Vector2(
            jugador.rect.centerx - self.rect.centerx,
            jugador.rect.centery - self.rect.centery
        )

        if direccion.length() != 0:
            direccion = direccion.normalize()

        # Usamos int() al asignar al centro para que Pygame no se queje
        nuevo_x = int(self.rect.centerx + direccion.x * self.velocidad)
        nuevo_y = int(self.rect.centery + direccion.y * self.velocidad)
        self.rect.center = (nuevo_x, nuevo_y)
        
        self.angulo = math.degrees(math.atan2(-direccion.y, direccion.x))

        self.frame += 0.1
        if self.frame >= len(self.animaciones):
            self.frame = 0.0

        self.imagen_original = self.animaciones[int(self.frame)]
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo + 255)
        self.rect = self.imagen.get_rect(center=self.rect.center)
        self.hitbox.center = self.rect.center

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)