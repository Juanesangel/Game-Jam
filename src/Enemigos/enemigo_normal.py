import pygame
import math
import random
import os

class Enemigo_normal:
    def __init__(self, x, y, animaciones, velocidad=1.0):
        self.animaciones = animaciones
        self.frame = 0.0
        self.pedido = random.choice(["Arepa", "Empanada"])
        self.imagen_original = self.animaciones[int(self.frame)]
        self.imagen = self.imagen_original
        
        # --- NUEVA LÓGICA DE ICONOS ---
        # Definir la ruta base de los iconos
        base_path = os.path.join("assets", "Images", "iconos")
        # Seleccionar la carpeta según el pedido
        folder = "arepa" if self.pedido == "Arepa" else "empanada"
        icon_path = os.path.join(base_path, folder)
        
        # Cargar el primer archivo .png que encuentre en la carpeta
        self.icono = None
        if os.path.exists(icon_path):
            archivos = [f for f in os.listdir(icon_path) if f.endswith('.png')]
            if archivos:
                img_path = os.path.join(icon_path, archivos[0])
                raw_icon = pygame.image.load(img_path).convert_alpha()
                # Reescalar el icono a un tamaño pequeño (ejemplo 30x30)
                self.icono = pygame.transform.scale(raw_icon, (30, 30))
        # ------------------------------

        self.pos_x = float(x)
        self.pos_y = float(y)
        
        self.rect = self.imagen.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.6, self.rect.height * 0.6)
        self.hitbox.center = self.rect.center

        self.velocidad = float(velocidad)
        self.angulo = 0.0
        # Mantengo la fuente por si acaso, aunque ya no se use para el tag principal
        self.fuente_tag = pygame.font.SysFont("Arial", 20, bold=True)

    def update(self, jugador):
        dx = jugador.rect.centerx - self.pos_x
        dy = jugador.rect.centery - self.pos_y
        distancia = math.hypot(dx, dy)

        if distancia != 0:
            self.pos_x += (dx / distancia) * self.velocidad
            self.pos_y += (dy / distancia) * self.velocidad
        
        self.angulo = math.degrees(math.atan2(-dy, dx))
        self.frame = (self.frame + 0.1) % len(self.animaciones)
        self.imagen_original = self.animaciones[int(self.frame)]
        
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo + 255)
        self.rect = self.imagen.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        self.hitbox.center = self.rect.center

    def dibujar(self, pantalla, show_debug=False):
        pantalla.blit(self.imagen, self.rect)
        
        # --- DIBUJAR ICONO EN LUGAR DE TEXTO ---
        if self.icono:
            # Posicionar el icono arriba de la cabeza del enemigo
            pos_icono = (self.rect.centerx - self.icono.get_width() // 2, self.rect.top - 35)
            pantalla.blit(self.icono, pos_icono)
        # ---------------------------------------

        if show_debug:
            pygame.draw.rect(pantalla, (0, 0, 255), self.hitbox, 2)