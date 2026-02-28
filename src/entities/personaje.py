import pygame
from config.window_config import WindowConfig as wc

class Personaje:
    def __init__(self, x, y, animaciones):
        # Estados de salud e invulnerabilidad
        self.invulnerable = False
        self.tiempo_invulnerable = 0
        self.cooldown_invulnerable = 1000 
        self.vida_max = 100
        self.vida = self.vida_max
        self.velocidad = 5
        
        # Animaciones
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.flip = False
        self.image = self.animaciones[self.frame_index]

        # Rectángulo de imagen (posicionado como int)
        self.rect = self.image.get_rect(center=(int(x), int(y)))
        
        # Hitbox (60% del tamaño)
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.6, self.rect.height * 0.6)
        self.hitbox.center = self.rect.center

    def movimiento(self, delta_x, delta_y):
        # Calcular nueva posición
        nueva_x = self.rect.x + delta_x * self.velocidad
        nueva_y = self.rect.y + delta_y * self.velocidad

        # --- LÍMITES (BOUNDARIES) ---
        # No salirse por los lados
        if nueva_x < 0: 
            nueva_x = 0
        elif nueva_x + self.rect.width > wc.WIDTH: 
            nueva_x = wc.WIDTH - self.rect.width

        # No pasar de la MITAD de la pantalla hacia ARRIBA
        # No salirse por el borde INFERIOR
        limite_superior = wc.HEIGHT // 2
        if nueva_y < limite_superior: 
            nueva_y = limite_superior
        elif nueva_y + self.rect.height > wc.HEIGHT: 
            nueva_y = wc.HEIGHT - self.rect.height

        self.rect.x = nueva_x
        self.rect.y = nueva_y
        
        # Orientación
        if delta_x < 0:
            self.flip = True
        elif delta_x > 0:
            self.flip = False
            
        self.actualizar_hitbox()

    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        
        # Animación
        cooldown_animacion = 100
        if tiempo_actual - self.update_time >= cooldown_animacion:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.update_time = tiempo_actual

        self.image = self.animaciones[self.frame_index]

        # Invulnerabilidad
        if self.invulnerable:
            if tiempo_actual - self.tiempo_invulnerable >= self.cooldown_invulnerable:
                self.invulnerable = False
        
        self.actualizar_hitbox()

    def dibujar(self, pantalla, show_debug=False):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        
        # Parpadeo si es invulnerable
        if self.invulnerable and (pygame.time.get_ticks() // 100) % 2 == 0:
            pass 
        else:
            pantalla.blit(imagen_flip, self.rect)
        
        if show_debug:
            pygame.draw.rect(pantalla, (255, 0, 0), self.hitbox, 2)
#hola
    def actualizar_hitbox(self):
        self.hitbox.center = self.rect.center

    def recibir_dano(self, cantidad):
        tiempo_actual = pygame.time.get_ticks()
        if not self.invulnerable:
            self.vida -= cantidad
            self.invulnerable = True
            self.tiempo_invulnerable = tiempo_actual