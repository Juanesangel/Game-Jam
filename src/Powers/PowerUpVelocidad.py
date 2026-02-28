import pygame

class PowerUpVelocidad:
    def __init__(self, aumento_velocidad=3, duracion=5000):
        self.aumento_velocidad = aumento_velocidad
        self.duracion = duracion
        self.personaje = None
        self.velocidad_original = 0
        self.tiempo_inicio = 0
        self.activo = False

    def activar(self, personaje):
        self.personaje = personaje
        self.velocidad_original = getattr(personaje, "velocidad", 5.0)
        personaje.velocidad = self.velocidad_original + self.aumento_velocidad
        self.tiempo_inicio = pygame.time.get_ticks()
        self.activo = True

    def actualizar(self):
        if not self.activo or self.personaje is None:
            return

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_inicio >= self.duracion:
            self.personaje.velocidad -= self.aumento_velocidad
            self.activo = False
            self.personaje = None