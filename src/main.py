import pygame
import sys
import os
import random
from config.window_config import WindowConfig as wc
from entities import cook as c
from entities import personaje
from entities.cocina import Cocina 
from Enemigos.enemigo_normal import Enemigo_normal
from Enemigos.cliente3 import Cliente3
from Enemigos.nino import Nino
from Cinematicas.Menu_inicio import EscenaBase, MenuInicio
from Cinematicas.cinematica_intro import EscenaCinematica 
from Cinematicas.pantalla_muerte import EscenaMuerte


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
        self.jugador = personaje.Personaje(wc.WIDTH//2, wc.HEIGHT - 100, self._cargar_animaciones_jugador())
        self.cocina = Cocina(wc.WIDTH//2, (wc.HEIGHT//2) + 200, self._cargar_animaciones_cocina())
        self.animaciones_gordo = self._cargar_animaciones_gordo()
        self.animaciones_enemigo = self._cargar_animaciones_enemigo()
        self.animaciones_cliente3 = self._cargar_animaciones_cliente3()
        self.animaciones_nino = self._cargar_animaciones_nino3()        
        self.cook_minigame = c.Cook()
        self.enemigos = []
        self.puntuacion = 0
        self.velocidad_base_enemigos = 2.0
        self.ultimo_umbral_velocidad = 0
        self.ultimo_umbral_powerup = 0
        self.ultimo_spawn = 1
        self.spawn_cooldown = 3000
        self.cambio_escenario_realizado = False
        self.fade_interno_activo = False
        self.fade_interno_alpha = 0
        self.paso_escenario = 0 
        self.show_debug = False
        self.pausado = False
        self.mensaje_dificultad_timer = 0
        self.fuente_ui = pygame.font.SysFont("Arial", 30, bold=True)
        self.fuente_notif = pygame.font.SysFont("Arial", 24, bold=True)

    def _cargar_assets_escenario(self, nombre_carpeta="transmilenio"):
        imgs = []
        path_dir = os.path.join(self.BASE_DIR, "assets", "Images", "escenarios", nombre_carpeta)
        if not os.path.exists(path_dir): return [pygame.Surface((wc.WIDTH, wc.HEIGHT))]
        archivos = sorted([f for f in os.listdir(path_dir) if f.endswith('.png')])
        for nombre in archivos:
            img = pygame.image.load(os.path.join(path_dir, nombre)).convert()
            imgs.append(pygame.transform.scale(img, (wc.WIDTH, wc.HEIGHT)))
        return imgs

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
            imgs.append(pygame.transform.scale(img, (int(img.get_width() * 0.18), int(img.get_height() * 0.18))))
        return imgs
    def _cargar_animaciones_gordo(self):
        imgs = []
        for i in range(7):
            path = os.path.join(
                self.BASE_DIR,
                "assets",
                "Images",
                "enemigos",
                "Cliente 2",
                f"cliente-{i}.png"
            )
            img = pygame.image.load(path).convert_alpha()
            imgs.append(
                pygame.transform.scale(
                    img,
                    (int(img.get_width() * 0.22), int(img.get_height() * 0.22))
                )
            )
        return imgs
    def _cargar_animaciones_cliente3(self):
        imgs = []
        for i in range(7):
            path = os.path.join(
                self.BASE_DIR,
                "assets",
                "Images",
                "enemigos",
                "Cliente 3",
                f"cliente-{i}.png"
            )
            img = pygame.image.load(path).convert_alpha()
            imgs.append(
                pygame.transform.scale(
                    img,
                    (int(img.get_width() * 0.22), int(img.get_height() * 0.22))
                )
            )
        return imgs
    def _cargar_animaciones_nino3(self):
        imgs = []
        for i in range(7):
            path = os.path.join(
                self.BASE_DIR,
                "assets",
                "Images",
                "enemigos",
                "Nino",
                f"Nino_-{i}.png"
            )
            img = pygame.image.load(path).convert_alpha()
            imgs.append(
                pygame.transform.scale(
                    img,
                    (int(img.get_width() * 0.22), int(img.get_height() * 0.22))
                )
            )
        return imgs
    def _crear_gordo(self, x, y):
        return Enemigo_normal(
            x,
            y,
            self.animaciones_gordo,
            velocidad=self.velocidad_base_enemigos - 0.5
        )
    def manejar_eventos(self, eventos):
        ahora = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        for e in eventos:
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_F4 and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                    self.show_debug = not self.show_debug
                if e.key == pygame.K_ESCAPE:
                    self.pausado = not self.pausado


            if self.cook_minigame.active:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    # Cancelar manualmente activa bloqueo corto
                    self.cook_minigame.active = False
                    self.cook_minigame.lock_until = ahora + 1000
                    continue
                self.cook_minigame.handle_input(e)
            else:
                if ahora >= self.cook_minigame.lock_until:
                    if self.jugador.hitbox.colliderect(self.cocina.hitbox):
                        if e.type == pygame.KEYDOWN:
                            if e.key == pygame.K_SPACE: 
                                self.cook_minigame.initiate_execution("Empanada", self.puntuacion >= 5)
                            elif e.key == pygame.K_f: 
                                self.cook_minigame.initiate_execution("Arepa", self.puntuacion >= 5)



        t = pygame.time.get_ticks()
        self.escenario.actualizar()
        
        if self.puntuacion >= 5 and not self.cambio_escenario_realizado:
            self.fade_interno_activo = True
            self.paso_escenario = 1 
            
        if self.fade_interno_activo:
            if self.paso_escenario == 1:
                self.fade_interno_alpha += 5
                if self.fade_interno_alpha >= 255:
                    self.fade_interno_alpha = 255
                    self.enemigos.clear() 
                    self.escenario.imagenes = self._cargar_assets_escenario("monserrate")
                    self.cambio_escenario_realizado = True
                    self.paso_escenario = 2
            elif self.paso_escenario == 2:
                self.fade_interno_alpha -= 5
                if self.fade_interno_alpha <= 0:
                    self.fade_interno_alpha = 0; self.fade_interno_activo = False

        # ---- SPAWN DE ENEMIGOS ----
        if t - self.ultimo_spawn > self.spawn_cooldown:

            mitad_y = (wc.HEIGHT // 2) - 100
            x, y = random.choice([
                (random.randint(0, wc.WIDTH), wc.HEIGHT + 50),
                (-50, random.randint(mitad_y, wc.HEIGHT))
            ])

            r = random.random()

            if r < 0.5:
                enemigo = Enemigo_normal(
                    int(x), int(y),
                    self.animaciones_enemigo,
                    velocidad=self.velocidad_base_enemigos
                )

            elif r < 0.8:
                enemigo = Nino(
                    int(x), int(y),
                    self.animaciones_nino,
                    velocidad=self.velocidad_base_enemigos - 0.1
                )

            elif r < 0.2:
                enemigo = self._crear_gordo(int(x), int(y))

            else:
                enemigo = Cliente3(
                    int(x), int(y),
                    self.animaciones_cliente3,
                    velocidad=self.velocidad_base_enemigos - 0.1
                )
            self.enemigos.append(enemigo)
            self.ultimo_spawn = t

        # ---- MOVIMIENTO JUGADOR ----
        if not self.cook_minigame.active:
            k = pygame.key.get_pressed()
            self.jugador.movimiento(
                k[pygame.K_d] - k[pygame.K_a],
                k[pygame.K_s] - k[pygame.K_w]
            )

        self.jugador.update()
        self.cocina.update()

        # ---- UPDATE ENEMIGOS ----
        for en in self.enemigos:
            en.update(self.jugador)
            if en.hitbox.colliderect(self.jugador.hitbox):
                self.jugador.recibir_dano(10)
                if self.jugador.vida <= 0: self.cambiar_escena("game_over")

        # ---- ENTREGA DE COMIDA ----
        if self.cook_minigame.entrega_lista:
            comida = self.cook_minigame.entrega_lista
            objetivo, dist_min = None, float("inf")

            for en in self.enemigos:
                if en.pedido == comida:
                    d = ((en.pos_x - self.jugador.rect.centerx) ** 2 +
                        (en.pos_y - self.jugador.rect.centery) ** 2) ** 0.5
                    if d < dist_min:
                        dist_min = d
                        objetivo = en

            if objetivo:
                self.enemigos.remove(objetivo)

            self.cook_minigame.entrega_lista = None

        # ---- SISTEMA DE PUNTUACIÓN Y DIFICULTAD ----
        if self.cook_minigame.puntos_pendientes != 0:

            self.puntuacion += self.cook_minigame.puntos_pendientes
            self.puntuacion = max(0, self.puntuacion)
            if self.puntuacion > 0 and self.puntuacion // 5 > self.ultimo_umbral_velocidad:
                self.ultimo_umbral_velocidad = self.puntuacion // 5
                if self.velocidad_base_enemigos < 100.0:
                    self.velocidad_base_enemigos = min(100.0, self.velocidad_base_enemigos + 1)
                    self.spawn_cooldown = max(1000, self.spawn_cooldown - 600)
                    self.mensaje_dificultad_timer = t + 2500
            if self.puntuacion // 15 > 500000:
                self.ultimo_umbral_powerup = self.puntuacion // 15

            self.cook_minigame.puntos_pendientes = 0

    def dibujar(self, surface):
        ahora = pygame.time.get_ticks()
        self.escenario.dibujar(surface)
        self.cocina.dibujar(surface, self.show_debug)
        for en in self.enemigos: en.dibujar(surface, self.show_debug)
        self.jugador.dibujar(surface, self.show_debug)
        self.jugador.dibujar_barra_vida(surface)
        
        if not self.cook_minigame.active:
            if self.jugador.hitbox.colliderect(self.cocina.hitbox):
                if ahora < self.cook_minigame.lock_until:
                    txt_lock = self.fuente_notif.render("COCINA CALIENTE...", True, (255, 100, 0))
                    surface.blit(txt_lock, (self.cocina.rect.centerx - txt_lock.get_width()//2, self.cocina.rect.top - 40))
                else:
                    txt_cook = self.fuente_notif.render("[SPACE] Empanada  [F] Arepa", True, (255, 255, 255))
                    surface.blit(txt_cook, (self.cocina.rect.centerx - txt_cook.get_width()//2, self.cocina.rect.top - 40))

        if self.cook_minigame.active:
            self.cook_minigame.continue_execution(surface)

        surface.blit(self.fuente_ui.render(f"PUNTOS: {self.puntuacion}", True, (255, 215, 0)), (20, 20))
        if self.pausado:
            overlay = pygame.Surface((wc.WIDTH, wc.HEIGHT), pygame.SRCALPHA); overlay.fill((0,0,0,180)); surface.blit(overlay, (0,0))
            txt_p = self.fuente_ui.render("PAUSA", True, (255,255,255))
            surface.blit(txt_p, (wc.WIDTH//2 - txt_p.get_width()//2, wc.HEIGHT//2))
        
        if self.fade_interno_activo:
            s_fade = pygame.Surface((wc.WIDTH, wc.HEIGHT)); s_fade.set_alpha(self.fade_interno_alpha); s_fade.fill((0, 0, 0)); surface.blit(s_fade, (0, 0))

class JuegoMotor:
    def __init__(self):
        pygame.init(); wc.initialize()
        self.ventana = pygame.display.set_mode((wc.WIDTH, wc.HEIGHT))
        self.clock = pygame.time.Clock()
        self.escena_actual = MenuInicio(self.iniciar_fade)
        self.fading, self.fade_alpha, self.proxima_escena = False, 0, ""

    def iniciar_fade(self, nombre):
        if nombre == "game_over": self.proxima_escena = nombre; self._cambiar_escena()
        else: self.fading, self.proxima_escena = True, nombre

    def _cambiar_escena(self):
        self.fade_alpha = 0
        if self.proxima_escena == "menu": self.escena_actual = MenuInicio(self.iniciar_fade)
        elif self.proxima_escena == "introduccion": self.escena_actual = EscenaCinematica(self.iniciar_fade, wc.WIDTH, wc.HEIGHT, ruta_fondo="assets/Assets_Menu_inicio/Conversacion.jpeg")
        elif self.proxima_escena == "juego": self.escena_actual = EscenaJuego(self.iniciar_fade)
        elif self.proxima_escena == "game_over": self.escena_actual = EscenaMuerte(self.iniciar_fade, wc.WIDTH, wc.HEIGHT)
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
                s = pygame.Surface((wc.WIDTH, wc.HEIGHT)); s.set_alpha(self.fade_alpha); s.fill((0,0,0)); self.ventana.blit(s, (0,0))
            pygame.display.flip()

if __name__ == "__main__":
    motor = JuegoMotor()
    motor.run()