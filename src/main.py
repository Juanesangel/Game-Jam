import pygame
import sys
from cocina import Cocina
from Enemigos.enemigo_normal import Enemigo_normal
import os
from config.window_config import WindowConfig as wc
from src.entities import cook as c
from src.entities import personaje
from src.entities import weapon
from src.Menu_inicio import EscenaBase, MenuInicio

class EscenaJuego(EscenaBase):
    def __init__(self, cambiar_escena_cb):
        super().__init__(cambiar_escena_cb)
        self.ancho, self.alto = wc.WIDTH, wc.HEIGHT
        self.cook_minigame = c.Cook()
        self.puntuacion = 0
        self.fuente_ui = pygame.font.SysFont("Arial", 40, bold=True)
        self.tiempo_limite = 0
        self.dificultad_maxima = False

        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.jugador = personaje.Personaje(50, 50, self._cargar_animaciones())
        self.pistola = weapon.Weapon(self._cargar_arma())

    def _cargar_animaciones(self):
        imgs = []
        for i in range(8):
            path = os.path.join(self.BASE_DIR, "assets", "Images", "characters", "Player", f"Personaje_Principal-{i}.png")
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            img = pygame.transform.scale(img, (int(w * wc.SCALA_PERSONAJE), int(h * wc.SCALA_PERSONAJE)))
            imgs.append(img)
        return imgs

    def _cargar_arma(self):
        path = os.path.join(self.BASE_DIR, "assets", "Images", "weapons", "Empanada.png")
        img = pygame.image.load(path).convert_alpha()
        w, h = img.get_size()
        return pygame.transform.scale(img, (int(w * wc.SCALA_ARMA), int(h * wc.SCALA_ARMA)))

    def manejar_eventos(self, eventos):
        t = pygame.time.get_ticks()
        for e in eventos:
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            self.cook_minigame.handle_input(e)
            
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                if not self.cook_minigame.active:
                    if self.cook_minigame.initiate_execution():
                        self.tiempo_limite = t + self.cook_minigame.get_timer()

    def actualizar(self, dt):
        t = pygame.time.get_ticks()

        # 1. Dificultad Dinámica
        if self.puntuacion >= 10 and not self.dificultad_maxima:
            self.cook_minigame.update_difficulty(use_wasd=True)
            self.dificultad_maxima = True
        
        # 2. Movimiento (Bloqueado si cocina)
        if not self.cook_minigame.active:
            keys = pygame.key.get_pressed()
            dx = (keys[pygame.K_d] - keys[pygame.K_a]) * 5
            dy = (keys[pygame.K_s] - keys[pygame.K_w]) * 5
            self.jugador.movimiento(dx, dy)
        
        self.jugador.update()
        self.pistola.update(self.jugador)

        # 3. Control de Tiempo del Minijuego
        if self.cook_minigame.active and t >= self.tiempo_limite:
            self.cook_minigame.cease_execution(apply_penalty=True)

        # 4. PROCESAR PUNTUACIÓN (Lógica Infalible)
        if self.cook_minigame.puntos_pendientes != 0:
            self.puntuacion += self.cook_minigame.puntos_pendientes
            self.puntuacion = max(0, self.puntuacion) # Nunca menor a 0
            
            # Vaciamos el buzón para que no se sume más de una vez
            self.cook_minigame.puntos_pendientes = 0

    def dibujar(self, surface):
        t = pygame.time.get_ticks()
        surface.fill((30, 30, 30))
        self.jugador.dibujar(surface)
        self.pistola.dibujar(surface)

        if self.cook_minigame.active:
            self.cook_minigame.continue_execution(surface)

        # UI: Pedidos
        score_txt = self.fuente_ui.render(f"PEDIDOS: {self.puntuacion}", True, (255, 215, 0))
        surface.blit(score_txt, (40, 40))

        # UI: Recarga
        if not self.cook_minigame.active and t < self.cook_minigame.lock_timer:
            restante = (self.cook_minigame.lock_timer - t) / 1000
            aviso = self.fuente_ui.render(f"RECARGANDO: {restante:.1f}s", True, (255, 80, 80))
            surface.blit(aviso, (self.ancho // 2 - aviso.get_width() // 2, 100))

# --- EL RESTO DE JUEGOMOTOR SE MANTIENE IGUAL ---
class JuegoMotor:
    def __init__(self):
        pygame.init()
        wc.initialize()
        self.ventana = pygame.display.set_mode((wc.WIDTH, wc.HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.fading, self.fade_alpha, self.proxima_escena = False, 0, ""
        self.escena_actual = MenuInicio(self.iniciar_fade)

    def iniciar_fade(self, nombre_escena):
        self.fading, self.proxima_escena = True, nombre_escena

    def _cambiar_escena_real(self):
        if self.proxima_escena == "menu": self.escena_actual = MenuInicio(self.iniciar_fade)
        elif self.proxima_escena == "juego": self.escena_actual = EscenaJuego(self.iniciar_fade)
        self.fading = False

    def run(self):
        while True:
            dt = self.clock.tick(wc.FPS) / 1000.0
            eventos = pygame.event.get()
            if not self.fading or self.fade_alpha < 255:
                self.escena_actual.manejar_eventos(eventos)
                self.escena_actual.actualizar(dt)
            self.escena_actual.dibujar(self.ventana)

            if self.fading:
                self.fade_alpha = min(255, self.fade_alpha + 12)
                if self.fade_alpha == 255: self._cambiar_escena_real()
            else:
                self.fade_alpha = max(0, self.fade_alpha - 12)
            
            if self.fade_alpha > 0:
                s = pygame.Surface((wc.WIDTH, wc.HEIGHT))
                s.set_alpha(self.fade_alpha); s.fill((0, 0, 0))
                self.ventana.blit(s, (0,0))
            pygame.display.flip()

if __name__ == "__main__":
    JuegoMotor().run()