import pygame

class Personaje:
    def __init__(self, x, y, animaciones):
        # Estados de salud e invulnerabilidad
        self.invulnerable = False
        self.tiempo_invulnerable = 0
        self.cooldown_invulnerable = 1000  # 1 segundo
        
        
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.flip = False
        self.image = self.animaciones[self.frame_index]

        # Rectángulo de imagen (posición en el mundo)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Hitbox (60% del tamaño del sprite, centrada)
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.6, self.rect.height * 0.6)
        self.hitbox.center = self.rect.center

    def movimiento(self, delta_x, delta_y):
        self.rect.x += delta_x
        self.rect.y += delta_y

        if delta_x < 0:
            self.flip = True
        elif delta_x > 0:
            self.flip = False

        self.actualizar_hitbox()

    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        
        # --- Lógica de Animación ---
        cooldown_animacion = 100
        if tiempo_actual - self.update_time >= cooldown_animacion:
            self.frame_index += 1
            self.update_time = tiempo_actual
            if self.frame_index >= len(self.animaciones):
                self.frame_index = 0

        self.image = self.animaciones[self.frame_index]

        # --- Lógica de Invulnerabilidad ---
        if self.invulnerable:
            if tiempo_actual - self.tiempo_invulnerable >= self.cooldown_invulnerable:
                self.invulnerable = False
        
        # Asegurar que la hitbox siempre siga al rect incluso si no hay movimiento
        self.actualizar_hitbox()

    def dibujar(self, pantalla, show_debug=False):
        # Voltear imagen si es necesario
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        
        # Efecto visual de invulnerabilidad (parpadeo opcional)
        if self.invulnerable and (pygame.time.get_ticks() // 100) % 2 == 0:
            pass # Aquí podrías no dibujar o cambiar el alpha si quisieras parpadeo
        else:
            pantalla.blit(imagen_flip, self.rect)
        
        # DIBUJO DE HITBOX SOLO EN MODO DEBUG (Ctrl + F4)
        if show_debug:
            pygame.draw.rect(pantalla, (255, 0, 0), self.hitbox, 2)

    def actualizar_hitbox(self):
        # Mantiene la hitbox proporcional y centrada respecto al rect del personaje
        self.hitbox.center = self.rect.center

    def recibir_dano(self, cantidad):
        tiempo_actual = pygame.time.get_ticks()
        if not self.invulnerable:
            self.vida -= cantidad
            self.invulnerable = True
            self.tiempo_invulnerable = tiempo_actual
            
            