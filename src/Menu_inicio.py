import pygame
import sys

# Configuración inicial
# ----------------------------
pygame.init()
info = pygame.display.Info()
ANCHO, ALTO = info.current_w, info.current_h
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menú de Inicio - Demo")
CLOCK = pygame.time.Clock()
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (60, 60, 60)
AZUL = (70, 140, 240)
AZUL_HOVER = (90, 160, 255)
ROJO = (220, 60, 60)
ROJO_HOVER = (240, 90, 90)

# Fuente
FUENTE_TITULO = pygame.font.SysFont("arial", 56, bold=True)
FUENTE_BOTON = pygame.font.SysFont("arial", 28, bold=True)
FUENTE_UI = pygame.font.SysFont("arial", 22)


# Utilidades UI
# ----------------------------
class Boton:
    def __init__(self, texto, rect, color_base, color_hover, on_click):
        self.texto = texto
        self.rect = pygame.Rect(rect)
        self.color_base = color_base
        self.color_hover = color_hover
        self.on_click = on_click
        self.hover = False  # lo usaremos como "en foco", no como hover de mouse

    def draw(self, surface):
        color = self.color_hover if self.hover else self.color_base
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, width=2, border_radius=12)

        texto_surf = FUENTE_BOTON.render(self.texto, True, BLANCO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        surface.blit(texto_surf, texto_rect)

    # En el menú deshabilitamos totalmente el mouse, así que estos métodos no se usan allí.
    def update(self, mouse_pos=None):
        pass

    def handle_event(self, event):
        pass


# Escenas
# ----------------------------
class EscenaBase:
    def __init__(self, cambiar_escena_cb):
        self.cambiar_escena = cambiar_escena_cb

    def manejar_eventos(self, eventos): ...
    def actualizar(self, dt): ...
    def dibujar(self, surface): ...

class MenuInicio(EscenaBase):
    def __init__(self, cambiar_escena_cb):
        super().__init__(cambiar_escena_cb)

        # 1) Ocultar cursor y 2) bloquear eventos de mouse mientras estamos en el menú
        pygame.mouse.set_visible(False)
        pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL])

        self.fondo = pygame.image.load("assets/Assets_Menu_inicio/Fondo_Menu_inicio.png").convert()
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
        
        self.overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 100)) 

        ancho_boton, alto_boton = 260, 60
        x = (ANCHO - ancho_boton) // 2
        y_base = ALTO // 2 - 40

        self.boton_jugar = Boton(
            "Iniciar juego",
            (x, y_base, ancho_boton, alto_boton),
            AZUL, AZUL_HOVER,
            on_click=lambda: self.cambiar_escena("juego")
        )

        self.boton_salir = Boton(
            "Salir",
            (x, y_base + 80, ancho_boton, alto_boton),
            ROJO, ROJO_HOVER,
            on_click=lambda: pygame.event.post(pygame.event.Event(pygame.QUIT))
        )

        self.botones = [self.boton_jugar, self.boton_salir]
        self.index_foco = 0 

    def manejar_eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_TAB):
                    self.index_foco = (self.index_foco + 1) % len(self.botones)
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.index_foco = (self.index_foco - 1) % len(self.botones)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.botones[self.index_foco].on_click()

    def actualizar(self, dt):

        for i, b in enumerate(self.botones):
            b.hover = (i == self.index_foco)

    def dibujar(self, surface):

        surface.blit(self.fondo, (0, 0))
        surface.blit(self.overlay, (0, 0))

        titulo = FUENTE_TITULO.render("Nombre...", True, BLANCO)
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 140))
        surface.blit(titulo, titulo_rect)

        subtitulo = FUENTE_UI.render("Usa ↑/↓ (o W/S) y Enter", True, BLANCO)
        subtitulo_rect = subtitulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 100))
        surface.blit(subtitulo, subtitulo_rect)

        for b in self.botones:
            b.draw(surface)

class EscenaJuego(EscenaBase):
    def __init__(self, cambiar_escena_cb):
        super().__init__(cambiar_escena_cb)
        self.tiempo = 0

        
        pygame.mouse.set_visible(True)
        pygame.event.set_allowed(None) 
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])

    def manejar_eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.cambiar_escena("menu")

    def actualizar(self, dt):
        self.tiempo += dt

    def dibujar(self, surface):
        surface.fill((25, 25, 35))
        titulo = FUENTE_TITULO.render("Juego!", True, BLANCO)
        surface.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 120)))

class Juego:
    def __init__(self):
        self.escenas = {}
        self.escena_actual = None
        self.cambiar_escena("menu")

    def cambiar_escena(self, nombre):
        if nombre == "menu":
            self.escenas["menu"] = MenuInicio(self.cambiar_escena)
            self.escena_actual = self.escenas["menu"]
        elif nombre == "juego":
            self.escenas["juego"] = EscenaJuego(self.cambiar_escena)
            self.escena_actual = self.escenas["juego"]
        else:
            raise ValueError(f"Escena desconocida: {nombre}")

    def run(self):
        while True:
            dt = CLOCK.tick(FPS) / 1000.0
            eventos = pygame.event.get()
            self.escena_actual.manejar_eventos(eventos)
            self.escena_actual.actualizar(dt)
            self.escena_actual.dibujar(VENTANA)
            pygame.display.flip()


# Entry point
# ----------------------------
if __name__ == "__main__":
    juego = Juego()
    juego.run()