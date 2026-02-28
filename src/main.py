import pygame
import sys
import os
import random
from Powers.powers import SeleccionPowerUp
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
        self.anim_speed = 120

    def actualizar(self):
        if pygame.time.get_ticks() - self.update_time > self.anim_speed:
            self.frame_index = (self.frame_index + 1) % len(self.imagenes)
            self.update_time = pygame.time.get_ticks()

    def dibujar(self, surface):
        surface.blit(self.imagenes[self.frame_index], (0, 0))

class EscenaJuego(EscenaBase):
    def __init__(self, cambiar_escena_cb):
        super().__init__(cambiar_escena_cb)
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        assets_fondo = self._cargar_assets_escenario()
        self.escenario = Escenario(assets_fondo)
        
        # Spawn inicial del personaje en la mitad inferior
        self.jugador = personaje.Personaje(wc.WIDTH//2, wc.HEIGHT - 100, self._cargar_animaciones_jugador())
        # Cocina cerca del límite medio
        self.cocina = Cocina(wc.WIDTH//2, (wc.HEIGHT//2) + 60, self._cargar_animaciones_cocina())
        self.animaciones_enemigo = self._cargar_animaciones_enemigo()
        
        self.cook_minigame = c.Cook()
        self.menu_powerup = SeleccionPowerUp(self.jugador) 
        self.enemigos = []
        self.puntuacion = 0
        self.ultimo_umbral_powerup = 0
        self.ultimo_spawn = 0
        self.spawn_cooldown = 2000
        self.show_debug = False
        self.dificultad_maxima = False
        self.timer_cartel_dificultad = 0
        
        # --- NUEVO: Cargar Escenario ---
        self.escenario = Escenario(self._cargar_assets_escenario())
        
        # --- Entidades ---
        self.jugador = personaje.Personaje(wc.WIDTH//2, wc.HEIGHT//2, self._cargar_animaciones_jugador())
        self.cocina = Cocina(wc.WIDTH//2, wc.HEIGHT//2 - 100, self._cargar_animaciones_cocina())
        
        self.cook_minigame = c.Cook()
        self.enemigos = []
        self.animaciones_enemigo = self._cargar_animaciones_enemigo()
        self.spawn_cooldown = 2000
        self.ultimo_spawn = 0
        self.fuente_ui = pygame.font.SysFont("Arial", 30, bold=True)

    def _cargar_assets_escenario(self):
        imgs = []
        # Asumiendo que las imágenes en 'transmilenio' siguen un patrón numérico o similar
        path_dir = os.path.join(self.BASE_DIR, "assets", "Images", "escenarios", "transmilenio")
        # Listamos y ordenamos los archivos para que la animación tenga sentido
        archivos = sorted([f for f in os.listdir(path_dir) if f.endswith('.png')])
        
        for nombre in archivos:
            img = pygame.image.load(os.path.join(path_dir, nombre)).convert()
            # Escalamos la imagen al tamaño total de la ventana configurada
            imgs.append(pygame.transform.scale(img, (wc.WIDTH, wc.HEIGHT)))
        return imgs
        self.menu_powerup = SeleccionPowerUp(self.jugador)

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
        # Solo spawnear en la mitad inferior
        mitad_y = wc.HEIGHT // 2
        opciones = [
            (random.randint(0, wc.WIDTH), wc.HEIGHT + 50),       # Borde inferior
            (-50, random.randint(mitad_y, wc.HEIGHT)),          # Lateral izquierdo inferior
            (wc.WIDTH + 50, random.randint(mitad_y, wc.HEIGHT)) # Lateral derecho inferior
        ]
        x, y = random.choice(opciones)
        en = Enemigo_normal(int(x), int(y), self.animaciones_enemigo, velocidad=1.5)
        self.enemigos.append(en)

    def manejar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if self.menu_powerup.activo:
                self.menu_powerup.manejar_eventos(e)
                continue
            keys = pygame.key.get_pressed()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_F4 and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                self.show_debug = not self.show_debug
            if not self.cook_minigame.active and self.jugador.hitbox.colliderect(self.cocina.hitbox):
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE: self.cook_minigame.initiate_execution("Empanada", self.dificultad_maxima)
                    elif e.key == pygame.K_f: self.cook_minigame.initiate_execution("Arepa", self.dificultad_maxima)
            self.cook_minigame.handle_input(e)
    
    def manejar_eventos_powers(self, eventos):
        t = pygame.time.get_ticks()

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
        if self.menu_powerup.activo: return
        t = pygame.time.get_ticks()
        self.escenario.actualizar()
        self.menu_powerup.actualizar()
        if t - self.ultimo_spawn > self.spawn_cooldown:
            self.spawn_enemigo()
            self.ultimo_spawn = t
        if not self.cook_minigame.active:
            k = pygame.key.get_pressed()
            dx = (k[pygame.K_d] - k[pygame.K_a])
            dy = (k[pygame.K_s] - k[pygame.K_w])
            self.jugador.movimiento(dx, dy)
        self.jugador.update()
        self.cocina.update()
        for en in self.enemigos: 
            en.update(self.jugador)

        if self.cook_minigame.puntos_pendientes > 0:
            self.puntuacion += self.cook_minigame.puntos_pendientes
            tipo = self.cook_minigame.tipo_comida
            candidatos = [en for en in self.enemigos if en.pedido == tipo]
            for _ in range(min(2, len(candidatos))):
                if candidatos:
                    victima = random.choice(candidatos)
                    if victima in self.enemigos: self.enemigos.remove(victima)
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
            if self.puntuacion // 15 > self.ultimo_umbral_powerup:
                self.ultimo_umbral_powerup = self.puntuacion // 15
                self.menu_powerup.activar_menu()

        if self.cook_minigame.active and t > self.cook_minigame.start_time + self.cook_minigame.timer_duration:
            self.cook_minigame.cease_execution(True)

    def dibujar(self, surface):
        self.escenario.dibujar(surface)
        self.cocina.dibujar(surface, self.show_debug)
        for en in self.enemigos: en.dibujar(surface, self.show_debug)
        self.jugador.dibujar(surface, self.show_debug)
        if self.jugador.hitbox.colliderect(self.cocina.hitbox) and not self.cook_minigame.active:
            hint = self.fuente_ui.render("[ESPACIO] Empanada | [F] Arepa", True, (0, 255, 200))
            surface.blit(hint, (wc.WIDTH//2 - hint.get_width()//2, wc.HEIGHT - 50))

        if self.cook_minigame.active:
            self.cook_minigame.continue_execution(surface)

        p_txt = self.fuente_ui.render(f"PUNTOS: {self.puntuacion}", True, (255, 215, 0))
        surface.blit(p_txt, (20, 20))
        #UI: Power ups
        self.menu_powerup.dibujar(surface)

# --- CLASE JUEGOMOTOR ---
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
        if self.proxima_escena == "juego": self.escena_actual = EscenaJuego(self.iniciar_fade)
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
            else: self.fade_alpha = max(0, self.fade_alpha - 15)
            if self.fade_alpha > 0:
                s = pygame.Surface((wc.WIDTH, wc.HEIGHT))
                s.set_alpha(self.fade_alpha)
                s.fill((0,0,0))
                self.ventana.blit(s, (0,0))
            pygame.display.flip()