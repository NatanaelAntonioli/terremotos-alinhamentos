# Essa versão apenas exibe uma matriz de alinhamentos para uma data escolhida.

from astropy.coordinates import SkyCoord
from sunpy.coordinates import get_body_heliographic_stonyhurst
from astropy.time import Time
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
from IPython.display import display

def alinhamento(timestr='2017-03-18T07:54:00.005'):
    obstime = Time(timestr) + 0 * u.day
    print(obstime)
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

    fig = plt.figure()
    ax1 = plt.subplot()
    for k in planet_coord_new:
        if k[2] == 'sun':
            plt.plot(k[0], k[1], 'x', label=k[2])
        else:
            plt.plot(k[0], k[1], 'o', label=k[2])
    plt.legend()
    plt.show()


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

    for i in range(10):
        print(planet_list[i] + "-" + str(i))

    matriz_d_dataframe = pd.DataFrame(matriz_d)
    display(matriz_d_dataframe)

    matriz_binaria_dataframe = pd.DataFrame(matriz_binaria)
    display(matriz_binaria_dataframe)

alinhamento()