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
        
        # --- LÓGICA DE ANIMACIÓN DE ICONOS ---
        self.frames_icono = []
        self.frame_icono_actual = 0.0
        self.anim_speed_icono = 0.1  # Ajusta la velocidad del loop del icono
        
        base_path = os.path.join("assets", "Images", "iconos")
        folder = "arepa" if self.pedido == "Arepa" else "empanada"
        path_dir = os.path.join(base_path, folder)

        if os.path.exists(path_dir):
            # Cargamos y escalamos todas las imágenes de la carpeta para la animación
            archivos = sorted([f for f in os.listdir(path_dir) if f.endswith('.png')])
            for nombre_archivo in archivos:
                img = pygame.image.load(os.path.join(path_dir, nombre_archivo)).convert_alpha()
                # Reescalado a 35x35 (puedes ajustar el tamaño aquí)
                img_escalada = pygame.transform.scale(img, (35, 35))
                self.frames_icono.append(img_escalada)
        # ---------------------------------------

        self.pos_x = float(x)
        self.pos_y = float(y)
        
        self.rect = self.imagen.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.6, self.rect.height * 0.6)
        self.hitbox.center = self.rect.center

        self.velocidad = float(velocidad)
        self.angulo = 0.0

    def update(self, jugador):
        # Movimiento hacia el jugador
        dx = jugador.rect.centerx - self.pos_x
        dy = jugador.rect.centery - self.pos_y
        distancia = math.hypot(dx, dy)

        if distancia != 0:
            self.pos_x += (dx / distancia) * self.velocidad
            self.pos_y += (dy / distancia) * self.velocidad
        
        # Actualización de animación del enemigo
        self.angulo = math.degrees(math.atan2(-dy, dx))
        self.frame = (self.frame + 0.1) % len(self.animaciones)
        self.imagen_original = self.animaciones[int(self.frame)]
        
        # --- ACTUALIZACIÓN DEL LOOP DEL ICONO ---
        if self.frames_icono:
            self.frame_icono_actual = (self.frame_icono_actual + self.anim_speed_icono) % len(self.frames_icono)
        # -----------------------------------------

        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo + 255)
        self.rect = self.imagen.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        self.hitbox.center = self.rect.center

    def dibujar(self, pantalla, show_debug=False):
        pantalla.blit(self.imagen, self.rect)
        
        # --- DIBUJAR EL FRAME ACTUAL DEL ICONO ---
        if self.frames_icono:
            img_icono = self.frames_icono[int(self.frame_icono_actual)]
            # Lo posicionamos un poco más arriba y centrado
            pos_icono = (self.rect.centerx - img_icono.get_width() // 2, self.rect.top - 40)
            pantalla.blit(img_icono, pos_icono)
        # ------------------------------------------

        if show_debug:
            pygame.draw.rect(pantalla, (0, 0, 255), self.hitbox, 2)