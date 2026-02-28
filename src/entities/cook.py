import pygame
import random
from config import window_config as w

class Cook(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 1. Configuración de dimensiones y superficie
        # Usamos el Enum inicializado para el tamaño
        width = w.WindowConfig.WIDTH.value // 2
        height = w.WindowConfig.HEIGHT.value // 2
        
        # Superficie con SRCALPHA para permitir transparencia
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((50, 50, 50, 180)) # Gris oscuro con alpha
        
        self.rect = self.image.get_rect()
        self.rect.center = (w.WindowConfig.WIDTH.value // 2, w.WindowConfig.HEIGHT.value // 2)
        
        # 2. Variables de estado del Minijuego
        self.active = False
        self.timer_duration = 5000  # 5 segundos iniciales
        self.start_time = 0
        self.lock_timer = 0         # Tiempo de penalización
        
        # 3. Lógica de Secuencias
        self.sequence = []
        self.current_step = 0
        
        # Diccionarios de teclas y símbolos
        self.arrow_keys = {
            pygame.K_UP: "↑", pygame.K_DOWN: "↓",
            pygame.K_LEFT: "←", pygame.K_RIGHT: "→"
        }
        self.wasd_keys = {
            pygame.K_w: "W", pygame.K_a: "A",
            pygame.K_s: "S", pygame.K_d: "D"
        }
        
        # Pool de teclas actual (inicia solo con flechas)
        self.available_keys = self.arrow_keys.copy()

    def set_timer_duration(self, new_duration: int):
        """Ajusta la dificultad cambiando la duración del timer."""
        self.timer_duration = new_duration

    def get_timer(self):
        """Retorna la duración actual seteada."""
        return self.timer_duration

    def update_difficulty(self, use_wasd=False):
        """Añade o quita las teclas WASD del juego."""
        if use_wasd:
            self.available_keys.update(self.wasd_keys)
        else:
            self.available_keys = self.arrow_keys.copy()

    def initiate_execution(self):
        """Arranca el minijuego si no hay penalización activa."""
        ahora = pygame.time.get_ticks()
        if ahora >= self.lock_timer:
            self.active = True
            self.current_step = 0
            self.start_time = ahora
            # Generar secuencia de 3 a 6 teclas del pool disponible
            self.sequence = [random.choice(list(self.available_keys.keys())) for _ in range(random.randint(3, 6))]
            return True
        return False

    def cease_execution(self, apply_penalty=False):
        """Finaliza el minijuego y aplica bloqueo si es necesario."""
        self.active = False
        if apply_penalty:
            # Bloqueo de 2.5 segundos
            self.lock_timer = pygame.time.get_ticks() + 2500

    def handle_input(self, event):
        """Procesa las pulsaciones de teclas del usuario."""
        if self.active and event.type == pygame.KEYDOWN:
            if event.key in self.available_keys:
                # Verificar si la tecla coincide con el paso actual de la secuencia
                if event.key == self.sequence[self.current_step]:
                    self.current_step += 1
                    # Victoria: se completaron todas las teclas
                    if self.current_step >= len(self.sequence):
                        self.cease_execution(apply_penalty=False)
                else:
                    # Error: Reinicia el progreso de la serie actual
                    self.current_step = 0

    def continue_execution(self, window):
        """Dibuja los elementos visuales del minijuego en la ventana."""
        if not self.active:
            return

        # 1. Dibujar el fondo del sprite
        window.blit(self.image, self.rect)
        
        # 2. Cálculo y dibujo de la Barra de Tiempo
        ahora = pygame.time.get_ticks()
        tiempo_pasado = ahora - self.start_time
        progreso = max(0, (self.timer_duration - tiempo_pasado) / self.timer_duration)
        
        # Contenedor de la barra
        bar_x = self.rect.left + 30
        bar_y = self.rect.top + 30
        bar_width = self.rect.width - 60
        
        pygame.draw.rect(window, (80, 0, 0), (bar_x, bar_y, bar_width, 12)) # Fondo barra
        color_barra = (0, 255, 100) if progreso > 0.3 else (255, 50, 50)
        pygame.draw.rect(window, color_barra, (bar_x, bar_y, bar_width * progreso, 12))

        # 3. Dibujar las Teclas de la Secuencia
        # Usamos una fuente del sistema que soporte flechas (como Segoe UI Symbol en Windows)
        fuente = pygame.font.SysFont("Arial", 50, bold=True)
        
        # Calculamos el espacio para distribuir las teclas proporcionalmente
        espaciado = self.rect.width // (len(self.sequence) + 1)
        
        for i, tecla in enumerate(self.sequence):
            # Color verde si ya se pulsó, blanco si está pendiente
            color = (0, 255, 100) if i < self.current_step else (255, 255, 255)
            
            # Resaltar la tecla actual con un círculo o subrayado
            if i == self.current_step:
                pygame.draw.circle(window, (255, 255, 255), 
                                   (self.rect.left + espaciado * (i + 1), self.rect.centery), 40, 2)

            simbolo = self.available_keys[tecla]
            txt_surface = fuente.render(simbolo, True, color)
            txt_rect = txt_surface.get_rect(center=(self.rect.left + espaciado * (i + 1), self.rect.centery))
            window.blit(txt_surface, txt_rect)