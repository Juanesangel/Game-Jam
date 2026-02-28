import pygame
import sys
import os
import random
from src.powers import SeleccionPowerUp
from config.window_config import WindowConfig as wc
from src.entities import cook as c
from src.entities import personaje
from src.entities.cocina import Cocina 
from src.Enemigos.enemigo_normal import Enemigo_normal
from src.Menu_inicio import EscenaBase, MenuInicio



class Escenario:
    def __init__(self, imagenes):
        self.imagenes = imagenes
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.anim_speed = 120  # Milisegundos entre frames

    def actualizar(self):
        if pygame.time.get_ticks() - self.update_time > self.anim_speed:
            self.frame_index = (self.frame_index + 1) % len(self.imagenes)
            self.update_time = pygame.time.get_ticks()

    def dibujar(self, surface):
        # Dibujamos el frame actual escalado a toda la ventana
        surface.blit(self.imagenes[self.frame_index], (0, 0))

class EscenaJuego(EscenaBase):
    def __init__(self, cambiar_escena_cb):
        super().__init__(cambiar_escena_cb)
<<<<<<<<< Temporary merge branch 1
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.puntuacion = 0
        self.show_debug = False
        self.dificultad_maxima = False
        self.timer_cartel_dificultad = 0
        
        # Entidades
        self.jugador = personaje.Personaje(wc.WIDTH//2, wc.HEIGHT//2, self._cargar_animaciones_jugador())
        self.cocina = Cocina(wc.WIDTH//2, wc.HEIGHT//2 - 100, self._cargar_animaciones_cocina())
        
        self.cook_minigame = c.Cook()
        self.enemigos = []
        self.animaciones_enemigo = self._cargar_animaciones_enemigo()
        self.spawn_cooldown = 2000
        self.ultimo_spawn = 0
        self.fuente_ui = pygame.font.SysFont("Arial", 30, bold=True)
=========
        self.ultimo_umbral_powerup = 0
        self.ancho, self.alto = wc.WIDTH, wc.HEIGHT
        self.cook_minigame = c.Cook()
        self.puntuacion = 0
        self.fuente_ui = pygame.font.SysFont("Arial", 40, bold=True)
        self.tiempo_limite = 0
        self.dificultad_maxima = False

        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.jugador = personaje.Personaje(50, 50, self._cargar_animaciones())
        self.menu_powerup = SeleccionPowerUp(self.jugador)
>>>>>>>>> Temporary merge branch 2

    def _cargar_animaciones_jugador(self):
        imgs = []
        for i in range(8):
            path = os.path.join(self.BASE_DIR, "assets", "Images", "characters", "Player", f"Personaje_Principal-{i}.png")
            img = pygame.image.load(path).convert_alpha()
            imgs.append(pygame.transform.scale(img, (int(img.get_width() * wc.SCALA_PERSONAJE), int(img.get_height() * wc.SCALA_PERSONAJE))))
        return imgs

    def _cargar_animaciones_cocina(self):
        imgs = []
        for i in range(9):
            path = os.path.join(self.BASE_DIR, "assets", "Images", "characters", "Cocina", f"Cocina-{i}.png")
            img = pygame.image.load(path).convert_alpha()
            imgs.append(img)
        return imgs

    def _cargar_animaciones_enemigo(self):
        imgs = []
        for i in range(7):
            path = os.path.join(self.BASE_DIR, "assets", "Images", "enemigos", "enemigos_normales", f"cliente-{i}.png")
            img = pygame.image.load(path).convert_alpha()
            imgs.append(pygame.transform.scale(img, (int(img.get_width() * 0.3), int(img.get_height() * 0.3))))
        return imgs

    def spawn_enemigo(self):
        x, y = random.choice([(random.randint(0, wc.WIDTH), -50), (random.randint(0, wc.WIDTH), wc.HEIGHT+50), (-50, random.randint(0, wc.HEIGHT))])
        en = Enemigo_normal(float(x), float(y), self.animaciones_enemigo, velocidad=1.5)
        self.enemigos.append(en)

    def manejar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            
            keys = pygame.key.get_pressed()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_F4 and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                self.show_debug = not self.show_debug

            if not self.cook_minigame.active and self.jugador.hitbox.colliderect(self.cocina.hitbox):
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        self.cook_minigame.initiate_execution("Empanada", self.dificultad_maxima)
                    elif e.key == pygame.K_f:
                        self.cook_minigame.initiate_execution("Arepa", self.dificultad_maxima)
            
            self.cook_minigame.handle_input(e)
<<<<<<<<< Temporary merge branch 1
=========
            
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                if not self.cook_minigame.active:
                    if self.cook_minigame.initiate_execution():
                        self.tiempo_limite = t + self.cook_minigame.get_timer()
    
    def manejar_eventos_powers(self, eventos):
        t = pygame.time.get_ticks()
>>>>>>>>> Temporary merge branch 2

        for e in eventos:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.cook_minigame.handle_input(e)

            # PASAMOS EVENTOS AL MENU
            if hasattr(self, "menu_powerup"):
                self.menu_powerup.manejar_eventos(e)

            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                if not self.cook_minigame.active:
                    if self.cook_minigame.initiate_execution():
                        self.tiempo_limite = t + self.cook_minigame.get_timer()
    
    
    def actualizar(self, dt):
        t = pygame.time.get_ticks()
        
        # Actualizar animación de fondo
        self.escenario.actualizar()

        if t - self.ultimo_spawn > self.spawn_cooldown:
            self.spawn_enemigo()
            self.ultimo_spawn = t

        if not self.cook_minigame.active:
            k = pygame.key.get_pressed()
            dx = (k[pygame.K_d] - k[pygame.K_a]) * 5
            dy = (k[pygame.K_s] - k[pygame.K_w]) * 5
            self.jugador.movimiento(dx, dy)
        
        self.jugador.update()
        self.cocina.update()
        for en in self.enemigos: 
            en.update(self.jugador)

<<<<<<<<< Temporary merge branch 1
        if self.cook_minigame.puntos_pendientes > 0:
            tipo = self.cook_minigame.tipo_comida
            self.puntuacion += 1
            candidatos = [en for en in self.enemigos if en.pedido == tipo]
            for _ in range(min(2, len(candidatos))):
                if candidatos:
                    victima = random.choice(candidatos)
                    self.enemigos.remove(victima)
                    candidatos.remove(victima)
=========
        # 3. Control de Tiempo del Minijuego
        if self.cook_minigame.active and t >= self.tiempo_limite:
            self.cook_minigame.cease_execution(apply_penalty=True)

        # 4. PROCESAR PUNTUACIÓN (Lógica Infalible)
        if self.cook_minigame.puntos_pendientes != 0:
            self.puntuacion += self.cook_minigame.puntos_pendientes
            self.puntuacion = max(0, self.puntuacion)

>>>>>>>>> Temporary merge branch 2
            self.cook_minigame.puntos_pendientes = 0
            
            if self.puntuacion >= 10 and not self.dificultad_maxima:
                self.dificultad_maxima = True
                self.timer_cartel_dificultad = t + 2000

        if self.cook_minigame.active and t > self.cook_minigame.start_time + self.cook_minigame.timer_duration:
            self.cook_minigame.cease_execution(True)

            # Detectar si cruzamos múltiplos de 15
            if self.puntuacion // 15 > self.ultimo_umbral_powerup:
                self.ultimo_umbral_powerup = self.puntuacion // 15
                self.menu_powerup.activar_menu()
                    
                # Vaciamos el buzón para que no se sume más de una vez
                self.cook_minigame.puntos_pendientes = 0
        self.menu_powerup.actualizar()

            # Detectar si cruzamos múltiplos de 15
            if self.puntuacion // 15 > self.ultimo_umbral_powerup:
                self.ultimo_umbral_powerup = self.puntuacion // 15
                self.menu_powerup.activar_menu()
                    
                # Vaciamos el buzón para que no se sume más de una vez
                self.cook_minigame.puntos_pendientes = 0
        self.menu_powerup.actualizar()

    def dibujar(self, surface):
        # 1. Dibujar escenario (reemplaza surface.fill)
        self.escenario.dibujar(surface)
        
        # 2. Entidades
        self.cocina.dibujar(surface, self.show_debug)
        for en in self.enemigos:
            en.dibujar(surface, self.show_debug)

        self.jugador.dibujar(surface, self.show_debug)
        
        # 3. UI y Feedback
        if self.jugador.hitbox.colliderect(self.cocina.hitbox) and not self.cook_minigame.active:
            hint = self.fuente_ui.render("[ESPACIO] Empanada | [F] Arepa", True, (0, 255, 200))
            surface.blit(hint, (wc.WIDTH//2 - hint.get_width()//2, wc.HEIGHT - 50))

        if self.cook_minigame.active:
            self.cook_minigame.continue_execution(surface)

        # UI
        p_txt = self.fuente_ui.render(f"PUNTOS: {self.puntuacion}", True, (255, 215, 0))
        surface.blit(p_txt, (20, 20))

<<<<<<<<< Temporary merge branch 1
# --- JUEGO MOTOR (Al margen izquierdo para que el Launcher lo vea) ---
=========
        # UI: Recarga
        if not self.cook_minigame.active and t < self.cook_minigame.lock_timer:
            restante = (self.cook_minigame.lock_timer - t) / 1000
            aviso = self.fuente_ui.render(f"RECARGANDO: {restante:.1f}s", True, (255, 80, 80))
            surface.blit(aviso, (self.ancho // 2 - aviso.get_width() // 2, 100))
        #UI: Power ups
        self.menu_powerup.dibujar(surface)

# --- EL RESTO DE JUEGOMOTOR SE MANTIENE IGUAL ---
>>>>>>>>> Temporary merge branch 2
class JuegoMotor:
    def __init__(self):
        pygame.init()
        wc.initialize()
        self.ventana = pygame.display.set_mode((wc.WIDTH, wc.HEIGHT))
        self.clock = pygame.time.Clock()
        self.escena_actual = MenuInicio(self.iniciar_fade)
        self.fading, self.fade_alpha, self.proxima_escena = False, 0, ""

    def iniciar_fade(self, nombre):
        self.fading, self.proxima_escena = True, nombre

    def _cambiar_escena(self):
        if self.proxima_escena == "juego": 
            self.escena_actual = EscenaJuego(self.iniciar_fade)
        self.fading = False

    def run(self):
        while True:
            dt = self.clock.tick(wc.FPS) / 1000.0
            self.escena_actual.manejar_eventos(pygame.event.get())
            self.escena_actual.actualizar(dt)
            self.escena_actual.dibujar(self.ventana)
            
            if self.fading:
                self.fade_alpha = min(255, self.fade_alpha + 15)
                if self.fade_alpha >= 255: self._cambiar_escena()
            else: 
                self.fade_alpha = max(0, self.fade_alpha - 15)
            
            if self.fade_alpha > 0:
                s = pygame.Surface((wc.WIDTH, wc.HEIGHT))
                s.set_alpha(self.fade_alpha)
                s.fill((0,0,0))
                self.ventana.blit(s, (0,0))
            pygame.display.flip()