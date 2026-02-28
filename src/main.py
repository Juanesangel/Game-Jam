import pygame
import sys
import os
from src.entities import cook as c
from config.window_config import WindowConfig as wc
from src import personaje
from src import weapon

def main():
    pygame.init()
    
    # 1. Inicializamos Config y CREAMOS LA VENTANA con tamaño exacto
    wc.initialize()
    pantalla_ancho = wc.WIDTH
    pantalla_alto = wc.HEIGHT
    window = pygame.display.set_mode((pantalla_ancho, pantalla_alto))
    pygame.display.set_caption("Cooking Game: Centered Pro")

    # 2. Instanciamos el minijuego
    cook_minigame = c.Cook()
    
    puntuacion = 0
    fuente_ui = pygame.font.SysFont("Arial", 35, bold=True)
    dificultad_aumentada = False
    tiempo_limite = 0  
    clock = pygame.time.Clock()

    def escalar_img(image, scale):
        return pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))

    # -------- CARGA DE RECURSOS --------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    animaciones = []
    for i in range(8):
        img_path = os.path.join(BASE_DIR, "..", "assets", "Images", "characters", "Player", f"Personaje_Principal-{i}.png")
        img = pygame.image.load(img_path).convert_alpha()
        animaciones.append(escalar_img(img, wc.SCALA_PERSONAJE))

    img_path_arma = os.path.join(BASE_DIR, "..", "assets", "Images", "weapons", "Empanada.png")
    imagen_pistola = pygame.image.load(img_path_arma).convert_alpha()
    imagen_pistola = escalar_img(imagen_pistola, wc.SCALA_ARMA)

    # -------- OBJETOS --------
    jugador = personaje.Personaje(50, 50, animaciones)
    pistola = weapon.Weapon(imagen_pistola)

    run = True
    while run:
        tiempo_actual = pygame.time.get_ticks()
        estaba_activo_antes = cook_minigame.active

        window.fill((30, 30, 30))

        # Dificultad Dinámica
        if puntuacion >= 10 and not dificultad_aumentada:
            cook_minigame.update_difficulty(use_wasd=True)
            cook_minigame.set_timer_duration(3500)
            dificultad_aumentada = True
        elif puntuacion < 10 and dificultad_aumentada:
            cook_minigame.update_difficulty(use_wasd=False)
            cook_minigame.set_timer_duration(5000)
            dificultad_aumentada = False

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            cook_minigame.handle_input(event)
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not cook_minigame.active:
                    if cook_minigame.initiate_execution():
                        tiempo_limite = tiempo_actual + cook_minigame.get_timer()

        # Personaje (Mundo)
        if not cook_minigame.active:
            keys = pygame.key.get_pressed()
            dx = (keys[pygame.K_d] - keys[pygame.K_a]) * 5
            dy = (keys[pygame.K_s] - keys[pygame.K_w]) * 5
            jugador.movimiento(dx, dy)
        
        jugador.update()
        pistola.update(jugador)
        jugador.dibujar(window)
        pistola.dibujar(window)

        # Minijuego (Pasamos la superficie 'window' exacta)
        if cook_minigame.active:
            if tiempo_actual >= tiempo_limite:
                cook_minigame.cease_execution(apply_penalty=True)
            else:
                cook_minigame.continue_execution(window)

        # Resultados de puntuación
        if estaba_activo_antes and not cook_minigame.active:
            if tiempo_actual < tiempo_limite:
                puntuacion += 1
                cook_minigame.set_timer_duration(max(1500, cook_minigame.timer_duration - 100))
            else:
                puntuacion = max(0, puntuacion - 1)

        # UI y Textos (Centrado con la pantalla real)
        txt_score = fuente_ui.render(f"SCORE: {puntuacion}", True, (255,255,255))
        window.blit(txt_score, (30, 30))

        if not cook_minigame.active and tiempo_actual < cook_minigame.lock_timer:
            restante = (cook_minigame.lock_timer - tiempo_actual) / 1000
            aviso = fuente_ui.render(f"ESPERA: {restante:.1f}s", True, (255, 80, 80))
            # Usamos pantalla_ancho de main
            window.blit(aviso, (pantalla_ancho // 2 - aviso.get_width() // 2, 80))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()