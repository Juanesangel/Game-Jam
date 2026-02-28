import pygame
import random
from config import window_config as w

class Cook(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Definimos dimensiones base (porcentaje del tamaño configurado o tamaño fijo)
        self.width = int(w.WindowConfig.WIDTH * 0.6)
        self.height = int(w.WindowConfig.HEIGHT * 0.4)
        
        # Superficie base
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill((50, 50, 50, 180)) 
        
        # Rectángulo que usaremos como ancla
        self.rect = self.image.get_rect()
        
        # Variables de estado
        self.active = False
        self.timer_duration = 5000  
        self.start_time = 0
        self.lock_timer = 0         
        self.sequence = []
        self.current_step = 0
        
        self.arrow_keys = {
            pygame.K_UP: "↑", pygame.K_DOWN: "↓",
            pygame.K_LEFT: "←", pygame.K_RIGHT: "→"
        }
        self.wasd_keys = {
            pygame.K_w: "W", pygame.K_a: "A",
            pygame.K_s: "S", pygame.K_d: "D"
        }
        self.available_keys = self.arrow_keys.copy()

    def set_timer_duration(self, new_duration: int):
        self.timer_duration = new_duration

    def get_timer(self):
        return self.timer_duration

    def update_difficulty(self, use_wasd=False):
        if use_wasd:
            self.available_keys.update(self.wasd_keys)
        else:
            self.available_keys = self.arrow_keys.copy()

    def initiate_execution(self):
        ahora = pygame.time.get_ticks()
        if ahora >= self.lock_timer:
            self.active = True
            self.current_step = 0
            self.start_time = ahora
            self.sequence = [random.choice(list(self.available_keys.keys())) for _ in range(random.randint(3, 6))]
            return True
        return False

    def cease_execution(self, apply_penalty=False):
        self.active = False
        if apply_penalty:
            self.lock_timer = pygame.time.get_ticks() + 2500

    def handle_input(self, event):
        if self.active and event.type == pygame.KEYDOWN:
            if event.key in self.available_keys:
                if event.key == self.sequence[self.current_step]:
                    self.current_step += 1
                    if self.current_step >= len(self.sequence):
                        self.cease_execution(apply_penalty=False)
                else:
                    self.current_step = 0

    def continue_execution(self, window):
        if not self.active:
            return

        # --- CENTRADO ABSOLUTO OBLIGATORIO ---
        # Obtenemos el rectángulo real de la ventana de Pygame y centramos nuestro self.rect
        pantalla_rect = window.get_rect()
        self.rect.center = pantalla_rect.center

        # 1. Dibujamos el fondo usando nuestra nueva posición calculada
        window.blit(self.image, self.rect)
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)
        
        # 2. Barra de tiempo
        ahora = pygame.time.get_ticks()
        progreso = max(0, (self.timer_duration - (ahora - self.start_time)) / self.timer_duration)
        
        bar_width = self.rect.width - 60
        bar_x = self.rect.left + 30
        bar_y = self.rect.top + 30
        
        pygame.draw.rect(window, (100, 100, 100), (bar_x, bar_y, bar_width, 10))
        color_barra = (0, 255, 150) if progreso > 0.3 else (255, 80, 80)
        pygame.draw.rect(window, color_barra, (bar_x, bar_y, int(bar_width * progreso), 10))

        # 3. Teclas
        fuente = pygame.font.SysFont("Arial", 50, bold=True)
        espaciado = self.rect.width // (len(self.sequence) + 1)
        
        for i, tecla in enumerate(self.sequence):
            pos_x = self.rect.left + espaciado * (i + 1)
            pos_y = self.rect.centery
            
            if i == self.current_step:
                pygame.draw.circle(window, (255, 255, 255), (pos_x, pos_y), 35, 2)

            simbolo = self.available_keys[tecla]
            color = (0, 255, 150) if i < self.current_step else (255, 255, 255)
            txt_surface = fuente.render(simbolo, True, color)
            txt_rect = txt_surface.get_rect(center=(pos_x, pos_y))
            window.blit(txt_surface, txt_rect)