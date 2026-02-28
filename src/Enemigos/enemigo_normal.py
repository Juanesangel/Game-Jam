import pygame
import math
import random

class Enemigo_normal:
    def __init__(self, x, y, animaciones, velocidad=1.5):
        self.animaciones = animaciones
        self.frame = 0.0
        self.pedido = random.choice(["Arepa", "Empanada"])
        self.imagen_original = self.animaciones[int(self.frame)]
        self.imagen = self.imagen_original
        
        self.pos_x = float(x)
        self.pos_y = float(y)
        
        # Rect usando enteros para evitar errores
        self.rect = self.imagen.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.6, self.rect.height * 0.6)
        self.hitbox.center = self.rect.center

        self.velocidad = float(velocidad)
        self.angulo = 0.0
        self.fuente_tag = pygame.font.SysFont("Arial", 20, bold=True)

    def update(self, jugador):
        
        # Calcular dirección hacia el jugador
        dx = jugador.rect.centerx - self.pos_x
        dy = jugador.rect.centery - self.pos_y
        distancia = math.hypot(dx, dy)

        if distancia != 0:
            self.pos_x += (dx / distancia) * self.velocidad
            self.pos_y += (dy / distancia) * self.velocidad
        
        self.angulo = math.degrees(math.atan2(-dy, dx))
        self.frame = (self.frame + 0.1) % len(self.animaciones)
        self.imagen_original = self.animaciones[int(self.frame)]
        
        # Rotación y actualización de rect con enteros
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo + 255)
        self.rect = self.imagen.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        self.hitbox.center = self.rect.center

    def dibujar(self, pantalla, show_debug=False):
        pantalla.blit(self.imagen, self.rect)
        color_texto = (255, 215, 0) if self.pedido == "Arepa" else (0, 255, 127)
        txt_surface = self.fuente_tag.render(self.pedido, True, color_texto)
        pos_texto = (self.rect.centerx - txt_surface.get_width() // 2, self.rect.top - 25)
        pantalla.blit(txt_surface, pos_texto)
        if show_debug:
            pygame.draw.rect(pantalla, (0, 0, 255), self.hitbox, 2)