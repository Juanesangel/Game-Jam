import pygame
import random
from Powers.PowerUpVelocidad import PowerUpVelocidad
from Powers.PowerUpVida import PowerUpVida 

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
            lambda: PowerUpVelocidad(aumento_velocidad=random.randint(2, 6)),
            lambda: PowerUpVida(cantidad=random.randint(10, 30))
        ]

        # CORRECCIÓN: Seleccionar máximo lo que haya disponible para evitar error de sample
        cantidad_a_pedir = min(len(posibles), 3)
        seleccionados = random.sample(posibles, cantidad_a_pedir)

        return [crear() for crear in seleccionados]

    def manejar_eventos(self, event):
        if not self.activo:
            return

        if event.type == pygame.KEYDOWN:
            # Soporte para teclado normal y numérico
            teclas = {
                pygame.K_1: 0, pygame.K_KP1: 0,
                pygame.K_2: 1, pygame.K_KP2: 1,
                pygame.K_3: 2, pygame.K_KP3: 2
            }
            
            if event.key in teclas:
                indice = teclas[event.key]
                if 0 <= indice < len(self.opciones):
                    p_up = self.opciones[indice]
                    p_up.activar(self.personaje)
                    self.powerups_activos.append(p_up)
                    self.activo = False

    def actualizar(self):
        for p in self.powerups_activos[:]:
            if hasattr(p, 'actualizar'):
                p.actualizar()
                if not p.activo:
                    self.powerups_activos.remove(p)
            else:
                # Instantáneos (Vida) se quitan tras aplicar
                self.powerups_activos.remove(p)

    def dibujar(self, pantalla):
        if not self.activo:
            return

        overlay = pygame.Surface((pantalla.get_width(), pantalla.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        pantalla.blit(overlay, (0, 0))

        fuente = pygame.font.SysFont("Arial", 40, bold=True)
        titulo = fuente.render("¡SELECCIONA UN POWER-UP!", True, (0, 255, 255))
        pantalla.blit(titulo, (pantalla.get_width()//2 - titulo.get_width()//2, 100))

        y = 250
        for i, p in enumerate(self.opciones):
            if isinstance(p, PowerUpVelocidad):
                texto = f"{i+1}: Velocidad +{p.aumento_velocidad}"
            elif isinstance(p, PowerUpVida):
                texto = f"{i+1}: Curar +{p.cantidad} Vida"
            else:
                texto = f"{i+1}: Mejora"

            render = fuente.render(texto, True, (255, 255, 255))
            pantalla.blit(render, (pantalla.get_width()//2 - render.get_width()//2, y))
            y += 80