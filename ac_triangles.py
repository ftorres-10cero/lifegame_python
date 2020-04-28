#
# DotCSV 28/04/2020 Autómatas celulares
# (https://www.twitch.tv/dotcsv)
# Doc: http://thehardmenpath.blogspot.com/2014/03/simbolos-42.html?m=1

import pygame
import numpy as np
import time

pygame.init()

width, height = 800, 800

bg = 0,0,0

screen  = pygame.display.set_mode((height, width), pygame.RESIZABLE)
screen.fill(bg)

# Tamaño de nuestra matriz
nxC, nyC = 400, 400

# Estado de las celdas. Viva = 1 / Muerta = 0
gameState = np.zeros((nxC,  nyC))

#dimensiones de cada celda individual
dimCW = width / nxC
dimCH = height / nyC

# Oscilador.
gameState[int(nxC/2), 0] = 1

pauseExect = False

# rule = np.random.randint(156)
# print("Rule: "+str(rule)+" "+np.binary_repr(rule, width = 8))

rule = 110

rules = list(np.binary_repr(rule, width = 8))
rules.reverse()

for y in range(0, nxC):
    for x in range(0, nyC):
        # Calculamos el polígono que forma la celda.
        poly = [((x) * dimCW, y * dimCH),
                ((x + 1) * dimCW, y * dimCH),
                ((x + 1) * dimCW, (y + 1) * dimCH),
                ((x) * dimCW, (y + 1) * dimCH)]

#        pygame.draw.polygon(screen, (40, 40, 40), poly, 1)

y = 0

# Bucle de ejecución
while y < nyC:

    # Copiamos la matriz del estado anterior
    # #para representar la matriz en el nuevo estado
    newGameState = np.copy(gameState)

    # Registramos eventos de teclado y ratón.
    ev = pygame.event.get()

    # Cada vez que identificamos un evento lo procesamos
    for event in ev:
        # Detectamos si se presiona una tecla.
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        # Detectamos si se presiona el ratón.
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = 1

    for x in range (0, nxC):

        if not pauseExect:

            ruleIdx = 4 * gameState[(x-1) % nxC ,y] + 2 * gameState[x,y] + 1 * gameState[(x+1) % nxC, y]

            newGameState[x, (y+1) % nyC] = rules[int(ruleIdx)]

        # Calculamos el polígono que forma la celda.
        poly = [((x)   * dimCW, y * dimCH),
                ((x+1) * dimCW, y * dimCH),
                ((x+1) * dimCW, (y+1) * dimCH),
                ((x)   * dimCW, (y+1) * dimCH)]

        # Si la celda está "muerta" pintamos un recuadro con borde gris
        if newGameState[x, y] == 1:
#            pygame.draw.polygon(screen, (40, 40, 40), poly, 0)
        # Si la celda está "viva" pintamos un recuadro relleno de color
 #       else:
            pygame.draw.polygon(screen, (200, 100, 100), poly, 0)

    #time.sleep(0.1)

    if y >= nyC:
        pauseExect = True
    elif not pauseExect:
        y = y + 1

    time.sleep(0.1)

    # Actualizamos el estado del juego.
    gameState = np.copy(newGameState)

    # Mostramos el resultado
    pygame.display.flip()


while True:
    time.sleep(0.1)
    print("end")