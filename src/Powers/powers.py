import pygame
import random
from Powers.PowerUpVelocidad import PowerUpVelocidad


class SeleccionPowerUp:
    def __init__(self, personaje, enemigos):
        self.personaje = personaje
        self.enemigos = enemigos
        self.activo = False
        self.opciones = []
        self.powerups_activos = []

    def activar_menu(self):
        self.activo = True
        self.opciones = self.generar_opciones()

    def generar_opciones(self):

        posibles = [

            lambda: PowerUpVelocidad(
                aumento_velocidad=random.randint(2, 6)
            ),

        
        ]

        seleccionados = random.sample(posibles, 3)

        return [crear() for crear in seleccionados]

    def manejar_eventos(self, event):
        if not self.activo:
            return

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                indice = event.key - pygame.K_1
                if 0 <= indice < len(self.opciones):
                    p_up = self.opciones[indice]
                    p_up.activar(self.personaje)
                    self.powerups_activos.append(p_up)
                    self.activo = False

    def actualizar(self):
        for p in self.powerups_activos[:]:
            p.actualizar()
            if not p.activo:
                self.powerups_activos.remove(p)

    def dibujar(self, pantalla):
        if not self.activo:
            return

        overlay = pygame.Surface(
            (pantalla.get_width(), pantalla.get_height()),
            pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 180))
        pantalla.blit(overlay, (0, 0))

        fuente = pygame.font.SysFont("Arial", 40, bold=True)

        titulo = fuente.render(
            "¡SELECCIONA UN POWER-UP!",
            True,
            (0, 255, 255)
        )
        pantalla.blit(
            titulo,
            (pantalla.get_width()//2 - titulo.get_width()//2, 100)
        )

        y = 250

        for i, p in enumerate(self.opciones):

            if isinstance(p, PowerUpVelocidad):
                texto = f"{i+1}: Velocidad +{p.aumento_velocidad}"

            else:
                texto = f"{i+1}: PowerUp"

            render = fuente.render(texto, True, (255, 255, 255))
            pantalla.blit(
                render,
                (pantalla.get_width()//2 - render.get_width()//2, y)
            )
            y += 80