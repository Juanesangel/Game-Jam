import pygame
import random
from config import window_config as w

class Cook(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = int(w.WindowConfig.WIDTH * 0.6)
        self.height = int(w.WindowConfig.HEIGHT * 0.4)
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill((50, 50, 50, 200)) 
        self.rect = self.image.get_rect()
        
        # Variables de estado y Puntuación
        self.active = False
        self.success = False
        self.puntos_pendientes = 0  # <--- CLAVE: 1 (ganó), -1 (perdió), 0 (nada)
        
        self.timer_duration = 5000  
        self.start_time = 0
        self.lock_timer = 0         
        self.sequence = []
        self.current_step = 0
        
        # Efectos visuales
        self.shake_offset: list[float] = [0, 0]
        
        self.arrow_keys = {
            pygame.K_UP: "↑", pygame.K_DOWN: "↓",
            pygame.K_LEFT: "←", pygame.K_RIGHT: "→"
        }
        self.wasd_keys = {
            pygame.K_w: "W", pygame.K_a: "A",
            pygame.K_s: "S", pygame.K_d: "D"
        }
        self.available_keys = self.arrow_keys.copy()

    def update_difficulty(self, use_wasd=False):
        if use_wasd:
            self.available_keys.update(self.wasd_keys)
        else:
            self.available_keys = self.arrow_keys.copy()

    def get_timer(self):
        return self.timer_duration

    def initiate_execution(self):
        ahora = pygame.time.get_ticks()
        if ahora >= self.lock_timer:
            self.active = True
            self.success = False
            self.puntos_pendientes = 0 # Limpiamos cualquier punto previo
            self.current_step = 0
            self.start_time = ahora
            self.sequence = [random.choice(list(self.available_keys.keys())) for _ in range(random.randint(3, 6))]
            return True
        return False

    def cease_execution(self, apply_penalty=False):
        if not self.active: return # Seguridad para no ejecutar doble
        
        self.active = False
        self.success = not apply_penalty 
        
        # Seteamos el punto para que el main lo recoja
        if self.success:
            self.puntos_pendientes = 1
        else:
            self.puntos_pendientes = -1
            self.lock_timer = pygame.time.get_ticks() + 2500

    def handle_input(self, event):
        if self.active and event.type == pygame.KEYDOWN:
            if event.key in self.available_keys:
                if event.key == self.sequence[self.current_step]:
                    self.current_step += 1
                    if self.current_step >= len(self.sequence):
                        self.cease_execution(apply_penalty=False)
                else:
                    # FALLO DE TECLA: Sacudida y reinicio de secuencia
                    self.current_step = 0
                    self.shake_offset = [random.randint(-15, 15), random.randint(-15, 15)]

    def continue_execution(self, window):
        if not self.active:
            return

        pantalla_rect = window.get_rect()
        self.rect.center = pantalla_rect.center
        
        # Aplicar sacudida al dibujo
        dibujo_rect = self.rect.copy()
        dibujo_rect.x += int(self.shake_offset[0])
        dibujo_rect.y += int(self.shake_offset[1])
        
        # Reducir sacudida gradualmente (amortiguación)
        self.shake_offset[0] *= 0.8
        self.shake_offset[1] *= 0.8

        # 1. Fondo
        window.blit(self.image, dibujo_rect)
        pygame.draw.rect(window, (255, 255, 255), dibujo_rect, 2)
        
        # 2. Barra de tiempo
        ahora = pygame.time.get_ticks()
        progreso = max(0, (self.timer_duration - (ahora - self.start_time)) / self.timer_duration)
        
        bar_width = self.rect.width - 60
        bar_x = dibujo_rect.left + 30
        bar_y = dibujo_rect.top + 30
        
        pygame.draw.rect(window, (100, 100, 100), (bar_x, bar_y, bar_width, 12))
        color_barra = (0, 255, 150) if progreso > 0.3 else (255, 80, 80)
        pygame.draw.rect(window, color_barra, (bar_x, bar_y, int(bar_width * progreso), 12))

        # 3. Teclas
        fuente = pygame.font.SysFont("Arial", 55, bold=True)
        espaciado = self.rect.width // (len(self.sequence) + 1)
        
        for i, tecla in enumerate(self.sequence):
            pos_x = dibujo_rect.left + espaciado * (i + 1)
            pos_y = dibujo_rect.centery
            
            if i == self.current_step:
                pygame.draw.circle(window, (255, 255, 255), (pos_x, pos_y), 38, 2)

            simbolo = self.available_keys[tecla]
            color = (0, 255, 150) if i < self.current_step else (255, 255, 255)
            txt_surface = fuente.render(simbolo, True, color)
            txt_rect = txt_surface.get_rect(center=(pos_x, pos_y))
            window.blit(txt_surface, txt_rect)