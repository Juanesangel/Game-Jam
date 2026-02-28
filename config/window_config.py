import pygame

class WindowConfig:
    # Definimos los atributos con valores por defecto (Placeholder)
    WIDTH = 0
    HEIGHT = 0

    # Personaje
    ALTO_PEROSNAJE = 50
    ANCHO_PERSONAJE = 50
    SCALA_PERSONAJE = 0.25
    COLOR_PERSONAJE = (255, 255, 0)
    
    # FPS
    FPS = 60 # Subí esto a 60 para que el juego vaya fluido

    SCALA_ENEMIGO=0.01


    SCALA_COCINA=2.5

    @classmethod
    def initialize(cls):
        """Actualiza la resolución con la del monitor real."""
        if not pygame.display.get_init():
            pygame.display.init()
            
        info = pygame.display.Info()
        
        # Asignación directa (Sin .value ni ._value_)
        cls.WIDTH = info.current_w
        cls.HEIGHT = info.current_h