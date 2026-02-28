import pygame
import constantes
from  personaje import Personaje
import os
pygame.init()
pygame.display.set_caption("NOMBRE JUEGO")

def escalar_img(image,scale):
  w=image.get_width()
  h=image.get_height()
  nueva_imagen = pygame.transform.scale(image, (w*scale,h*scale))
  return nueva_imagen
from personaje import Personaje
print("Cantidad de argumentos:", Personaje.__init__.__code__.co_argcount)

#importar imagenes
#Personaje
animaciones =[]
for i in range (8):
  BASE_DIR = os.path.dirname(os.path.abspath(__file__))
  img_path = os.path.join(BASE_DIR, "..","assets","Images","characters","Player",f"Personaje_Principal-{i}.png")
  img = pygame.image.load(img_path)
#Arma
# crea el jugador de la clase jugador
jugador = Personaje(250,250,animaciones)
screen = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
# crear un arma de la clase weapon
#controla el frame

reloj =pygame.time.Clock()
run = True
while run == True:
  jugador.update()
  #QUE VAYA A 60 FPS
  reloj.tick(constantes.FPS)
  jugador.dibujar(screen)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      
    
  pygame.display.update()

pygame.quit()