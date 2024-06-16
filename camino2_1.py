import pygame
import random
import sys

pygame.font.init()

X, Y = 50, 28
MITAD_X = X // 2
MITAD_Y = Y // 2
TAMAÑO_BLOQUE = 32
ANCHO, ALTURA = X * TAMAÑO_BLOQUE, Y * TAMAÑO_BLOQUE
VEN = pygame.display.set_mode((ANCHO, ALTURA))

FONT = pygame.font.SysFont("consolas", 20)

COLOR_FONDO = (255, 223, 240)  # BG COLOR
COLOR_TEXTO = (255, 255, 255)  # TexT
COLOR_ROJO = (255, 105, 180)  # RED
COLOR_NODO = (255, 182, 193)  # NODE
COLOR_CUADRICULA = (255, 192, 203)  # Rosa pastel para la cuadrícula

FPS = 40

reloj = pygame.time.Clock()


class Nodo():
    def __init__(self, pos, numero):
        self.pos = pos
        self.numero = numero

    def obtener_pos(self):
        return self.pos

    def obtener_numero(self):
        return self.numero


def dibujar_cuadricula():
    for x in range(1, X):
        pygame.draw.line(VEN, COLOR_CUADRICULA, [x * TAMAÑO_BLOQUE, 0], [x * TAMAÑO_BLOQUE, Y * TAMAÑO_BLOQUE])
    for y in range(1, Y):
        pygame.draw.line(VEN, COLOR_CUADRICULA, [0, y * TAMAÑO_BLOQUE], [X * TAMAÑO_BLOQUE, y * TAMAÑO_BLOQUE])


def dibujar_ventana(nodos, aristas, puntos, ciclo):
    VEN.fill(COLOR_FONDO)

    dibujar_cuadricula()
    dibujar_aristas(nodos, aristas)
    dibujar_ciclo(ciclo)

    pygame.display.update()


def dibujar_ciclo(puntos):
    anterior = puntos[0]
    for punto in puntos:
        pygame.draw.line(VEN, COLOR_ROJO, [punto[0] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2, punto[1] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2], [anterior[0] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2, anterior[1] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2], 4)
        anterior = punto
        reloj.tick(FPS)
        pygame.display.update()
    pygame.draw.line(VEN, COLOR_ROJO, [puntos[0][0] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2, puntos[0][1] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2], [puntos[len(puntos) - 1][0] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2, puntos[len(puntos) - 1][1] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2], 4)


def dibujar_aristas(nodos, aristas):
    for arista in aristas:
        for pos_x in range(0, MITAD_X):
            for pos_y in range(0, MITAD_Y):
                if (nodos[pos_x][pos_y].obtener_numero() == arista[0][0]):
                    inicio = nodos[pos_x][pos_y].obtener_pos()
                if (nodos[pos_x][pos_y].obtener_numero() == arista[0][1]):
                    fin = nodos[pos_x][pos_y].obtener_pos()

        color = (160, 160, 160)

        pygame.draw.line(VEN, color, [inicio[0] * TAMAÑO_BLOQUE, inicio[1] * TAMAÑO_BLOQUE], [fin[0] * TAMAÑO_BLOQUE, fin[1] * TAMAÑO_BLOQUE], 10)
        reloj.tick(FPS)
        pygame.display.update()
    reloj.tick(10)


def crear_nodos():
    nodos = [[Nodo((x * 2 + 1, y * 2 + 1), x + y * MITAD_X) for y in range(0, MITAD_Y)] for x in range(0, MITAD_X)]
    return nodos


def crear_aristas():
    aristas = [[0 for y in range(0, MITAD_Y * MITAD_X)] for x in range(0, MITAD_X * MITAD_Y)]

    saltar = [MITAD_X * x for x in range(0, MITAD_Y)]
    for x in range(0, MITAD_X * MITAD_Y):
        for y in range(0, MITAD_Y * MITAD_X):
            if not (x == y):
                if (x + 1 == y and y not in saltar): aristas[x][y] = random.randint(1, 3)
                elif (x + MITAD_X == y): aristas[x][y] = random.randint(1, 3)

    return aristas


def ciclo_hamiltoniano(nodos, aristas):
    puntos = []
    for arista in aristas:
        for pos_x in range(0, MITAD_X):
            for pos_y in range(0, MITAD_Y):
                if (nodos[pos_x][pos_y].obtener_numero() == arista[0][0]):
                    inicio = nodos[pos_x][pos_y].obtener_pos()
                if (nodos[pos_x][pos_y].obtener_numero() == arista[0][1]):
                    fin = nodos[pos_x][pos_y].obtener_pos()
        puntos.append(inicio)
        puntos.append(((inicio[0] + fin[0]) // 2, (inicio[1] + fin[1]) // 2))
        puntos.append(fin)

    ciclo = [(0, 0)]
    actual = ciclo[0]
    dir = (1, 0)

    while len(ciclo) < X * Y:
        x = actual[0]
        y = actual[1]

        if dir == (1, 0):  # Derecha
            if (x + dir[0], y + dir[1] + 1) in puntos and (x + 1, y) not in puntos:
                actual = (x + dir[0], y + dir[1])
            else:
                dir = (0, 1) if (x, y + 1) in puntos and (x + 1, y + 1) not in puntos else (0, -1)
        elif dir == (0, 1):  # Abajo
            if (x + dir[0], y + dir[1]) in puntos and (x + dir[0] + 1, y + dir[1]) not in puntos:
                actual = (x + dir[0], y + dir[1])
            else:
                dir = (1, 0) if (x, y + 1) in puntos and (x + 1, y + 1) in puntos else (-1, 0)
        elif dir == (-1, 0):  # Izquierda
            if (x, y) in puntos and (x, y + 1) not in puntos:
                actual = (x + dir[0], y + dir[1])
            else:
                dir = (0, -1) if (x, y + 1) not in puntos else (0, 1)
        elif dir == (0, -1):  # Arriba
            if (x, y) not in puntos and (x + 1, y) in puntos:
                actual = (x + dir[0], y + dir[1])
            else:
                dir = (-1, 0) if (x + 1, y) in puntos else (1, 0)
        if actual not in ciclo:
            ciclo.append(actual)

    return puntos, ciclo


def algoritmo_prims(aristas):
    aristas_limpios = []
    for x in range(0, MITAD_X * MITAD_Y):
        for y in range(0, MITAD_Y * MITAD_X):
            if not (aristas[x][y] == 0):
                aristas_limpios.append(((x, y), aristas[x][y]))

    visitados = []
    no_visitados = [x for x in range(MITAD_X * MITAD_Y)]
    actual = 0
    aristas_finales = []

    while len(no_visitados) > 0:
        visitados.append(actual)

        for number in no_visitados:
            if number in visitados:
                no_visitados.remove(number)

        mis_aristas = []
        for arista in aristas_limpios:
            if ((arista[0][0] in visitados or arista[0][1] in visitados) and not (arista[0][0] in visitados and arista[0][1] in visitados)):
                mis_aristas.append(arista)

        min_arista = ((-1, -1), 999)

        for arista in mis_aristas:
            if (arista[1] < min_arista[1]):
                min_arista = arista

        if len(no_visitados) == 0:
            break

        aristas_finales.append(min_arista)

        if min_arista[0][0] == -1:
            actual = no_visitados[0]
        else:
            if (min_arista[0][1] in visitados):
                actual = min_arista[0][0]
            else:
                actual = min_arista[0][1]

    return aristas_finales


def main():
    pygame.display.set_caption("Ciclo Hamiltoniano")

    # Esperar a que se presione una tecla
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                esperando = False
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

    nodos = crear_nodos()
    aristas = crear_aristas()

    aristas_finales = algoritmo_prims(aristas)

    puntos, ciclo = ciclo_hamiltoniano(nodos, aristas_finales)

    dibujar_ventana(nodos, aristas_finales, puntos, ciclo)

    run = True
    while run:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
        reloj.tick(FPS)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
