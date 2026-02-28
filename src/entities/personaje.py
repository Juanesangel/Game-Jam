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
        self.escudo = 0
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
        limite_superior = (wc.HEIGHT // 2)-100
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

    def actualizar_hitbox(self):
        self.hitbox.center = self.rect.center

    def recibir_dano(self, cantidad):
        if self.invulnerable:
            return

        if self.escudo > 0:
            if cantidad <= self.escudo:
                self.escudo -= cantidad
                cantidad = 0
            else:
                cantidad -= self.escudo
                self.escudo = 0

        if cantidad > 0:
            self.vida -= cantidad
            self.vida = max(0, self.vida)

        self.invulnerable = True
        self.tiempo_invulnerable = pygame.time.get_ticks()
    
    
    def dibujar_barra_vida(self, pantalla):
        ancho_barra = 300
        alto_barra = 25
        x = 40
        y = 90

        # Fondo (rojo oscuro)
        pygame.draw.rect(pantalla, (120, 0, 0), (x, y, ancho_barra, alto_barra))

        # Vida actual (verde)
        proporcion = self.vida / self.vida_max
        ancho_vida = ancho_barra * proporcion
        pygame.draw.rect(pantalla, (0, 200, 0), (x, y, ancho_vida, alto_barra))

        # Borde blanco
        pygame.draw.rect(pantalla, (255, 255, 255), (x, y, ancho_barra, alto_barra), 2)