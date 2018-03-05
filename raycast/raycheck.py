# -*- coding: utf-8 -*-

import pygame, sys, os, math
from pygame.locals import *


class Ray():
    X_CTE = 0
    Y_CTE = 1
    def __init__(self):
        #Distancia del punto de partida del ray hasta la colision
        self.distancia=None
        #Coordenadas del punto de colision (tipo float)
        self.collisionPoint=(None,None)
        #Coordenadas del punto de colision en pixels (tipo int)
        self.collisionPixel=(None,None)

    #Dado un vector lo convierte en unitario
    #Param:
    #   (x,y) -> componentes del vector original.
    #Salida: el vector como vector unitario.
    @classmethod
    def getUnitaryVector(cls,(x,y)):
        module = math.sqrt(float(x**2) + y**2)
        return (x/module,y/module)

    #Comprueba si hay alguna colisión con algun sprite del spriteGroup. No devuelve los sprites con los que ha colisionado.
    #Params:
    #   (origenX,origenY)-> coordenadas del punto de origen del ray
    #   dir -> dirección del ray. Se hará transformación a vector unitario.
    #   longitud -> longitud máxima del ray.
    #   spriteGroup -> grupo que contiene los sprites con los que se comprobará la colision.
    #                  IMPORTANTE: los srites deben tener el atributo rect.
    #Salida: True si hay colision (cuando encuentre una colisión ya no comprueba el resto)). False si no hay colisión.
    def anyRayCast(self,(origenX,origenY),dir,longitud,spriteGroup):
                #vector director
                (dirX,dirY)= Ray().getUnitaryVector(dir)
                #punto origen
                p1 = (float(origenX),float(origenY))
                #punto destino
                p2 = (p1[0]+float(dirX)*longitud,p1[1]+float(dirY)*longitud)

                collision = False
                for sprite in spriteGroup:
                    #sprite coordinates
                    left = sprite.rect.left
                    right = sprite.rect.right
                    top  =sprite.rect.top
                    bottom = sprite.rect.bottom
                    if(dirX!=0.0):
                        #lado izquierdo
                        if(self.__check_intersection(p1,p2,(top,bottom),left,Ray.X_CTE)):
                            collision=True
                        #lado derecho
                        if(self.__check_intersection(p1,p2,(top,bottom),right,Ray.X_CTE)):
                            collision= True

                    if(dirY!=0.0):
                        #lado superior
                        if (self.__check_intersection(p1,p2,(left,right),top,Ray.Y_CTE)):
                            collision= True
                        #lado inferior
                        if (self.__check_intersection(p1,p2,(left,right),bottom,Ray.Y_CTE)):
                            collision= True
                return collision

    #comprueba las intersecciones del ray con un lado del rectangulo del objeto sobre el que se comprueba la colision.
    #Params:
    #   p1 -> Punto origen del ray .
    #   p2 -> Punto destino del ray.
    #   (c1,c2) -> dependiendo del lado serán las componentes x o y del lado (definido por rectLine) del rect.
    #               Es decir c1 y c2 definen el segmento de un lado del rect. P.ej: el segmento izquierdo sería c1=y1, c2=y2,
    #               siendo y1 e y2  las componentes y de las esquinas que definen ese lado.
    #   rectLine-> la recta que contiene el lado del rect que se está intersecando, puede ser la recta x=rectLite ó y=rectLine.
    #   side    -> indica si son los lados verticales o horizontales del rect. Sirve para saber si estamos despejando
    #               el param x ó y de las ecuaciones.
    #Salida: True si hay intersección con ese lado, False si no.
    def __check_intersection(self, p1,p2,(c1,c2),rectLine,side):
        # ecuaciones. despejan componentes de las ecuaciones:
        # x = x0 +t*(x1-x0)
        # y = y0+t(y1-y0)

        # devuelve el valor del parametro t
        ec_get_t = lambda a, a1, a2: (a - a1) / (a2 - a1)
        # devuelve el valor de x ó y
        ec_get_param = lambda t, a1, a2: a1 + t * (a2 - a1)

        #Dependiendo de si cogemos los lados del rect verticales o horizontales debemos despejar t con las componentes
        # x ó y de p1 y p2
        if(side==Ray.X_CTE):
            a1=p1[0]
            a2=p2[0]
            b1=p1[1]
            b2=p2[1]
        elif(side==Ray.Y_CTE):
            a1=p1[1]
            a2=p2[1]
            b1=p1[0]
            b2=p2[0]
        else:
            print 'Cannot determine rect side.'
            raise SystemExit

        #Calcula el param t del ray con respecto al lado
        t1=ec_get_t(rectLine, a1, a2)
        #Despeja la otra componente: y si X_CTE, x si Y_CTE
        param = ec_get_param(t1,b1,b2)
        #Calcula el param t del lado con respecto al ray
        t2 = ec_get_t(param,c1,c2)

        if (t1 >= 0 and t1 <= 1 and t2 >= 0 and t2 <= 1):
            if(side==Ray.X_CTE):
                collisionPoint=(rectLine,param)
            elif(side==Ray.Y_CTE):
                collisionPoint = (param,rectLine)
            else:
                print 'Cannot determine rect side.'
                raise SystemExit
            #distancia desde p1 hasta el punto de colision,
            dist = math.sqrt((collisionPoint[0]-p1[0])**2+(collisionPoint[1]-p1[1])**2)
            if(self.distancia==None or dist<self.distancia):
                self.distancia=dist
                self.collisionPoint=collisionPoint
                self.collisionPixel=(int(collisionPoint[0]),int(collisionPoint[1]))
                return True
        return False

    #dibuja en pantalla el ray. No detecta ninguna colisión, solo dibuja.
    #Param:
    #   (origenX,origenY) -> origen del ray.
    #   dir      -> dirección del ray. Se convertirá a vector unitario.
    #   longitud -> longitud del ray.
    #   width    -> ancho del ray.
    #   pantalla -> superficie sobre la que se dibujará el ray.
    #Salida: nada. Solo dibuja.
    def debugRay(self,(origenX,origenY),dir,longitud,color,width,pantalla):
        # vector director
        (dirX, dirY) = Ray().getUnitaryVector(dir)
        # punto origen
        p1 = (float(origenX), float(origenY))
        # punto destino
        p2 = (p1[0] + float(dirX) * longitud, p1[1] + float(dirY) * longitud)
        pygame.draw.line(pantalla,color,p1,p2,width)


#A PARTIR DE AQUI ES EL TEST PARA VER QUE EL MÓDULO FUNCIONA
#colores
BLANCO = (255,255,255)
NEGRO = (0,0,0)
ROJO = (255,0,0)
#tamaño pantalla
PANTALLA_X =800
PANTALLA_Y=600

#Carga una imagen
def load_image(name, colorkey=None):
    fullname = os.path.join('imagenes',name)
    try:
        image=pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

#Clase para los sprites contra los que se comprueban las colisiones
class myRayTestSprite(pygame.sprite.Sprite):
    def __init__(self,posX,posY):
        pygame.sprite.Sprite.__init__(self);
        self.image = load_image("blueSquare.png",None)
        self.rect=self.image.get_rect()
        self.rect.topleft=(posX,posY)

#A partir de un angulo te devuelve el vector director unitario que forma ese ángulo con el eje horizontal.
def getUnitVectorFromAngle(angle):
    x = math.cos(angle)
    y=math.sin(angle)
    #Esto es para evitar numeros muy pequeños cercanos a 0 y que luego no de problemas de division por 0.
    if math.fabs(x) < 0.00001:
        x = 0
    if math.fabs(y) < 0.00001:
        y = 0
    return (x,y)


def test():
    p1 = (PANTALLA_X/2,PANTALLA_Y/2)
    #direccion inicial
    dir=(1,0)
    #longitud inicial
    longitud = 200
    longitudIncrement=1
    angleIncremet=0.02
    angle=0
    pygame.init()

    tipoLetra = pygame.font.SysFont('arial', 12)

    pantalla = pygame.display.set_mode((PANTALLA_X, PANTALLA_Y), 0, 32)
    reloj = pygame.time.Clock()
    pygame.display.set_caption('Test del ray')

    while True:
        reloj.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        teclasPulsadas = pygame.key.get_pressed()

        #La entada puede ser o cambiar el angulo de la dirección o la longitud del rayo
        if teclasPulsadas[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        elif teclasPulsadas[K_LEFT]:
            angle += angleIncremet
            dir = getUnitVectorFromAngle(angle)
        elif teclasPulsadas[K_RIGHT]:
            angle -=angleIncremet
            dir = getUnitVectorFromAngle(angle)
        elif teclasPulsadas[K_UP]:
            longitud+=longitudIncrement
        elif teclasPulsadas[K_DOWN]:
            longitud-= longitudIncrement

        pantalla.fill((0,0,0))
        #se crea un pequeño rect para el punto de origen
        origen = pygame.Rect(p1[0]-2,p1[1]-2,5,5)
        #Los sprites para colisionar
        col =  myRayTestSprite(500,500)
        col1 = myRayTestSprite(10,20)
        col2 = myRayTestSprite(300,150)
        col3 = myRayTestSprite(700,50)
        #Se meten en un grupo
        grupo = pygame.sprite.Group(col,col2,col1,col3)

        grupo.draw(pantalla)
        pygame.draw.rect(pantalla, BLANCO,origen)
        rayo = Ray()
        collision = rayo.anyRayCast(p1,dir,longitud,grupo)
        #Si hay colision se muestra cierta info
        if(collision):
            collisionRect = pygame.Rect(rayo.collisionPoint[0]-2,rayo.collisionPoint[1]-2,5,5)
            pygame.draw.rect(pantalla,BLANCO,collisionRect)
            strval = "Pos: "+str(round(rayo.collisionPoint[0],2))+","+str(round(rayo.collisionPoint[1],2))+"Pixel pos:"+str(rayo.collisionPixel)+"Dist: "+str(rayo.distancia)
            texto = tipoLetra.render(strval, True, BLANCO)
            pantalla.blit(texto, (rayo.collisionPixel[0]+10, rayo.collisionPixel[1]+10, 20, 20))

        rayo.debugRay(p1,dir,longitud,ROJO,1,pantalla)
        pygame.display.update()


if __name__ == "__main__":
    test()