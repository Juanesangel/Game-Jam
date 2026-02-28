import pygame

class Cocina:
    def __init__(self, x, y, animaciones):
        # 1. Ajuste de escala: Escalamos las imágenes recibidas
        # Subimos a 1.8 para un tamaño considerable en pantalla
        self.escala = 1.8 
        self.animaciones = [
            pygame.transform.scale(img, (int(img.get_width() * self.escala), int(img.get_height() * self.escala))) 
            for img in animaciones
        ]
        
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.flip = False

        self.image = self.animaciones[self.frame_index]
        # Posicionamos usando el centro para que no se desplace al escalar
        self.rect = self.image.get_rect(center=(x, y))

        # 2. Hitbox: Inflamos el área para facilitar la interacción
        self.hitbox = self.rect.inflate(20, 20) 

    def update(self):
        cooldown_animacion = 150 
        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.update_time >= cooldown_animacion:
            self.frame_index += 1
            self.update_time = tiempo_actual
            if self.frame_index >= len(self.animaciones):
                self.frame_index = 0

        self.image = self.animaciones[self.frame_index]
        self.hitbox.center = self.rect.center

    def dibujar(self, pantalla, show_debug=False):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        pantalla.blit(imagen_flip, self.rect)
        
        # DEBUG: Solo se muestra con Ctrl + F4
        if show_debug:
            pygame.draw.rect(pantalla, (0, 255, 0), self.hitbox, 2)