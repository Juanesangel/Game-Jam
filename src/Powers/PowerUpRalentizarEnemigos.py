import pygame
class PowerUpRalentizarEnemigos:
    def __init__(self, factor=0.5, duracion=5000):
        self.factor = factor
        self.duracion = duracion
        self.enemigos = []
        self.velocidades_originales = []
        self.tiempo_inicio = 0
        self.activo = False

    def activar(self, enemigos):
        if self.activo:
            return

        self.enemigos = enemigos
        self.velocidades_originales = []

        for e in enemigos:
            self.velocidades_originales.append(e.velocidad)
            e.velocidad *= self.factor

        self.tiempo_inicio = pygame.time.get_ticks()
        self.activo = True

    def actualizar(self):
        if not self.activo:
            return

        if pygame.time.get_ticks() - self.tiempo_inicio >= self.duracion:
            for i, e in enumerate(self.enemigos):
                e.velocidad = self.velocidades_originales[i]

            self.activo = False