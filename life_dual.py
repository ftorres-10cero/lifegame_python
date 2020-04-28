import pygame
import numpy as np
import time

pygame.init()

width, height = 800, 800
screen  = pygame.display.set_mode((height, width))

bg = 25, 25, 25

screen.fill(bg)

nxC, nyC = 25, 25

dimCW = width / nxC
dimCH = height / nyC


# Estado de las celdas. Viva = 1 / Muerta = 0
gameState = np.zeros((nxC,  nyC))


# Autómata palo.

gameState[5, 3] = 1
gameState[4, 4] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1
gameState[6, 5] = 1

# Autómata mancha.
gameState[11, 11] = -1
gameState[12, 12] = -1
gameState[12, 11] = -1
gameState[10, 11] = -1
gameState[11, 12] = -1
gameState[12, 13] = -1

pauseExect = False

# Bucle de ejecución
while True:

    newGameState = np.copy(gameState)

    time.sleep(0.1)

    screen.fill(bg)

    # Registramos eventos de teclado y ratón.
    ev = pygame.event.get()

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

    for y in range(0, nxC):
        for x in range (0, nyC):

            if not pauseExect:

                # Calculamos el número de vecinos cercanos.
                n_neigh =   gameState[(x - 1) % nxC, (y - 1)  % nyC] + \
                            gameState[(x)     % nxC, (y - 1)  % nyC] + \
                            gameState[(x + 1) % nxC, (y - 1)  % nyC] + \
                            gameState[(x - 1) % nxC, (y)      % nyC] + \
                            gameState[(x)     % nxC, (y)      % nyC] + \
                            gameState[(x + 1) % nxC, (y)      % nyC] + \
                            gameState[(x - 1) % nxC, (y + 1)  % nyC] + \
                            gameState[(x)     % nxC, (y + 1)  % nyC] + \
                            gameState[(x + 1) % nxC, (y + 1)  % nyC]

                # Regla #1 : Una celda muerta con más 3 vecinas vivas, "revive".

                if gameState[x, y] == 0 and n_neigh > 3:
                    newGameState[x, y] = 1

                # Regla #2 : Una celda viva con menos de 2 o 3 vecinas vinas, "muere".

                elif gameState[x, y] == 0 and (n_neigh < -2):
                    newGameState[x, y] = -1

                elif gameState[x, y] == 1 and (n_neigh < 1 or n_neigh > 5):
                    newGameState[x, y] = 0

                elif gameState[x, y] == -1 and (n_neigh < -5 or n_neigh > -1):
                    newGameState[x, y] = 0

                # Regla #3 : Una celda viva con menos de 2 o 3 vecinas vinas, "muere".



            # Calculamos el numero de vecinos cercanos.
            poly = [((x)   * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x)   * dimCW, (y+1) * dimCH)]

            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            elif newGameState[x, y] == 1:
                pygame.draw.polygon(screen, (0, 175, 0), poly, 0)
            else:
                pygame.draw.polygon(screen, (175, 0, 0), poly, 0)

    # Actualizamos el estado del juego.

    gameState = np.copy(newGameState)

    pygame.display.flip()