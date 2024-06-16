import pygame
import random
import ctypes

pygame.font.init()

# Constantes
ANCHO_CELDA, ALTO_CELDA = 50, 28
MITAD_ANCHO = ANCHO_CELDA // 2
MITAD_ALTO = ALTO_CELDA // 2
TAMAÑO_BLOQUE = 32
ANCHO_VENTANA, ALTO_VENTANA = ANCHO_CELDA * TAMAÑO_BLOQUE, ALTO_CELDA * TAMAÑO_BLOQUE
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

# Colores
COLOR_FONDO = (255, 223, 240)     # Fondo rosado claro
COLOR_TEXTO = (255, 255, 255)     # Texto blanco
COLOR_ROJO = (255, 105, 180)      # Rosa fucsia para el ciclo
COLOR_NODO = (255, 182, 193)      # Rosa claro para los nodos
COLOR_CUADRICULA = (255, 192, 203)# Rosa pastel para la cuadrícula
COLOR_BORDE = (160, 160, 160)     # Color gris claro para los bordes

FPS = 60

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
    for x in range(1, ANCHO_CELDA):
        pygame.draw.line(VENTANA, COLOR_CUADRICULA, (x * TAMAÑO_BLOQUE, 0), (x * TAMAÑO_BLOQUE, ALTO_VENTANA))
    for y in range(1, ALTO_CELDA):
        pygame.draw.line(VENTANA, COLOR_CUADRICULA, (0, y * TAMAÑO_BLOQUE), (ANCHO_VENTANA, y * TAMAÑO_BLOQUE))

def dibujar_ventana(nodos, aristas, puntos, ciclo):
    VENTANA.fill(COLOR_FONDO)
    dibujar_cuadricula()
    dibujar_aristas(nodos, aristas)
    dibujar_ciclo(ciclo)
    pygame.display.update()

def dibujar_ciclo(puntos):
    anterior = puntos[0]
    for punto in puntos:
        pygame.draw.line(VENTANA, COLOR_ROJO, (punto[0] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2, punto[1] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2), 
                         (anterior[0] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2, anterior[1] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2), 4)
        anterior = punto
        reloj.tick(FPS)
        pygame.display.update()
    pygame.draw.line(VENTANA, COLOR_ROJO, (puntos[0][0] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2, puntos[0][1] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2), 
                     (puntos[-1][0] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2, puntos[-1][1] * TAMAÑO_BLOQUE + TAMAÑO_BLOQUE // 2), 4)

def dibujar_aristas(nodos, aristas):
    for arista in aristas:
        inicio = None
        fin = None
        for pos_x in range(MITAD_ANCHO):
            for pos_y in range(MITAD_ALTO):
                if nodos[pos_x][pos_y].obtener_numero() == arista[0][0]:
                    inicio = nodos[pos_x][pos_y].obtener_pos()
                if nodos[pos_x][pos_y].obtener_numero() == arista[0][1]:
                    fin = nodos[pos_x][pos_y].obtener_pos()
        if inicio and fin:
            pygame.draw.line(VENTANA, COLOR_BORDE, (inicio[0] * TAMAÑO_BLOQUE, inicio[1] * TAMAÑO_BLOQUE), 
                             (fin[0] * TAMAÑO_BLOQUE, fin[1] * TAMAÑO_BLOQUE), 10)
            reloj.tick(FPS)
            pygame.display.update()
    reloj.tick(30)

def crear_nodos():
    return [[Nodo((x * 2 + 1, y * 2 + 1), x + y * MITAD_ANCHO) for y in range(MITAD_ALTO)] for x in range(MITAD_ANCHO)]

def crear_aristas():
    aristas = [[0 for _ in range(MITAD_ALTO * MITAD_ANCHO)] for _ in range(MITAD_ANCHO * MITAD_ALTO)]
    saltar = [MITAD_ANCHO * x for x in range(MITAD_ANCHO)]
    for x in range(MITAD_ANCHO * MITAD_ALTO):
        for y in range(MITAD_ALTO * MITAD_ANCHO):
            if x != y:
                if x + 1 == y and y not in saltar:
                    aristas[x][y] = random.randint(1, 3)
                elif x + MITAD_ANCHO == y:
                    aristas[x][y] = random.randint(1, 3)
    return aristas

def ciclo_hamiltoniano(nodos, aristas):
    puntos = []
    for arista in aristas:
        inicio = None
        fin = None
        for pos_x in range(MITAD_ANCHO):
            for pos_y in range(MITAD_ALTO):
                if nodos[pos_x][pos_y].obtener_numero() == arista[0][0]:
                    inicio = nodos[pos_x][pos_y].obtener_pos()
                if nodos[pos_x][pos_y].obtener_numero() == arista[0][1]:
                    fin = nodos[pos_x][pos_y].obtener_pos()
        if inicio and fin:
            puntos.append(inicio)
            puntos.append(((inicio[0] + fin[0]) // 2, (inicio[1] + fin[1]) // 2))
            puntos.append(fin)

    ciclo = [(0, 0)]
    actual = ciclo[0]
    direccion = (1, 0)

    while len(ciclo) < ANCHO_CELDA * ALTO_CELDA:
        x, y = actual
        if direccion == (1, 0):  # Derecha
            if (x + direccion[0], y + direccion[1] + 1) in puntos and (x + 1, y) not in puntos:
                actual = (x + direccion[0], y + direccion[1])
            else:
                direccion = (0, 1) if (x, y + 1) in puntos and (x + 1, y + 1) not in puntos else (0, -1)
        elif direccion == (0, 1):  # Abajo
            if (x + direccion[0], y + direccion[1]) in puntos and (x + direccion[0] + 1, y + direccion[1]) not in puntos:
                actual = (x + direccion[0], y + direccion[1])
            else:
                direccion = (1, 0) if (x, y + 1) in puntos and (x + 1, y + 1) in puntos else (-1, 0)
        elif direccion == (-1, 0):  # Izquierda
            if (x, y) in puntos and (x, y + 1) not in puntos:
                actual = (x + direccion[0], y + direccion[1])
            else:
                direccion = (0, -1) if (x, y + 1) not in puntos else (0, 1)
        elif direccion == (0, -1):  # Arriba
            if (x, y) not in puntos and (x + 1, y) in puntos:
                actual = (x + direccion[0], y + direccion[1])
            else:
                direccion = (-1, 0) if (x + 1, y) in puntos else (1, 0)
        if actual not in ciclo:
            ciclo.append(actual)

    return puntos, ciclo

def algoritmo_prims(aristas):
    aristas_limpias = [((x, y), aristas[x][y]) for x in range(MITAD_ANCHO * MITAD_ALTO) for y in range(MITAD_ALTO * MITAD_ANCHO) if aristas[x][y] != 0]
    visitados = []
    no_visitados = list(range(MITAD_ANCHO * MITAD_ALTO))
    actual = 0
    aristas_finales = []

    while no_visitados:
        visitados.append(actual)
        no_visitados = [n for n in no_visitados if n not in visitados]

        mis_aristas = [arista for arista in aristas_limpias if (arista[0][0] in visitados or arista[0][1] in visitados) and not (arista[0][0] in visitados and arista[0][1] in visitados)]
        arista_minima = min(mis_aristas, key=lambda arista: arista[1], default=((0, 0), 999))

        if not mis_aristas:  # Si no hay aristas, romper el bucle
            break

        aristas_finales.append(arista_minima)
        actual = arista_minima[0][0] if arista_minima[0][1] in visitados else arista_minima[0][1]

    return aristas_finales

def poner_ventana_en_primer_plano():
    hwnd = pygame.display.get_wm_info()['window']
    ctypes.windll.user32.SetForegroundWindow(hwnd)

def principal():
    pygame.display.set_caption("Ciclo Hamiltoniano")
    
    poner_ventana_en_primer_plano()
    
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

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

    pygame.quit()

principal()