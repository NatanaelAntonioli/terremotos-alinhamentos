# Essa versão apenas exibe uma matriz de alinhamentos para uma data escolhida.

from datetime import date
from astropy.coordinates import SkyCoord
from sunpy.coordinates import get_body_heliographic_stonyhurst
from astropy.time import Time
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
from IPython.display import display
import random
import scipy.stats

def alinhamento(offset):
    f = open("arquivo.txt", "a")

    timestr='2010-01-01T07:54:00.005'
    obstime = Time(timestr) + offset * u.day
    #print(obstime)
    planet_list = ['earth','sun','mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune','moon']
    planet_coord = [get_body_heliographic_stonyhurst(this_planet, time=obstime) for this_planet in planet_list]

    planet_coord_new = []

    i = 0
    for current in planet_coord:
        planeta = [0, 0, 0]
        current = str(current)
        current = current.split("(")[4]
        current = current.replace(")>", "")
        current = current.split(",")
        for k in range(3):
            current[k] = float(current[k])
        x = np.deg2rad(current[0])
        r = current[2]
        xp = math.cos(x) * r
        yp = math.sin(x) * r
        name = planet_list[i]

        planeta[0] = xp
        planeta[1] = yp
        planeta[2] = name

        i = i + 1

        planet_coord_new.append(planeta)

    terra = np.array([planet_coord_new[0][0],planet_coord_new[0][1]])

    s = (10,10)
    matriz_d = np.zeros(s)
    matriz_binaria = np.zeros(s)

    for i in range(9):
        p1 = planet_coord_new[i+1]
        planeta1 = np.array([p1[0], p1[1]])

        for j in range(9):
            if i != j:
                p2 = planet_coord_new[j+1]
                planeta2 = np.array([p2[0], p2[1]])

                d = np.cross(planeta2 - planeta1, terra - planeta1) / np.linalg.norm(planeta2 - planeta1)
                d = abs(d)
                matriz_d[i+1][j+1] = d
                if i != 8 and j != 8 and d < 0.01 and i != j:
                    matriz_binaria[i+1][j+1] = 1
                if (i == 8 or j == 8) and d < 0.00035 and i != j:
                    matriz_binaria[i+1][j+1] = 1

    np.set_printoptions(precision=4)
    np.set_printoptions(suppress=True)

    matriz_d_dataframe = pd.DataFrame(matriz_d)
    #display(matriz_d_dataframe)

    matriz_binaria_dataframe = pd.DataFrame(matriz_binaria)
    #display(matriz_binaria_dataframe)

    return matriz_binaria_dataframe



s = (10,10)

matriz_cumulativa = np.zeros(s)
matriz_cumulativa_terremotos = np.zeros(s)
pd.set_option('display.precision', 1)

"""
# Primeiro, calculamos a cumulativa para todos os dias do período
for i in range(3650+2):

    timestr='2010-01-01T07:54:00.005'
    obstime = Time(timestr) + i * u.day

    datestr = str(obstime).replace('T07:54:00.005','')
    print("Calculando cumulativa" + datestr)
    matriz_dia = alinhamento(i)

    matriz_cumulativa = matriz_cumulativa + matriz_dia

print("Matriz cumulativa total: ")
matriz_cumulativa_dataframe = pd.DataFrame(matriz_cumulativa)
display(matriz_cumulativa_dataframe)

"""

# Depois, calculamos a cumulativa para os dias do período com terremotos, e contamos quantos são
total = 0
for i in range(3650+2):

    timestr='2010-01-01T07:54:00.005'
    obstime = Time(timestr) + i * u.day
    datestr = str(obstime)[:10]

    if datestr in open('terremotos.txt', encoding="utf8").read():
        print("Checando data:" + datestr)
        matriz_dia = alinhamento(i)
        matriz_cumulativa_terremotos = matriz_cumulativa_terremotos + matriz_dia
        total = total +1

matriz_cumulativa_dataframe_terremotos = pd.DataFrame(matriz_cumulativa_terremotos)
print("Matriz cumulativa para terremotos: ")
print(total)
display(matriz_cumulativa_dataframe_terremotos)

print("Matriz comulativa esperada: ")
matriz_cumulativa_esperada = matriz_cumulativa * total/3652
display(matriz_cumulativa_esperada)

print("Matriz de diferenças: ")
matriz_diferencas = matriz_cumulativa_esperada - matriz_cumulativa_terremotos
display(matriz_diferencas)

# Agora, fazemos nossa amostragem aleatória

amostras = 30
matrizes = []

for i in range(amostras):
    print(i)
    matriz_cumulativa_terremotos_hip = np.zeros(s)

    for j in range(1131):
        offset = random.randint(0, 3652)
        timestr='2010-01-01T07:54:00.005'
        obstime = Time(timestr) + offset * u.day
        matriz_dia = alinhamento(offset)
        matriz_cumulativa_terremotos_hip = matriz_cumulativa_terremotos_hip + matriz_dia
    
    matrizes.append(matriz_cumulativa_terremotos_hip)

matriz_media= np.zeros(s)
matriz_desvio = np.zeros(s)

# Prepara a matriz de medias
for i in matrizes:
    matriz_media = matriz_media + i
matriz_media = matriz_media / amostras

# Prepara a matriz de desvios
for i in matrizes:  
    matriz_desvio = matriz_desvio + np.square(i - matriz_media)




matriz_desvio = matriz_desvio / amostras
matriz_desvio = matriz_desvio**0.5

print("Media calculada: ")
display(matriz_media)
print("Desvio calculado: ")
display(matriz_desvio)

matriz_diferencas = abs(matriz_cumulativa_terremotos - matriz_media)
matriz_diferencas_norm = np.divide(matriz_diferencas, matriz_desvio)

matriz_diferencas_norm = pd.DataFrame(matriz_diferencas_norm)

pd.set_option('display.float_format', lambda x: '%.2f' % x)
display(matriz_diferencas_norm)