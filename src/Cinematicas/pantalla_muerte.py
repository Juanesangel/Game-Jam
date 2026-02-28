# pantalla_muerte.py
import pygame
import sys

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

class BotonTexto:
    def __init__(self, texto, centro, fuente, on_click):
        self.texto = texto
        self.fuente = fuente
        self.on_click = on_click
        self.hover = False
        self.texto_surf = self.fuente.render(self.texto, True, BLANCO)
        self.rect = self.texto_surf.get_rect(center=centro)

    def draw(self, surface):
        if self.hover:
            borde_rect = self.rect.inflate(16, 10)
            pygame.draw.rect(surface, (255, 255, 255), borde_rect, width=2, border_radius=10)
        sombra = self.fuente.render(self.texto, True, (0, 0, 0))
        sombra_rect = sombra.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))
        surface.blit(sombra, sombra_rect)
        surface.blit(self.texto_surf, self.rect)

class EscenaMuerte:
    def __init__(self, cambiar_escena_cb, ancho, alto, fuente_titulo=None, fuente_ui=None, fondo_path="assets/Assets_Menu_inicio/Game_over.jpeg"):
        self.cambiar_escena = cambiar_escena_cb
        self.ANCHO = ancho
        self.ALTO = alto
        self._musica_activa = False

        # --- MANEJO SEGURO DE AUDIO (SOLUCIÓN WASAPI) ---
        try:
            # Intentar inicializar con parámetros estándar para evitar conflictos de frecuencia
            if not pygame.mixer.get_init():
                pygame.mixer.pre_init(44100, -16, 2, 512)
                pygame.mixer.init()
            
            pygame.mixer.music.stop()
            self.musica_path = "assets/Assets_Menu_inicio/Audio_Gameover.mp3"
            pygame.mixer.music.load(self.musica_path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            self._musica_activa = True
        except Exception as e:
            # Si hay error de endpoint o WASAPI, el juego NO se cierra
            print(f"[AUDIO SKIP] No se pudo cargar el sonido de muerte: {e}")
            self._musica_activa = False

        # Ocultar mouse para control por teclado
        pygame.mouse.set_visible(False)

        # Carga de fuentes con fallback
        try:
            self.FUENTE_TITULO = fuente_titulo or pygame.font.Font("assets/Assets_Menu_inicio/PressStart2P-Regular.ttf", 50)
            self.FUENTE_UI = fuente_ui or pygame.font.Font("assets/Assets_Menu_inicio/PressStart2P-Regular.ttf", 20)
        except:
            self.FUENTE_TITULO = pygame.font.SysFont("Arial", 60, bold=True)
            self.FUENTE_UI = pygame.font.SysFont("Arial", 30, bold=True)

        # Carga de fondo
        self.fondo = None
        try:
            self.fondo = pygame.image.load(fondo_path).convert()
            self.fondo = pygame.transform.scale(self.fondo, (self.ANCHO, self.ALTO))
        except:
            print("[ADVERTENCIA] No se encontró la imagen de Game Over.")

        self.overlay = pygame.Surface((self.ANCHO, self.ALTO), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

        self.titulo_surf = self.FUENTE_TITULO.render("HAS PERDIDO", True, (255, 50, 50))
        self.titulo_rect = self.titulo_surf.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 - 80))

        # Botón configurado para "menu" (nombre usado en JuegoMotor)
        self.boton_menu = BotonTexto(
            "REINTENTAR", 
            (self.ANCHO // 2, self.ALTO // 2 + 60), 
            self.FUENTE_UI,
            on_click=lambda: (self._detener_musica(), self.cambiar_escena("menu"))
        )

        self.botones = [self.boton_menu]
        self.index_foco = 0
        self.tiempo_entrada = 0.0

    def _detener_musica(self, con_fade=True):
        if self._musica_activa:
            try:
                if con_fade:
                    pygame.mixer.music.fadeout(500)
                else:
                    pygame.mixer.music.stop()
            except:
                pass
            finally:
                self._musica_activa = False

    def manejar_eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_z):
                    if self.tiempo_entrada > 0.5: # Pequeño delay para evitar skips accidentales
                        self.botones[self.index_foco].on_click()

    def actualizar(self, dt):
        self.tiempo_entrada += dt
        for i, b in enumerate(self.botones):
            b.hover = (i == self.index_foco)

    def dibujar(self, surface):
        if self.fondo:
            surface.blit(self.fondo, (0, 0))
        else:
            surface.fill((20, 0, 0))
            
        surface.blit(self.overlay, (0, 0))
        surface.blit(self.titulo_surf, self.titulo_rect)

        for b in self.botones:
            b.draw(surface)
            
        pie = self.FUENTE_UI.render("Enter para volver al menú", True, BLANCO)
        surface.blit(pie, (self.ANCHO // 2 - pie.get_width() // 2, self.ALTO - 50))