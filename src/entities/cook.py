import pygame
import random
from config import window_config as w

class Cook(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = int(w.WindowConfig.WIDTH * 0.6)
        self.height = int(w.WindowConfig.HEIGHT * 0.4)
        self.scale = int(w.WindowConfig.SCALA_COCINA )
        
        self.image = pygame.Surface((self.width, self.height), self.scale)
        self.image.fill((50, 50, 50, 200)) 
        self.rect = self.image.get_rect()
        
        self.active = False
        self.puntos_pendientes = 0
        self.tipo_comida = "" 
        self.entrega_lista = None  # <--- NUEVO: Almacena qué se terminó de cocinar
        
        self.timer_duration = 5000  # 5 segundos para completar
        self.start_time = 0
        self.lock_until = 0 
        self.sequence = []
        self.current_step = 0
        self.shake_offset: list[float] = [0.0, 0.0]
        
        self.arrow_keys = {pygame.K_UP: "↑", pygame.K_DOWN: "↓", pygame.K_LEFT: "←", pygame.K_RIGHT: "→"}
        self.wasd_keys = {pygame.K_w: "W", pygame.K_a: "A", pygame.K_s: "S", pygame.K_d: "D"}
        self.current_pool = {}

    def initiate_execution(self, modo, dificultad_max):
        ahora = pygame.time.get_ticks()
        if ahora < self.lock_until: return False
        
        self.active = True
        self.puntos_pendientes = 0
        self.entrega_lista = None # Resetear entrega al iniciar
        self.current_step = 0
        self.start_time = ahora
        
        if dificultad_max:
            self.current_pool = {**self.arrow_keys, **self.wasd_keys}
        else:
            self.current_pool = self.arrow_keys if modo == "Empanada" else self.wasd_keys
            
        self.tipo_comida = modo
        self.sequence = [random.choice(list(self.current_pool.keys())) for _ in range(random.randint(3, 5))]
        return True

    def cease_execution(self, apply_penalty=False):
        if not self.active: return
        
        if not apply_penalty:
            self.puntos_pendientes = 1
            self.entrega_lista = self.tipo_comida # Notificamos qué comida está lista
        else:
            self.puntos_pendientes = -1
            self.lock_until = pygame.time.get_ticks() + 2500
            self.entrega_lista = None
            
        self.active = False

    def handle_input(self, event):
        if self.active and event.type == pygame.KEYDOWN:
            if event.key in self.current_pool:
                if event.key == self.sequence[self.current_step]:
                    self.current_step += 1
                    if self.current_step >= len(self.sequence):
                        self.cease_execution(apply_penalty=False)
                else:
                    self.current_step = 0
                    self.shake_offset = [random.randint(-15, 15), random.randint(-15, 15)]

    def continue_execution(self, window):
        if not self.active: return
        
        ahora = pygame.time.get_ticks()
        tiempo_transcurrido = ahora - self.start_time
        
        if tiempo_transcurrido >= self.timer_duration:
            self.cease_execution(apply_penalty=True)
            return

        self.rect.center = window.get_rect().center
        dibujo_rect = self.rect.copy()
        dibujo_rect.x += int(self.shake_offset[0])
        dibujo_rect.y += int(self.shake_offset[1])
        self.shake_offset[0] *= 0.8
        self.shake_offset[1] *= 0.8

        pygame.draw.rect(window, (40, 40, 40, 220), dibujo_rect)
        pygame.draw.rect(window, (255, 255, 255), dibujo_rect, 3)
        
        fuente_tit = pygame.font.SysFont("Arial", 40, bold=True)
        txt_tit = fuente_tit.render(f"PREPARANDO: {self.tipo_comida.upper()}", True, (255, 215, 0))
        window.blit(txt_tit, (dibujo_rect.centerx - txt_tit.get_width()//2, dibujo_rect.top + 30))

        progreso = max(0, (self.timer_duration - tiempo_transcurrido) / self.timer_duration)
        color_barra = (int(255 * (1-progreso)), int(255 * progreso), 0)
        
        pygame.draw.rect(window, (100, 100, 100), (dibujo_rect.left + 50, dibujo_rect.top + 90, (dibujo_rect.width-100), 15))
        pygame.draw.rect(window, color_barra, (dibujo_rect.left + 50, dibujo_rect.top + 90, (dibujo_rect.width-100) * progreso, 15))

        fuente_key = pygame.font.SysFont("Arial", 60, bold=True)
        gap = dibujo_rect.width // (len(self.sequence) + 1)
        for i, k in enumerate(self.sequence):
            color = (0, 255, 100) if i < self.current_step else (255, 255, 255)
            txt = fuente_key.render(self.current_pool[k], True, color)
            window.blit(txt, (dibujo_rect.left + gap*(i+1) - txt.get_width()//2, dibujo_rect.centery))