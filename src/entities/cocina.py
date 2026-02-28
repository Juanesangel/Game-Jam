import pygame

class Cocina:
    def __init__(self, x, y, animaciones):
        # --- NUEVA LÓGICA DE ESCALA ---
        self.escala = 2.0  # Cambia este valor para ajustar el tamaño (ej: 2.5, 3.0)
        self.animaciones = []
        
        # Escalamos cada frame de la animación antes de guardarlo
        for img in animaciones:
            nuevo_ancho = int(img.get_width() * self.escala)
            nuevo_alto = int(img.get_height() * self.escala)
            img_escalada = pygame.transform.scale(img, (nuevo_ancho, nuevo_alto))
            self.animaciones.append(img_escalada)
        # ------------------------------

        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frame_index]
        
        # El rect se crea automáticamente con el nuevo tamaño escalado
        self.rect = self.image.get_rect(center=(x, y))
        
        # Ajustamos la hitbox. 
        # Si la imagen ya es grande, quizás no necesites multiplicar por 5.
        # He puesto 1.2 para que sea un poco más grande que la imagen visual.
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 1.2, self.rect.height * 1.2)
        self.hitbox.center = self.rect.center

    def update(self):
        if pygame.time.get_ticks() - self.update_time > 150:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.image = self.animaciones[self.frame_index]
            self.update_time = pygame.time.get_ticks()

    def dibujar(self, surface, show_debug=False):
        surface.blit(self.image, self.rect)
        if show_debug:
            # Dibujamos la hitbox en verde para verificar el área de colisión
            pygame.draw.rect(surface, (0, 255, 0), self.hitbox, 2)