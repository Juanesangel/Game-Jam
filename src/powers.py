import pygame
import random
from Powers.PowerUpVelocidad import PowerUpVelocidad
class SeleccionPowerUp:
    def __init__(self, personaje):
        self.personaje = personaje
        self.activo = False
        self.opciones = []

    def activar_menu(self):
        """Genera opciones aleatorias cada vez que aparece el menú"""
        self.activo = True
        self.opciones = self.generar_opciones()

    def generar_opciones(self):
        """Crea 3 powerups aleatorios"""
        posibles_aumentos = [2, 4, 6, 8, 10]
        opciones = []

        # Elegimos 3 valores sin repetir
        valores = random.sample(posibles_aumentos, 3)

        for valor in valores:
            opciones.append(PowerUpVelocidad(aumento_velocidad=valor))

        return opciones

    def manejar_eventos(self, event):
        if not self.activo:
            return

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                indice = event.key - pygame.K_1

                if 0 <= indice < len(self.opciones):
                    self.opciones[indice].activar(self.personaje)
                    self.activo = False

    def actualizar(self):
        for powerup in self.opciones:
            powerup.actualizar()

    def dibujar(self, pantalla):
        if not self.activo:
            return

        fuente = pygame.font.Font(None, 50)
        pantalla.fill((0, 0, 0))

        y = 200

        for i, powerup in enumerate(self.opciones):
            texto = f"{i+1} - Velocidad +{powerup.aumento_velocidad}"
            render = fuente.render(texto, True, (255, 255, 255))
            pantalla.blit(render, (200, y))
            y += 60

        pygame.display.flip()