# cinematica_intro.py
import pygame
import sys

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

def scale_height_keep_aspect(surf, target_h):
    """Escala una Surface a una altura target conservando proporción."""
    w, h = surf.get_size()
    if h == 0:
        return surf
    new_w = int(w * (target_h / h))
    return pygame.transform.smoothscale(surf, (new_w, target_h))

def wrap_text(texto, fuente, max_ancho):
    """
    Divide el texto en varias líneas sin superar max_ancho.
    Retorna una lista de líneas.
    """
    palabras = texto.split(" ")
    lineas = []
    linea = ""
    for p in palabras:
        prueba = (linea + (" " if linea else "") + p)
        if fuente.size(prueba)[0] <= max_ancho:
            linea = prueba
        else:
            if linea:
                lineas.append(linea)
            linea = p
    if linea:
        lineas.append(linea)
    return lineas

class EscenaCinematica:
    """
    Mini-cinemática con retrato de la abuela y cuadro de diálogo con efecto typewriter.
    Navegación: Enter (completar/avanzar), ESC (volver al menú).
    Al terminar todos los diálogos -> cambiar_escena('juego')
    """
    def __init__(self, cambiar_escena_cb, ancho, alto,
                 
                 ruta_fondo=None, ruta_abuela="assets/cinematics/abuela.png",
                 fuente_nombre=None, fuente_dialogo=None,
                 cps=40):
        """
        - cambiar_escena_cb: callback para cambiar escena
        - ancho, alto: dimensiones de la ventana
        - ruta_fondo: imagen opcional de fondo de la escena
        - ruta_abuela: retrato de la abuela (PNG con alpha recomendado)
        - fuente_nombre, fuente_dialogo: pygame.font.Font opcionales
        - cps: caracteres por segundo del efecto máquina de escribir
        """
        self.cambiar_escena = cambiar_escena_cb
        self.ANCHO = ancho
        self.ALTO = alto

        # Opciones de entrada
        pygame.mouse.set_visible(False)
        pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL])

        #Fuentes
        self.fuente_nombre = fuente_nombre or pygame.font.SysFont("arial", 26, bold=True)
        self.fuente_dialogo = fuente_dialogo or pygame.font.SysFont("arial", 28)

        # Fondo
        self.fondo = None
        if ruta_fondo:
            try:
                img = pygame.image.load(ruta_fondo).convert()
                self.fondo = pygame.transform.scale(img, (self.ANCHO, self.ALTO))
            except Exception as e:
                print(f" No se pudo cargar fondo de cinemática: {e}")

        # Overlay para separar el cuadro de diálogo
        self.overlay = pygame.Surface((self.ANCHO, self.ALTO), pygame.SRCALPHA)

        # Caja de diálogo (en la parte inferior)
        self.margen = 20
        self.altura_caja = int(self.ALTO * 0.1)
        self.rect_caja = pygame.Rect(
            self.margen, self.ALTO - self.altura_caja - self.margen,
            self.ANCHO - 2 * self.margen, self.altura_caja
        )

        self.retrato = None
        self.retrato_rect = None
        if ruta_abuela:
            try:
                retrato_img = pygame.image.load(ruta_abuela).convert_alpha()
                retrato_img = scale_height_keep_aspect(retrato_img, int(self.rect_caja.height * 0.8))

                # Colocar retrato en la izquierda de la caja
                self.retrato = retrato_img
                self.retrato_rect = retrato_img.get_rect()
                self.retrato_rect.left = self.rect_caja.left + 16
                self.retrato_rect.bottom = self.rect_caja.bottom - 16
            except Exception as e:
                print(f" No se pudo cargar retrato de abuela: {e}")

        # Área de texto
        if self.retrato:
            espacio_izq = (self.retrato_rect.right + 16)
        else:
            espacio_izq = self.rect_caja.left + 16
        self.rect_texto = pygame.Rect(
            espacio_izq,
            self.rect_caja.top + 18,
            self.rect_caja.right - 16 - espacio_izq,
            self.rect_caja.height - 36
        )

        # Diálogos
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

        # Estado de la narrativa
        self.idx = 0
        self.cps = cps
        self.chars_visibles = 0
        self.t_acum = 0.0
        self.linea_completa = False

        # Parpadeo del indicador "Enter"
        self.t_blink = 0.0
        self.indicador_visible = True

        # Evitar doble Enter al entrar
        self.t_entrada = 0.0
        self.bloqueo_ms = 180

    # ---------------- LÓGICA ----------------
    def manejar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:

                # Pequeño bloqueo al llegar
                if self.t_entrada < self.bloqueo_ms / 1000.0:
                    continue

                if e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    texto_actual = self.dialogos[self.idx]["text"]
                    if not self.linea_completa:
                        # Completa de golpe la línea actual
                        self.chars_visibles = len(texto_actual)
                        self.linea_completa = True
                    else:
                        # Avanza al siguiente diálogo
                        self.idx += 1
                        if self.idx >= len(self.dialogos):
                            # Cinemática terminada -> a juego
                            self.cambiar_escena("juego")
                            return
                        # Reset para la siguiente línea
                        self.t_acum = 0.0
                        self.chars_visibles = 0
                        self.linea_completa = False

    def actualizar(self, dt):
        self.t_entrada += dt

        # Typewriter
        if self.idx < len(self.dialogos):
            texto_actual = self.dialogos[self.idx]["text"]
            if not self.linea_completa:
                self.t_acum += dt * self.cps
                nuevos = int(self.t_acum)
                if nuevos > self.chars_visibles:
                    self.chars_visibles = min(nuevos, len(texto_actual))
                    if self.chars_visibles >= len(texto_actual):
                        self.linea_completa = True

        # Parpadeo indicador
        self.t_blink += dt
        if self.t_blink >= 0.5:
            self.t_blink = 0.0
            self.indicador_visible = not self.indicador_visible

    # ---------------- DIBUJO ----------------
    def dibujar(self, surface):
       
        # Fondo
        if self.fondo:
            surface.blit(self.fondo, (0, 0))
        else:
            surface.fill((20, 25, 35))

        # Caja de diálogo
        panel = pygame.Surface(self.rect_caja.size, pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))
        surface.blit(panel, self.rect_caja.topleft)

        # Borde del panel
        pygame.draw.rect(surface, (255, 255, 255), self.rect_caja, width=2, border_radius=12)

        # Retrato
        if self.retrato and self.retrato_rect:
            surface.blit(self.retrato, self.retrato_rect.topleft)

            # Pequeño borde alrededor del retrato
            pygame.draw.rect(surface, (255, 255, 255), self.retrato_rect.inflate(8, 8), width=2, border_radius=10)

        # Nombre del hablante
        if self.idx < len(self.dialogos):
            speaker = self.dialogos[self.idx]["speaker"]
            placa = self.fuente_nombre.render(speaker, True, BLANCO)
            placa_bg = pygame.Surface((placa.get_width() + 14, placa.get_height() + 8), pygame.SRCALPHA)
            placa_bg.fill((0, 0, 0, 180))

            # Nombre del que habla
            pos_placa = (self.rect_caja.left + 20, self.rect_caja.top - 50)
            surface.blit(placa_bg, pos_placa)
            surface.blit(placa, (pos_placa[0] + 7, pos_placa[1] + 4))

            # Text
            texto_completo = self.dialogos[self.idx]["text"]
            texto_visible = texto_completo[:self.chars_visibles]

            lineas = wrap_text(texto_visible, self.fuente_dialogo, self.rect_texto.width)

            y = self.rect_texto.top
            for linea in lineas:
                
                # Sombra sutil
                sombra = self.fuente_dialogo.render(linea, True, (0, 0, 0))
                surface.blit(sombra, (self.rect_texto.left + 2, y + 2))
                
                # Texto
                txt = self.fuente_dialogo.render(linea, True, BLANCO)
                surface.blit(txt, (self.rect_texto.left, y))
                y += txt.get_height() + 6  # interlineado

            # Indicador para continuar
            if self.linea_completa and self.indicador_visible:
                tip = self.fuente_nombre.render("▶ Enter", True, BLANCO)
                tip_rect = tip.get_rect(bottomright=(self.rect_caja.right - 12, self.rect_caja.bottom - 10))
                surface.blit(tip, tip_rect)




if __name__ == "__main__":
    import pygame
    import sys

    pygame.init()

    # --- Config de ventana de prueba ---
    info = pygame.display.Info()

    ANCHO, ALTO = info.current_w, info.current_h
    VENTANA = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Preview - Cinemática Abuela")

    CLOCK = pygame.time.Clock()
    FPS = 20

    # Callback falso para "cambiar_escena".
    # En la preview, al "cambiar" a 'menu' o 'juego' simplemente salimos.
    def dummy_cambiar_escena(nombre):
        print(f"[Preview] cambiar_escena('{nombre}') -> cerrando preview")
        pygame.quit()
        sys.exit()

    # Escena de cinemática.
    try:
        escena = EscenaCinematica(
            cambiar_escena_cb=dummy_cambiar_escena,
            ancho=ANCHO,
            alto=ALTO,
            ruta_fondo="assets/Assets_Menu_inicio/Conversacion.jpeg", 
            cps=40  # velocidad del efecto máquina de escribir
        )
    except Exception as e:
        print(f"[Preview] Error creando la escena: {e}")
        pygame.quit()
        sys.exit(1)

    # Loop principal de preview
    while True:
        dt = CLOCK.tick(FPS) / 1000.0
        eventos = pygame.event.get()

        escena.manejar_eventos(eventos)
        escena.actualizar(dt)
        escena.dibujar(VENTANA)
        pygame.display.flip()