
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

    #Musica
    def _detener_musica(self, con_fade=True):
        if pygame.mixer.get_init() and self._musica_activa:
            try:
                if con_fade:
                    pygame.mixer.music.fadeout(600)  # 600 ms para desvanecer
                else:
                    pygame.mixer.music.stop()
            except Exception:
                pass
            finally:
                self._musica_activa = False

    #
    def __init__(self, cambiar_escena_cb, ancho, alto, fuente_titulo=None, fuente_ui=None, fondo_path=None):
        self.cambiar_escena = cambiar_escena_cb
        self.ANCHO = ancho
        self.ALTO = alto

        pygame.mouse.set_visible(False)
        pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL])

        self.FUENTE_TITULO = fuente_titulo or pygame.font.Font("assets/Assets_Menu_inicio/PressStart2P-Regular.ttf", 60)
        self.FUENTE_UI = fuente_ui or pygame.font.Font("assets/Assets_Menu_inicio/PressStart2P-Regular.ttf", 30)

        self.fondo = None
        if fondo_path:
            try:
                self.fondo = pygame.image.load(fondo_path).convert()
                self.fondo = pygame.transform.scale(self.fondo, (self.ANCHO, self.ALTO))
            except Exception as e:
                print(f"[ADVERTENCIA] No se pudo cargar el fondo de muerte: {e}")


        # --- MÚSICA DE FONDO ---
        self.musica_path = "assets/Assets_Menu_inicio/Audio_Gameover.mp3"  # <-- ajusta a tu nombre real
        self._musica_activa = False

        # Inicializa mixer si hace falta
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Si venías del menú con música sonando, asegúrate de frenarla antes:
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

        # Carga y reproduce la pista de "muerte"
        try:
            pygame.mixer.music.load(self.musica_path)
            pygame.mixer.music.set_volume(0.2)   # ajusta (0.0–1.0)
            pygame.mixer.music.play(-1)          # loop infinito mientras estés en esta pantalla
            self._musica_activa = True
        except pygame.error as e:
            print(f"[ADVERTENCIA] No se pudo reproducir la música de muerte: {e}")


        self.overlay = pygame.Surface((self.ANCHO, self.ALTO), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 160))

        self.titulo_surf = self.FUENTE_TITULO.render("GAME OVER!", True, BLANCO)
        self.titulo_rect = self.titulo_surf.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 - 120))

        opciones_y = self.ALTO // 2 + 10
        sep = 50

        self.boton_menu = BotonTexto(
        "Volver al menú", 
        (self.ANCHO // 2, opciones_y + sep), 
        self.FUENTE_UI,
        on_click=lambda: (self._detener_musica(con_fade=True), self.cambiar_escena("Menú de Inicio"))
        )

        
        self.botones = [self.boton_menu]
        self.index_foco = 0

        self.tiempo_entrada = 0.0
        self.bloqueo_ms = 200

    def manejar_eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.tiempo_entrada < self.bloqueo_ms / 1000.0:
                    continue
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.botones[self.index_foco].on_click()

    def actualizar(self, dt):
        self.tiempo_entrada += dt
        for i, b in enumerate(self.botones):
            b.hover = (i == self.index_foco)

    def dibujar(self, surface):
        if self.fondo:
            surface.blit(self.fondo, (0, 0))
        else:
            surface.fill((30, 0, 0))
        surface.blit(self.overlay, (0, 0))
        surface.blit(self.titulo_surf, self.titulo_rect)

        for b in self.botones:
            b.draw(surface)
        pie = self.FUENTE_UI.render("• Enter - seleccionar", True, BLANCO)
        pie_rect = pie.get_rect(midbottom=(self.ANCHO // 2, self.ALTO - 24))
        surface.blit(pie, pie_rect)



# ---------------------------
# PREVIEW LOCAL 
# ---------------------------
if __name__ == "__main__":
    pygame.init()
    
    info = pygame.display.Info()
    ANCHO, ALTO = info.current_w, info.current_h
    VENTANA = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Preview - Pantalla de Muerte")
    CLOCK = pygame.time.Clock()
    FPS = 20

    
    def dummy_cambiar_escena(nombre):
        print(f"[Preview] cambiar_escena('{nombre}')")
        
        if nombre == "Menú de Inicio":
            pygame.quit()
            sys.exit()

    escena = EscenaMuerte(
        cambiar_escena_cb=dummy_cambiar_escena,
        ancho=ANCHO, alto=ALTO,
        fondo_path="assets/Assets_Menu_inicio/Game_over.jpeg"
    )

    while True:
        dt = CLOCK.tick(FPS) / 1000.0
        eventos = pygame.event.get()
        escena.manejar_eventos(eventos)
        escena.actualizar(dt)
        escena.dibujar(VENTANA)
        pygame.display.flip()
