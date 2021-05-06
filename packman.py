# Código modificado por:
# Autor: Erick Hernández Silva
# Autor: Jeovani Hernández Bastida

# Se importan las librerias a usar
from random import choice, randint
from turtle import *
from freegames import floor, vector

state = {'score': 0}    # Puntuación
path = Turtle(visible=False)    # Dibuja el mapa
writer = Turtle(visible=False)      # Escribe la puntuación
aim = vector(5, 0)  # Movimiento 
pacman = vector(-40, -80)   # Movimiento

# Matriz de vectores   
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

# Muestra el tablero donde 0 es un espacio negro y 1 un espacio azul
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]


def square(x, y):
    """Dibuja los cuadros azules en x, y"""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

def offset(point):
    """Con ayuda de las coordenadas se sabe donde esta el pacman"""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point):
    """
    Nos va regresar valido si el lugar donde se encuentra el pacman 
    es aceptable
    """
    index = offset(point)
    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

def world():
    """Dibuja el mundo usando el path"""
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]
        """
        Si estamos en un cuadro valido lo dibujamos en azul 
        y ponemos el punto blanco
        """
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

def moveGhosts():
    """Mueve los fantasmas"""
    global plan
    # Ciclo que modifica el movimiento de los fantasmas
    for point, course in ghosts:
        #Si el numero aleatorio es 4, modifica la trayectoria
        if(randint(0,5) == 4):
            options = [
                    vector(5, 0),
                    vector(-5, 0),
                    vector(0, 5),
                    vector(0, -5),
                    vector(0,pacman.y/2),
                    vector(pacman.x/2,0)
                ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y
        else:
            # Si el destino es válido, lo hace
            if valid(point + course):
                point.move(course)
            #Si el destino no es válido, elige uno nuevo
            else:
                options = [
                    vector(5, 0),
                    vector(-5, 0),
                    vector(0, 5),
                    vector(0, -5),
                    vector(0,pacman.y/2),
                    vector(pacman.x/2,0)
                ]
                plan = choice(options)
                course.x = plan.x
                course.y = plan.y
        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')  # Dibuja al fantasma
    update()
    # Termina el juego si alguno de los fantamas choca con pacman 
    for point, course in ghosts: 
        if abs(pacman - point) < 20:
            return
    ontimer(moveGhosts, 100)  # Ejecuta el método moveGhosts cada 100ms

def limpiar():
    clear()
    ontimer(limpiar, 100)

def movePacman():
    """Mueve el pacman"""
    writer.undo()
    writer.write(state['score'])
     
    # Si la futura posición del pacman es válida se mueve
    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)  # Indica el indíce de los tiles

    # Acrualiza la puntuación
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1  

        # Dibuja el cuadro sin la bolita blanca
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()    # Mueve el cursor hacia arriba
    goto(pacman.x + 10, pacman.y + 10)  # Nos lleva hacia el pacman en x, y 
    dot(20, 'yellow')   # Dibuja el pacman
    update()
    ontimer(movePacman, 100)  # Ejecuta el método movePacman cada 100ms

def change(x, y):
    """Cambia la dirección del pacman si esta es válida"""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

setup(420, 420, 370, 0) #Crea el canvas
hideturtle()    # Esconde la tortuga
tracer(False)   # Cambia la animación
writer.goto(160, 160)   # Mueve la puntuacion
writer.color('white')   # Cambia el color a blanco 
writer.write(state['score'])    # Cambia la puntación
listen()    # Escucha el teclado en busca de inputs

# Se definen las teclas a presionar para el movimiento del pacman
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')

world()  # Dibuja el mundo
movePacman()  # Mueve por primera vez al pacman
moveGhosts()    # Mueve por primera vez los fantasmas
limpiar()
done()