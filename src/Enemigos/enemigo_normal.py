import pygame
import math
import random

class Enemigo_normal:
    def __init__(self, x, y, animaciones, velocidad=1.5):
        self.animaciones = animaciones
        self.frame = 0.0
        # Asignar pedido aleatorio si no tiene uno
        self.pedido = random.choice(["Arepa", "Empanada"])

        self.imagen_original = self.animaciones[int(self.frame)]
        self.imagen = self.imagen_original
        
        # Posición en float para movimiento suave
        self.pos_x = float(x)
        self.pos_y = float(y)
        
        self.rect = self.imagen.get_rect(center=(int(self.pos_x), int(self.pos_y)))

        # Hitbox optimizada (60% del tamaño visual)
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.6, self.rect.height * 0.6)
        self.hitbox.center = self.rect.center

        self.velocidad = float(velocidad)
        self.angulo = 0.0
        
        # Fuente para el tag del pedido
        self.fuente_tag = pygame.font.SysFont("Arial", 20, bold=True)

    def update(self, jugador):
        # Calcular vector hacia el jugador
        direccion = pygame.math.Vector2(
            jugador.rect.centerx - self.pos_x,
            jugador.rect.centery - self.pos_y
        )

        if direccion.length() != 0:
            direccion = direccion.normalize()

        # Movimiento fluido
        self.pos_x += direccion.x * self.velocidad
        self.pos_y += direccion.y * self.velocidad
        
        # Actualizar rectangulo de colisión visual
        self.rect.center = (int(self.pos_x), int(self.pos_y))
        
        # Rotación hacia el objetivo
        self.angulo = math.degrees(math.atan2(-direccion.y, direccion.x))

        # Animación
        self.frame = (self.frame + 0.1) % len(self.animaciones)
        self.imagen_original = self.animaciones[int(self.frame)]
        
        # Aplicar rotación (ajuste de +255 según tus assets)
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo + 255)
        self.rect = self.imagen.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        
        # Sincronizar hitbox
        self.hitbox.center = self.rect.center

    def dibujar(self, pantalla, show_debug=False):
        # Dibujar Sprite
        pantalla.blit(self.imagen, self.rect)
        
        # Dibujar TAG de pedido
        color_texto = (255, 215, 0) if self.pedido == "Arepa" else (0, 255, 127)
        txt_surface = self.fuente_tag.render(self.pedido, True, color_texto)
        pos_texto = (self.rect.centerx - txt_surface.get_width() // 2, self.rect.top - 25)
        pantalla.blit(txt_surface, pos_texto)
        
        # Debug
        if show_debug:
            pygame.draw.rect(pantalla, (0, 0, 255), self.hitbox, 2)