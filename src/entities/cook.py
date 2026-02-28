import pygame
import random
import os

class Cook:
    def __init__(self):
        self.active = False
        self.recipe_name = ""
        self.sequence = []
        self.current_step = 0
        self.puntos_pendientes = 0
        self.entrega_lista = None
        self.lock_until = 0
        
        # Variables del Timer
        self.timer = 0
        self.timer_limit = 0
        
        self.base_path = os.path.join("assets", "Images", "flechas")
        
        try:
            self.img_blanca = pygame.image.load(os.path.join(self.base_path, "flecha_blanca.png")).convert_alpha()
            self.img_verde = pygame.image.load(os.path.join(self.base_path, "flecha_verde.png")).convert_alpha()
            
            self.size = (50, 50)
            # CORRECCIÓN: Uso de transform.scale en lugar de image.scale
            self.img_blanca = pygame.transform.scale(self.img_blanca, self.size)
            self.img_verde = pygame.transform.scale(self.img_verde, self.size)
        except Exception as e:
            print(f"Error cargando flechas: {e}")
            self.img_blanca = pygame.Surface((50, 50))
            self.img_blanca.fill((200, 200, 200))
            self.img_verde = pygame.Surface((50, 50))
            self.img_verde.fill((0, 255, 0))

        self.rotaciones = {"RIGHT": 0, "UP": 90, "LEFT": 180, "DOWN": 270}

    def initiate_execution(self, name, hard_mode=False):
        self.active = True
        self.recipe_name = name
        self.current_step = 0
        self.entrega_lista = None
        self.lock_until = 0 
        
        length = 5 if hard_mode else 3
        self.sequence = [random.choice(["UP", "DOWN", "LEFT", "RIGHT"]) for _ in range(length)]
        
        # Timer: 4s en difícil, 6s en normal
        self.timer_limit = 4000 if hard_mode else 6000
        self.timer = pygame.time.get_ticks() + self.timer_limit

    def handle_input(self, event):
        if not self.active or event.type != pygame.KEYDOWN:
            return

        key_map = {
            pygame.K_UP: "UP", pygame.K_DOWN: "DOWN", pygame.K_LEFT: "LEFT", pygame.K_RIGHT: "RIGHT",
            pygame.K_w: "UP", pygame.K_s: "DOWN", pygame.K_a: "LEFT", pygame.K_d: "RIGHT"
        }

        if event.key in key_map:
            if key_map[event.key] == self.sequence[self.current_step]:
                self.current_step += 1
                if self.current_step >= len(self.sequence):
                    self.active = False
                    self.entrega_lista = self.recipe_name
                    self.puntos_pendientes = 1 
                    self.lock_until = 0 # Sin bloqueo si ganas
            else:
                self.current_step = 0

    def continue_execution(self, surface):
        if not self.active:
            return

        ahora = pygame.time.get_ticks()
        tiempo_restante = self.timer - ahora

        # Si falla el timer: bloquear cocina
        if tiempo_restante <= 0:
            self.active = False
            self.lock_until = ahora + 3000 # Bloqueo por error
            return

        # Dibujo del interfaz del minijuego
        overlay = pygame.Surface((surface.get_width(), 140), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, surface.get_height() // 2 - 70))

        # Barra de tiempo visual
        ancho_barra = 200
        pct = max(0, tiempo_restante / self.timer_limit)
        pygame.draw.rect(surface, (100, 100, 100), (surface.get_width()//2 - ancho_barra//2, surface.get_height()//2 + 45, ancho_barra, 10))
        pygame.draw.rect(surface, (255, 0, 0), (surface.get_width()//2 - ancho_barra//2, surface.get_height()//2 + 45, int(ancho_barra * pct), 10))

        espaciado = 20
        total_width = len(self.sequence) * (50 + espaciado) - espaciado
        start_x = (surface.get_width() - total_width) // 2
        y_pos = surface.get_height() // 2 - 25

        for i, direction in enumerate(self.sequence):
            base_img = self.img_verde if i < self.current_step else self.img_blanca
            img_rotada = pygame.transform.rotate(base_img, self.rotaciones[direction])
            rect_rotado = img_rotada.get_rect(center=(start_x + i * (50 + espaciado) + 25, y_pos + 25))
            surface.blit(img_rotada, rect_rotado)

        font = pygame.font.SysFont("Arial", 28, bold=True)
        txt = font.render(f"PREPARANDO: {self.recipe_name.upper()}", True, (255, 255, 255))
        surface.blit(txt, (surface.get_width() // 2 - txt.get_width() // 2, y_pos - 50))