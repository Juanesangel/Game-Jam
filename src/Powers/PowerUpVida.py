import pygame
class PowerUpVida:
    def __init__(self, cantidad=20):
        self.cantidad = cantidad

    def activar(self, personaje):
        personaje.vida += self.cantidad