import pygame
import random
from Powers.PowerUpVelocidad import PowerUpVelocidad

class SeleccionPowerUp:
    def __init__(self, personaje):
        self.personaje = personaje
        self.activo = False
        self.opciones = []
        self.powerups_activos = [] # Lista para manejar duraciones de los que ya se eligieron

    def activar_menu(self):
        self.activo = True
        self.opciones = self.generar_opciones()

    def generar_opciones(self):
        posibles_aumentos = [2, 3, 4, 5, 6]
        opciones = []
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
                    p_up = self.opciones[indice]
                    p_up.activar(self.personaje)
                    self.powerups_activos.append(p_up) # Se va a la lista de ejecución
                    self.activo = False

    def actualizar(self):
        # Actualizamos solo los que están en curso
        for p in self.powerups_activos[:]:
            p.actualizar()
            if not p.activo:
                self.powerups_activos.remove(p)

    def dibujar(self, pantalla):
        if not self.activo:
            return

        # Overlay semi-transparente para el menú
        overlay = pygame.Surface((pantalla.get_width(), pantalla.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        pantalla.blit(overlay, (0,0))

        fuente = pygame.font.SysFont("Arial", 40, bold=True)
        titulo = fuente.render("¡SELECCIONA UN POWER-UP!", True, (0, 255, 255))
        pantalla.blit(titulo, (pantalla.get_width()//2 - titulo.get_width()//2, 100))

        y = 250
        for i, p in enumerate(self.opciones):
            texto = f"Presiona {i+1}: Velocidad +{p.aumento_velocidad}"
            render = fuente.render(texto, True, (255, 255, 255))
            pantalla.blit(render, (pantalla.get_width()//2 - render.get_width()//2, y))
            y += 80