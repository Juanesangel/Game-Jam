import pygame
import sys

# Colores básicos
BLANCO = (255, 255, 255)
AZUL, AZUL_HOVER = (70, 140, 240), (90, 160, 255)
ROJO, ROJO_HOVER = (220, 60, 60), (240, 90, 90)

pygame.font.init()
FUENTE_TITULO = pygame.font.SysFont("Sabo-filled.oft", 85, bold=True)
FUENTE_BOTON = pygame.font.SysFont("PressStar2P-Regular.ttf", 50, bold=True)

class Boton:
    def __init__(self, texto, rect, color_base, color_hover, on_click, imagen_fondo=None):
        self.texto = texto
        self.rect = pygame.Rect(rect)
        self.on_click = on_click
        self.hover = False
        
        if imagen_fondo:
            self.imagen_base = pygame.transform.smoothscale(imagen_fondo, self.rect.size)
            self.brillo = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            self.brillo.fill((255, 255, 255, 60))
            mask = pygame.mask.from_surface(self.imagen_base)
            mask_surf = mask.to_surface(setcolor=(255, 255, 255, 60), unsetcolor=(0, 0, 0, 0))
            self.brillo = mask_surf
        else:
            self.imagen_base = None

    def draw(self, surface):
        if self.imagen_base:
            surface.blit(self.imagen_base, self.rect.topleft)
            if self.hover:
                surface.blit(self.brillo, self.rect.topleft)
        else:
            pygame.draw.rect(surface, (100, 100, 100), self.rect, border_radius=12)

        txt = FUENTE_BOTON.render(self.texto, True, (255, 255, 255))
        surface.blit(txt, txt.get_rect(center=self.rect.center))


class EscenaBase:
    def __init__(self, cambiar_escena_cb): self.cambiar_escena = cambiar_escena_cb
    def manejar_eventos(self, eventos): pass
    def actualizar(self, dt): pass
    def dibujar(self, surface): pass

class MenuInicio(EscenaBase):
    def __init__(self, cambiar_escena_cb):
        super().__init__(cambiar_escena_cb)
        info = pygame.display.Info()
        self.ancho, self.alto = info.current_w, info.current_h
        
        # --- MÚSICA DEL MENÚ 
        self._musica_menu_path = "assets/Assets_Menu_inicio/Audio_Menu_inicio.mp3"           
        self._musica_activa = False                                       
        try:                                                               
            if not pygame.mixer.get_init():                                
                pygame.mixer.init()                                        
            pygame.mixer.music.load(self._musica_menu_path)              
            pygame.mixer.music.set_volume(0.4)  # 0.0–1.0                  
            # Reproduce en loop con un pequeño fade-in                      
            pygame.mixer.music.play(-1, fade_ms=400)                        
            self._musica_activa = True                                      
        except pygame.error as e:                                           
            print(f"[ADVERTENCIA] Música del menú no disponible: {e}")     
        

        # Carga de Imágenes
        try:
            btn_img = pygame.image.load("assets/Assets_Menu_inicio/Boton_Menu_inicio.png").convert_alpha()
            self.fondo = pygame.image.load("assets/Assets_Menu_inicio/Fondo_Menu_inicio.png").convert()
            self.fondo = pygame.transform.scale(self.fondo, (self.ancho, self.alto))
        except Exception as e:
            print(f"Error cargando imágenes: {e}")
            btn_img = None
            self.fondo = pygame.Surface((self.ancho, self.alto))
            self.fondo.fill((30, 30, 30))

        x = (self.ancho - 500) // 2

        # Callbacks que apagan la música ANTES de cambiar/ salir             # >>>
        def _go_intro():                                                    # >>>
            self._apagar_musica_menu(fade_ms=500)                           # >>>
            self.cambiar_escena("introduccion")                             # >>>
        def _salir():                                                       # >>>
            self._apagar_musica_menu(fade_ms=400)                           # >>>
            sys.exit()                                                      # >>>

        self.botones = [
            Boton("Iniciar juego", (x, self.alto//2 - 60, 500, 100), AZUL, AZUL_HOVER, 
                  _go_intro, imagen_fondo=btn_img),                         # >>>
            Boton("Salir", (x, self.alto//2 + 80, 500, 100), ROJO, ROJO_HOVER, 
                  _salir, imagen_fondo=btn_img)                             # >>>
        ]
        self.index = 0

    # Método utilitario para apagar la música del menú                       
    def _apagar_musica_menu(self, fade_ms=400):                             
        if pygame.mixer.get_init() and self._musica_activa:                 
            try:                                                            
                if fade_ms and fade_ms > 0:                                 
                    pygame.mixer.music.fadeout(fade_ms)                     
                else:                                                       
                    pygame.mixer.music.stop()                               
            except Exception:                                              
                pass                                                        
            self._musica_activa = False                                     

    def manejar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_DOWN, pygame.K_s): 
                    self.index = (self.index + 1) % len(self.botones)
                if e.key in (pygame.K_UP, pygame.K_w): 
                    self.index = (self.index - 1) % len(self.botones)
                if e.key in (pygame.K_RETURN, pygame.K_SPACE): 
                    self.botones[self.index].on_click()

    def actualizar(self, dt):
        for i, b in enumerate(self.botones): 
            b.hover = (i == self.index)

    def dibujar(self, surface):
        surface.blit(self.fondo, (0, 0))
        titulo = FUENTE_TITULO.render("La Arepona", True, BLANCO)
        surface.blit(titulo, titulo.get_rect(center=(self.ancho//2, self.alto//2 - 200)))
        for b in self.botones: 
            b.draw(surface)