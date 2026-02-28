import sys
import os

# Esto asegura que Python encuentre la carpeta 'src' correctamente
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import JuegoMotor

if __name__ == "__main__":
    try:
        # Inicializamos y ejecutamos
        app = JuegoMotor()
        app.run()
    except Exception as e:
        print("\n--- ERROR CRÍTICO AL INICIAR EL JUEGO ---")
        print(f"Detalle: {e}")
        input("\nPresiona Enter para cerrar...") # Evita que la ventana desaparezca