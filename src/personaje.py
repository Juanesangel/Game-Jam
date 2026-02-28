import pygame

class Personaje:
    def __init__(self, x, y, animaciones):
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.flip = False

        self.image = self.animaciones[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

    def movimiento(self, delta_x, delta_y):
        self.rect.x += delta_x
        self.rect.y += delta_y

        if delta_x < 0:
            self.flip = True
        elif delta_x > 0:
            self.flip = False

    def update(self):
        cooldown_animacion = 100
        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.update_time >= cooldown_animacion:
            self.frame_index += 1
            self.update_time = tiempo_actual

            if self.frame_index >= len(self.animaciones):
                self.frame_index = 0

        self.image = self.animaciones[self.frame_index]

    def dibujar(self, pantalla):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        pantalla.blit(imagen_flip, self.rect)