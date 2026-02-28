import pygame

class Cocina:
    def __init__(self, x, y, animaciones):
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 1.5, self.rect.height * 1.5)
        self.hitbox.center = self.rect.center

    def update(self):
        if pygame.time.get_ticks() - self.update_time > 150:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.image = self.animaciones[self.frame_index]
            self.update_time = pygame.time.get_ticks()

    def dibujar(self, surface, show_debug=False):
        surface.blit(self.image, self.rect)
        if show_debug:
            pygame.draw.rect(surface, (0, 255, 0), self.hitbox, 2)