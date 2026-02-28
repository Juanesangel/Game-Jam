import pygame
import sys
from src.entities import cook as c
from config.window_config import WindowConfig as wc

def main():
    # 1. INICIALIZACIÓN OBLIGATORIA
    pygame.init()
    
    # 2. CONFIGURACIÓN DE VENTANA Y ENUMS
    wc.initialize()
    window = pygame.display.set_mode((wc.WIDTH.value, wc.HEIGHT.value))
    pygame.display.set_caption("Cooking Game: Pro Level")

    # 3. INSTANCIAR EL MINIJUEGO
    cook_minigame = c.Cook()
    
    # --- VARIABLES DE ESTADO Y UI ---
    puntuacion = 0
    fuente_ui = pygame.font.SysFont("Arial", 35, bold=True)
    dificultad_aumentada = False
    
    # Control de tiempo para el cierre automático
    tiempo_limite = 0  
    clock = pygame.time.Clock()

    run = True
    while run:
        # 4. OBTENER TIEMPO ACTUAL
        tiempo_actual = pygame.time.get_ticks()
        
        # Guardamos si estaba activo antes de procesar para detectar el momento del cierre
        estaba_activo_antes = cook_minigame.active

        window.fill("black")

        # --- A. CONTROL DE DIFICULTAD DINÁMICA ---
        if puntuacion >= 10 and not dificultad_aumentada:
            cook_minigame.update_difficulty(use_wasd=True)
            cook_minigame.set_timer_duration(3500) # El tiempo baja a 3.5s al llegar a 10 pts
            dificultad_aumentada = True
        
        elif puntuacion < 10 and dificultad_aumentada:
            # Si el jugador pierde puntos y baja de 10, vuelve a la dificultad inicial
            cook_minigame.available_keys = cook_minigame.arrow_keys.copy()
            cook_minigame.set_timer_duration(5000)
            dificultad_aumentada = False

        # --- B. MANEJO DE EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # El minijuego procesa sus propias teclas (Flechas y WASD)
            cook_minigame.handle_input(event)
            
            # Intento de inicio con SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not cook_minigame.active:
                    cook_minigame.initiate_execution()
                    # Si initiate_execution puso active=True (no estaba bloqueado)
                    if cook_minigame.active:
                        tiempo_limite = tiempo_actual + cook_minigame.timer_duration

        # --- C. LÓGICA DEL MINIJUEGO ---
        if cook_minigame.active:
            # Comprobar si se acabó el tiempo
            if tiempo_actual >= tiempo_limite:
                # Cierra con penalización de 2.5s
                cook_minigame.cease_execution(apply_penalty=True)
            else:
                # Dibuja la interfaz interna (barra de tiempo y teclas)
                cook_minigame.continue_execution(window)

        # --- D. DETECCIÓN DE RESULTADOS Y PUNTUACIÓN ---
        # Si el juego se cerró en este frame:
        if estaba_activo_antes and not cook_minigame.active:
            if tiempo_actual < tiempo_limite:
                # GANÓ: Completó la secuencia a tiempo
                puntuacion += 1
                # Reducción extra de dificultad: cada victoria quita 100ms al timer
                nuevo_tiempo = max(1500, cook_minigame.timer_duration - 100)
                cook_minigame.set_timer_duration(nuevo_tiempo)
            else:
                # PERDIÓ: El timer llegó a cero
                puntuacion = max(0, puntuacion - 1)

        # --- E. DIBUJAR INTERFAZ DE USUARIO (UI) ---
        color_puntos = (0, 255, 0) if puntuacion >= 10 else (255, 255, 255)
        texto_score = fuente_ui.render(f"SCORE: {puntuacion}", True, color_puntos)
        window.blit(texto_score, (30, 30))

        # Mostrar aviso de bloqueo si el jugador falló recientemente
        if not cook_minigame.active and tiempo_actual < cook_minigame.lock_timer:
            restante = (cook_minigame.lock_timer - tiempo_actual) / 1000
            aviso = fuente_ui.render(f"BLOQUEADO: {restante:.1f}s", True, (255, 50, 50))
            window.blit(aviso, (wc.WIDTH.value // 2 - 120, 30))

        pygame.display.flip()
        clock.tick(60) 

if __name__ == "__main__":
    main()