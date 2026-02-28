import pygame
import sys

# Colores básicos
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

def scale_height_keep_aspect(surf, target_h):
    """Escala una superficie manteniendo la relación de aspecto basada en la altura."""
    w, h = surf.get_size()
    if h == 0: return surf
    new_w = int(w * (target_h / h))
    return pygame.transform.smoothscale(surf, (new_w, target_h))

def wrap_text(texto, fuente, max_ancho):
    """Divide el texto en líneas que quepan en el ancho especificado."""
    palabras = texto.split(" ")
    lineas, linea = [], ""
    for p in palabras:
        prueba = (linea + (" " if linea else "") + p)
        if fuente.size(prueba)[0] <= max_ancho: 
            linea = prueba
        else:
            if linea: lineas.append(linea)
            linea = p
    if linea: lineas.append(linea)
    return lineas

class EscenaCinematica:
    def __init__(self, cambiar_escena_cb, ancho, alto, ruta_fondo=None, ruta_abuela="assets/cinematics/abuela.png", fuente_nombre=None, fuente_dialogo=None, cps=40):
        self.cambiar_escena = cambiar_escena_cb
        self.ANCHO, self.ALTO = ancho, alto
        pygame.mouse.set_visible(False)
        pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL])

        # Configuración de fuentes
        self.fuente_nombre = fuente_nombre or pygame.font.SysFont("arial", 40, bold=True)
        self.fuente_dialogo = fuente_dialogo or pygame.font.SysFont("arial", 60)

        # Carga de fondo
        self.fondo = None
        if ruta_fondo:
            try:
                img = pygame.image.load(ruta_fondo).convert()
                self.fondo = pygame.transform.scale(img, (self.ANCHO, self.ALTO))
            except Exception as e: 
                print(f"Error cargando fondo: {e}")

        # Configuración de la caja de texto
        self.margen = 20
        self.altura_caja = int(self.ALTO * 0.25)
        self.rect_caja = pygame.Rect(self.margen, self.ALTO - self.altura_caja - self.margen, self.ANCHO - 2 * self.margen, self.altura_caja)

        # Carga del retrato de la abuela
        self.retrato = None
        self.retrato_rect = None # Inicializamos explícitamente como None
        try:
            retr = pygame.image.load(ruta_abuela).convert_alpha()
            self.retrato = scale_height_keep_aspect(retr, int(self.rect_caja.height * 0.8))
            self.retrato_rect = self.retrato.get_rect(left=self.rect_caja.left + 16, bottom=self.rect_caja.bottom - 16)
        except Exception as e: 
            print(f"Aviso: No se pudo cargar el retrato ({e}). Se continuará sin imagen.")

        # Ajuste del área de texto según si hay retrato o no
        espacio_izq = self.retrato_rect.right + 16 if self.retrato_rect else self.rect_caja.left + 16
        self.rect_texto = pygame.Rect(espacio_izq, self.rect_caja.top + 18, self.rect_caja.right - 16 - espacio_izq, self.rect_caja.height - 36)

        # Diálogos originales mantenidos
        self.dialogos = [
            {"speaker": "Abuela (Tú)", "text": "Ay mi niño... me duele el alma decírtelo, pero hoy amanecimos con la alacena vacía."},
            {"speaker": "Nieto", "text": "No se preocupe, abuelita. Yo sé que la cosa está difícil en la ciudad."},
            {"speaker": "Abuela (Tú)", "text": "La plata ya no alcanza para nada y las ventas de empanadas han estado flojas... No sé qué vamos a comer hoy."},
            {"speaker": "Nieto", "text": "Entonces hoy no se va sola. Yo voy con usted al puesto para ayudarle con los pedidos."},
            {"speaker": "Abuela (Tú)", "text": "¡Ni lo pienses! La calle está muy dura y la gente en Bogotá mantiene con un afán terrible. Te pueden lastimar."},
            {"speaker": "Nieto", "text": "Pero abuela, si llegan todos al tiempo se le arma un desorden. Entre los dos despachamos más rápido."},
            {"speaker": "Abuela (Tú)", "text": "Eres muy terco, igualito a tu abuelo... Está bien, pero te me quedas cerquita. ¡Vamos a ver si hoy la suerte nos cambia!"},
            {"speaker": "Nieto", "text": "¡Esa es la actitud! Póngase el delantal, que hoy no se nos quema ni una empanada."}
        ]

        # Lógica de animación de texto
        self.idx, self.cps, self.chars_visibles, self.t_acum, self.linea_completa = 0, cps, 0, 0.0, False
        self.t_blink, self.indicador_visible, self.t_entrada = 0.0, True, 0.0

    def manejar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.QUIT: 
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if self.t_entrada < 0.2: continue
                if e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if not self.linea_completa:
                        self.chars_visibles = len(self.dialogos[self.idx]["text"])
                        self.linea_completa = True
                    else:
                        self.idx += 1
                        if self.idx >= len(self.dialogos): 
                            self.cambiar_escena("juego")
                        else: 
                            self.t_acum, self.chars_visibles, self.linea_completa = 0.0, 0, False

    def actualizar(self, dt):
        self.t_entrada += dt
        if self.idx < len(self.dialogos):
            txt = self.dialogos[self.idx]["text"]
            if not self.linea_completa:
                self.t_acum += dt * self.cps
                self.chars_visibles = min(int(self.t_acum), len(txt))
                if self.chars_visibles >= len(txt): 
                    self.linea_completa = True
        
        # Animación del indicador "Enter"
        self.t_blink += dt
        if self.t_blink >= 0.5: 
            self.t_blink, self.indicador_visible = 0.0, not self.indicador_visible

    def dibujar(self, surface):
        # Dibujar fondo
        if self.fondo: 
            surface.blit(self.fondo, (0, 0))
        else: 
            surface.fill((20, 25, 35))
        
        # Dibujar caja de diálogo (semi-transparente)
        panel = pygame.Surface(self.rect_caja.size, pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))
        surface.blit(panel, self.rect_caja.topleft)
        pygame.draw.rect(surface, (255, 255, 255), self.rect_caja, width=2, border_radius=12)

        # CORRECCIÓN: Solo dibujar el retrato si ambos objetos existen
        if self.retrato and self.retrato_rect: 
            surface.blit(self.retrato, self.retrato_rect.topleft)
            pygame.draw.rect(surface, (255, 255, 255), self.retrato_rect.inflate(8, 8), width=2, border_radius=10)

        # Dibujar texto
        if self.idx < len(self.dialogos):
            # Nombre del hablante
            speaker = self.dialogos[self.idx]["speaker"]
            placa = self.fuente_nombre.render(speaker, True, BLANCO)
            surface.blit(placa, (self.rect_caja.left + 20, self.rect_caja.top - 40))

            # Contenido del diálogo
            texto_actual = self.dialogos[self.idx]["text"][:self.chars_visibles]
            lineas = wrap_text(texto_actual, self.fuente_dialogo, self.rect_texto.width)
            
            y = self.rect_texto.top
            for l in lineas:
                txt_surf = self.fuente_dialogo.render(l, True, BLANCO)
                surface.blit(txt_surf, (self.rect_texto.left, y))
                y += txt_surf.get_height() + 6

            # Indicador para continuar
            if self.linea_completa and self.indicador_visible:
                tip = self.fuente_nombre.render("▶ Enter", True, BLANCO)
                surface.blit(tip, tip.get_rect(bottomright=(self.rect_caja.right - 12, self.rect_caja.bottom - 10)))

if __name__ == "__main__":
    pygame.init()
    info = pygame.display.Info()
    ANCHO, ALTO = info.current_w, info.current_h
    VENTANA = pygame.display.set_mode((ANCHO, ALTO))
    CLOCK = pygame.time.Clock()
    
    # Prueba local de la escena
    escena = EscenaCinematica(lambda n: sys.exit(), ANCHO, ALTO, ruta_fondo="assets/Assets_Menu_inicio/Conversacion.jpeg")
    
    while True:
        dt = CLOCK.tick(60) / 1000.0
        eventos = pygame.event.get()
        escena.manejar_eventos(eventos)
        escena.actualizar(dt)
        escena.dibujar(VENTANA)
        pygame.display.flip()