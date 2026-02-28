import pygame

class Personaje:
    def __init__(self, x, y, animaciones):

        self.invulnerable = False
        self.tiempo_invulnerable = 0
        self.cooldown_invulnerable = 1000  # 1 segundo
        
        
        self.animaciones = animaciones
        self.frame_index = 3
        self.update_time = pygame.time.get_ticks()
        self.flip = False

        self.vida_max = 100
        self.vida = self.vida_max

        self.image = self.animaciones[self.frame_index]

        # Rect de imagen
        self.rect = self.image.get_rect(topleft=(x, y))

        #Hitbox más pequeña y centrada
        self.hitbox = pygame.Rect(270, 200, self.rect.width * 0.5, self.rect.height * 0.5)

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
        tiempo_actual = pygame.time.get_ticks()

        if self.invulnerable:
            if tiempo_actual - self.tiempo_invulnerable >= self.cooldown_invulnerable:
                self.invulnerable = False

    def dibujar(self, pantalla):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        pantalla.blit(imagen_flip, self.rect)
        pygame.draw.rect(pantalla, (255, 0, 0), self.hitbox, 1)


    def recibir_dano(self, cantidad):

        tiempo_actual = pygame.time.get_ticks()

        if not self.invulnerable:
            self.vida -= cantidad
            self.invulnerable = True
            self.tiempo_invulnerable = tiempo_actual