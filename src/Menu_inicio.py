import pygame
import sys

# Colores y Fuentes (Se mantienen como constantes del módulo)
BLANCO = (255, 255, 255)
AZUL, AZUL_HOVER = (70, 140, 240), (90, 160, 255)
ROJO, ROJO_HOVER = (220, 60, 60), (240, 90, 90)

# Las fuentes se cargan una sola vez al importar el módulo
pygame.font.init()
FUENTE_TITULO = pygame.font.SysFont("Arial", 72, bold=True)
FUENTE_BOTON = pygame.font.SysFont("Arial", 32, bold=True)
FUENTE_UI = pygame.font.SysFont("Arial", 24)

class Boton:
    def __init__(self, texto, rect, color_base, color_hover, on_click, imagen_fondo=None):
        self.texto = texto
        self.rect = pygame.Rect(rect)
        self.color_base = color_base
        self.color_hover = color_hover
        self.on_click = on_click
        self.hover = False
        self.imagen_base = pygame.transform.smoothscale(imagen_fondo, self.rect.size) if imagen_fondo else None

    def draw(self, surface):
        if self.imagen_base:
            surface.blit(self.imagen_base, self.rect.topleft)
            if self.hover:
                overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 40))
                surface.blit(overlay, self.rect.topleft)
        else:
            pygame.draw.rect(surface, self.color_hover if self.hover else self.color_base, self.rect, border_radius=12)

        txt = FUENTE_BOTON.render(self.texto, True, BLANCO)
        surface.blit(txt, txt.get_rect(center=self.rect.center))

class EscenaBase:
    def __init__(self, cambiar_escena_cb):
        self.cambiar_escena = cambiar_escena_cb
    def manejar_eventos(self, eventos): pass
    def actualizar(self, dt): pass
    def dibujar(self, surface): pass

class MenuInicio(EscenaBase):
    def __init__(self, cambiar_escena_cb):
        super().__init__(cambiar_escena_cb)
        info = pygame.display.Info()
        self.ancho, self.alto = info.current_w, info.current_h

        # Música y Estado
        pygame.mouse.set_visible(False)
        pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN])
        
        if not pygame.mixer.get_busy():
            try:
                pygame.mixer.music.load("assets/Assets_Menu_inicio/Audio_menu_inicio.mp3")
                pygame.mixer.music.play(-1)
            except: pass

        # Assets
        try:
            btn_img = pygame.image.load("assets/Assets_Menu_inicio/Boton_Menu_inicio.png").convert_alpha()
            self.fondo = pygame.transform.scale(pygame.image.load("assets/Assets_Menu_inicio/Fondo_Menu_inicio.png"), (self.ancho, self.alto))
        except:
            btn_img, self.fondo = None, pygame.Surface((self.ancho, self.alto))

        # Botones
        x = (self.ancho - 500) // 2
        self.botones = [
            Boton("Iniciar juego", (x, self.alto//2 - 60, 500, 100), AZUL, AZUL_HOVER, lambda: self.cambiar_escena("juego"), btn_img),
            Boton("Salir", (x, self.alto//2 + 80, 500, 100), ROJO, ROJO_HOVER, lambda: pygame.quit() or sys.exit(), btn_img)
        ]
        self.index = 0

    def manejar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_DOWN, pygame.K_s): self.index = (self.index + 1) % len(self.botones)
                if e.key in (pygame.K_UP, pygame.K_w): self.index = (self.index - 1) % len(self.botones)
                if e.key in (pygame.K_RETURN, pygame.K_SPACE): self.botones[self.index].on_click()

    def actualizar(self, dt):
        for i, b in enumerate(self.botones): b.hover = (i == self.index)

    def dibujar(self, surface):
        surface.blit(self.fondo, (0, 0))
        titulo = FUENTE_TITULO.render("Tacos Doña Juana", True, BLANCO)
        surface.blit(titulo, titulo.get_rect(center=(self.ancho//2, self.alto//2 - 200)))
        for b in self.botones: b.draw(surface)