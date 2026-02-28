import pygame
import random
from config import window_config as w

class Cook(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = int(w.WindowConfig.WIDTH * 0.6)
        self.height = int(w.WindowConfig.HEIGHT * 0.4)
        self.rect = pygame.Rect(0,0, self.width, self.height)
        
        self.active = False
        self.puntos_pendientes = 0
        self.tipo_comida = "" 
        self.entrega_lista = None # Variable clave para eliminar enemigos
        
        self.timer_duration = 5000
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
        
        self.active, self.current_step, self.start_time = True, 0, ahora
        self.tipo_comida, self.entrega_lista = modo, None
        
        self.current_pool = {**self.arrow_keys, **self.wasd_keys} if dificultad_max else (self.arrow_keys if modo == "Empanada" else self.wasd_keys)
        self.sequence = [random.choice(list(self.current_pool.keys())) for _ in range(random.randint(3, 5))]
        return True

    def cease_execution(self, apply_penalty=False):
        if not self.active: return
        if not apply_penalty:
            self.puntos_pendientes = 1
            self.entrega_lista = self.tipo_comida # Avisa qué comida se terminó
        else:
            self.puntos_pendientes = -1
            self.lock_until = pygame.time.get_ticks() + 2500
        self.active = False

    def handle_input(self, event):
        if self.active and event.type == pygame.KEYDOWN:
            if event.key in self.current_pool:
                if event.key == self.sequence[self.current_step]:
                    self.current_step += 1
                    if self.current_step >= len(self.sequence): self.cease_execution(False)
                else:
                    self.current_step = 0
                    self.shake_offset = [random.randint(-15, 15), random.randint(-15, 15)]

    def continue_execution(self, window):
        if not self.active: return
        ahora = pygame.time.get_ticks()
        if ahora - self.start_time >= self.timer_duration:
            self.cease_execution(True); return

        self.rect.center = window.get_rect().center
        dr = self.rect.copy()
        dr.x += int(self.shake_offset[0]); dr.y += int(self.shake_offset[1])
        self.shake_offset[0] *= 0.8; self.shake_offset[1] *= 0.8

        pygame.draw.rect(window, (40, 40, 40, 220), dr)
        pygame.draw.rect(window, (255, 255, 255), dr, 3)
        
        txt = pygame.font.SysFont("Arial", 40, bold=True).render(f"PREPARANDO: {self.tipo_comida.upper()}", True, (255, 215, 0))
        window.blit(txt, (dr.centerx - txt.get_width()//2, dr.top + 30))

        prog = max(0, (self.timer_duration - (ahora - self.start_time)) / self.timer_duration)
        pygame.draw.rect(window, (100, 100, 100), (dr.left + 50, dr.top + 90, dr.width-100, 15))
        pygame.draw.rect(window, (int(255*(1-prog)), int(255*prog), 0), (dr.left + 50, dr.top + 90, (dr.width-100)*prog, 15))

        f_key = pygame.font.SysFont("Arial", 60, bold=True)
        gap = dr.width // (len(self.sequence) + 1)
        for i, k in enumerate(self.sequence):
            col = (0, 255, 100) if i < self.current_step else (255, 255, 255)
            t_key = f_key.render(self.current_pool[k], True, col)
            window.blit(t_key, (dr.left + gap*(i+1) - t_key.get_width()//2, dr.centery))