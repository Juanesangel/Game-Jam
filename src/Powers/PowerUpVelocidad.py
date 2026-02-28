import pygame


class PowerUpVelocidad:
    def __init__(self, aumento_velocidad=3, duracion=5000):
        """
        aumento_velocidad -> incremento de velocidad
        duracion -> tiempo activo en milisegundos
        """
        self.aumento_velocidad = aumento_velocidad
        self.duracion = duracion

        self.personaje = None
        self.velocidad_original = None
        self.tiempo_inicio = 0
        self.activo = False

    def activar(self, personaje):
        # Evita activar el powerup si ya está activo
        if self.activo:
            return

        self.personaje = personaje
        self.velocidad_original = getattr(personaje, "velocidad", 0)

        # Aumentamos velocidad solo una vez
        personaje.velocidad = self.velocidad_original + self.aumento_velocidad

        self.tiempo_inicio = pygame.time.get_ticks()
        self.activo = True

    def actualizar(self):
        if not self.activo or self.personaje is None:
            return

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.tiempo_inicio >= self.duracion:
            # Restauramos exactamente al valor original
            self.personaje.velocidad = self.velocidad_original

            # Limpiamos referencias
            self.personaje = None
            self.activo = False