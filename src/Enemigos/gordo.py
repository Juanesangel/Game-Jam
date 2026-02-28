import pygame
import os

#funciones
#Escalar imagen


""""
#Enemigos 
directorio_enemigos = "imagen de los enemigos"
tipo_enemigos= nombres_carpetas(directorio_enemigos)
animaciones_enemigos = []
for eni in tipo_enemigos:
    lista_temp = []
    ruta_temp = eni
    num_animaciones=contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        img_enemigo= pygame.image.load(f"{ruta_temp}//{eni}_{i+1}.png").convert_alpha()
        img_enemigo = escalar_img(img_enemigo,scale 2):
        lista_temp.append(img_enemigo)
    animaciones_enemigos.append(lista_temp)
    
    
#contar elementos
def contar_elementos(directorio):
    return len(os.listdir(directorio))

#Funcion listar nombres elementos
def nombres_carpetas(directorio):
    return os.listdir(directorio)


nombres_carpetas("carpetas")

#cosas para despues 
normal=personaje (x:50,y:50, animaciones_enemgigos[0])
gordo=personaje (x:50,y:50, animaciones_enemgigos[0])

"""