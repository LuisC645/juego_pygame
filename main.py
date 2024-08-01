import pygame
import random
import math
from pygame import mixer
import os

#inicializar pygame
pygame.init()

# Ruta
path = os.getcwd()

#crear pantalla
screen=pygame.display.set_mode((800,600))

#musica de fondo 
mixer.music.load(path + '/media/MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

#Titulo e icono
pygame.display.set_caption('Invasion Espacial')
icono=pygame.image.load(path + '/images/ovni.png')
pygame.display.set_icon(icono)


#fondo
img_fondo=pygame.image.load(path + '/images/Fondo.jpg')


#texto finalament

fuente_final=pygame.font.Font('freesansbold.ttf',40) 

def texto_final():

    font=fuente_final.render('Juego Terminado',True,(255,255,255))
    screen.blit(font,(60,200))


#balas
img_balas=pygame.image.load(path + '/images/bala.png')
bala_x=0
bala_y=500
bala_x_cambio=0
bala_y_cambio=1
bala_visible=False

def disparar_bala(x,y):
    global bala_visible
    bala_visible=True
    screen.blit(img_balas,(x+16,y+10))


#jugador 
img_jugador=pygame.image.load(path + '/images/cohete.png')
jugador_x=368
jugador_y=500

x_cambio=0

#mostrar jugador
def jugador(x,y):
    screen.blit(img_jugador,(x,y))


#enemigo
img_enemigo=[]
enemigo_x=[]
enemigo_y=[]
enemigo_x_cambio=[]
enemigo_y_cambio=[]
cantidad_enemigos=5

for i in range(cantidad_enemigos):

    img_enemigo.append(pygame.image.load(path + '/images/enemigo.png'))
    enemigo_x.append(random.randint(0,726))
    enemigo_y.append(random.randint(50,200))

    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

#mostrar enemigo
def enemigo(x,y,i):
    screen.blit(img_enemigo[i],(x,y))                                               


#detectar coliciones
def hay_colision(x1,y1,x2,y2):
    distancia=math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))
    if distancia<27:
        return True
    else:
        return False


#puntaje
puntaje=0

fuente=pygame.font.Font('freesansbold.ttf',32)
txt_x=10
txt_y=10

def mostrar_puntaje(x,y):
    texto=fuente.render(f'Puntaje: {puntaje}',True,(255,255,255))
    screen.blit(texto,(x,y))


#loop juego
se_ejecuta=True;

while se_ejecuta:

    #color pantalla
    screen.blit(img_fondo,(0,0))    

    for evento in pygame.event.get():

        #salir del juego
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        #mover jugador - mapear teclas        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                x_cambio = -0.3

            if evento.key == pygame.K_RIGHT:
                x_cambio = 0.3


            #disparar con espacio
            if evento.key == pygame.K_SPACE:
                sonar_bala=mixer.Sound(path + '/media/disparo.mp3')
                sonar_bala.set_volume(0.5)
                sonar_bala.play()
                if bala_visible==False:
                    bala_x=jugador_x
                    disparar_bala(bala_x,bala_y)

            
        if evento.type == pygame.KEYUP:
            if evento.type == pygame.K_LEFT or evento.type == pygame.K_RIGHT:
                x_cambio = 0
            

    #cambio de movimiento del jugador
    jugador_x+=x_cambio

    #limites de movimiento del jugador
    if jugador_x<=0:
        x_cambio=0
    elif jugador_x>=736:
        jugador_x=736


    #modificar cambio enemigo_x
    for i in range(cantidad_enemigos):

        #fin juego
        if enemigo_y[i]>=500:
            for j in range(cantidad_enemigos):
                enemigo_y[j]=1000
            texto_final()
            break; 

        enemigo_x[i]+=enemigo_x_cambio[i]

        #limites de movimiento del enemigo
        if enemigo_x[i]<=0:
            enemigo_x_cambio[i]=0.3
            enemigo_y[i]+=enemigo_y_cambio[i]
        elif enemigo_x[i]>=736:
            enemigo_x_cambio[i]=-0.3
            enemigo_y[i]+=enemigo_y_cambio[i]


        #colision
        colision=hay_colision(enemigo_x[i],enemigo_y[i],bala_x,bala_y)
        if colision:
            sonar_colision=mixer.Sound(path + '/media/golpe.mp3')
            sonar_colision.play()
            bala_y=500
            bala_visible=False
            puntaje+=1
            enemigo_x[i]=random.randint(0,736)
            enemigo_y[i]=random.randint(50,200)
            
        #enemigo
        enemigo(enemigo_x[i],enemigo_y[i],i)

    
    #movimiento bala
    if bala_y<=-64:
        bala_y=500
        bala_visible=False

    if bala_visible:
        disparar_bala(bala_x,bala_y)
        bala_y-=bala_y_cambio


    #jugador
    jugador(jugador_x,jugador_y)  

    #mostrar Puntaje
    mostrar_puntaje(txt_x,txt_y)


    pygame.display.update()
    