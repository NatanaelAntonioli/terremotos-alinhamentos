import datetime
import ephem
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
from IPython.display import display

date = datetime.datetime(2010, 1, 1) + datetime.timedelta(days=10)

m = ephem.Moon(date)


s = (3652,2)
matriz = np.zeros(s)

for i in range(3652):
    date = datetime.datetime(2010, 1, 1) + datetime.timedelta(days=i)
    m = ephem.Moon(date)
    fase = m.moon_phase
    matriz[i][0] = fase
    
    datestr = str(date).replace(" 00:00:00", "")
    print(datestr)

    if datestr in open('terremotos.txt', encoding="utf8").read():
        matriz[i][1] = 1



s = (4)
numero_dias = np.zeros(s)
numero_terremotos = np.zeros(s)
x = np.zeros(s)
aleatorio = np.zeros(s)

k = 0
for j in x:
    j = k
    k = k +1

for i in matriz:
    valor_lua = round(i[0] * 100)
    if valor_lua <= 25:
        fase = 0
    elif valor_lua <= 50:
        fase = 1
    elif valor_lua <= 75:
        fase = 2
    elif valor_lua <= 100:
        fase = 3

    numero_terremotos[fase] = numero_terremotos[fase] + i[1]
    numero_dias[fase] = numero_dias[fase] + 1

print("Número de dias em cada fração iluminada: ")
print(numero_dias)
print("Número de terremotos em cada dia: ")
print(numero_terremotos)

date = datetime.datetime(2010, 1, 1) + datetime.timedelta(days=0)
m = ephem.Moon(date)

# Produz um conjunto de 30 matrizes aleatórias, com 30% de chance de terremoto

amostras = 30

matrizes = []
for i in range(amostras):
    aleatorio = np.zeros(s)
    #print(i)
    for i in range(3652):
        date = datetime.datetime(2010, 1, 1) + datetime.timedelta(days=i)
        m = ephem.Moon(date)
        fase = m.moon_phase
        valor_lua = round(fase * 100)
    
        if valor_lua <= 25:
            fase = 0
        elif valor_lua <= 50:
            fase = 1
        elif valor_lua <= 75:
            fase = 2
        elif valor_lua <= 100:
            fase = 3


        if random.random() <= 0.30:
            aleatorio[fase] = aleatorio[fase] + 1
    matrizes.append(aleatorio)
    
matriz_media = np.zeros(s)
matriz_desvio = np.zeros(s)

for i in matrizes:
    matriz_media = matriz_media + i
matriz_media = matriz_media/amostras


for i in matrizes:  
    matriz_desvio = matriz_desvio + np.square(i - matriz_media)

matriz_desvio = matriz_desvio / amostras
matriz_desvio = matriz_desvio**0.5

#print(matriz_media)
#print(matriz_desvio)

matriz_diferencas = abs(numero_terremotos - matriz_media)
matriz_diferencas_norm = np.divide(matriz_diferencas, matriz_desvio)

pd.set_option('display.float_format', lambda x: '%.2f' % x)
print("Matriz de desvios em relação à média: ")
print(matriz_diferencas_norm)