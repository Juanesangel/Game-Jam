import pygame
from enum import Enum

class WindowConfig(Enum):
    # Valores iniciales (se sobreescribirán)
    WIDTH = 0
    HEIGHT = 0

    @classmethod
    def initialize(cls):
        """Actualiza los valores del Enum con la resolución real del monitor"""
        info = pygame.display.Info()
        # Modificamos el atributo interno '_value_' para actualizar el Enum en ejecución
        cls.WIDTH._value_ = info.current_w
        cls.HEIGHT._value_ = info.current_h