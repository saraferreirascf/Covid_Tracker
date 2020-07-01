import numpy as np; np.random.seed(32)
import matplotlib.pyplot as plt
import psycopg2
import math
from matplotlib.animation import FuncAnimation
import datetime
import csv
from postgis import Polygon,MultiPolygon
from postgis.psycopg import register
from Functions_project import *
import sys
import random
from matplotlib.path import Path
from matplotlib.textpath import TextToPath
from matplotlib.font_manager import FontProperties
from matplotlib import style



###########
# DISPLAY #
###########
def polygon_to_points(polygon_string):
    xs, ys = [],[]
    points = polygon_string[9:-2].split(',')
    for point in points:
        (x,y) = point.split()
        xs.append(float(x))
        ys.append(float(y))
    return xs,ys

def linestring_to_points(line_string):
    xs, ys = [],[]
    points = line_string[11:-2].split(',')
    for point in points:
        (x,y) = point.split()
        xs.append(float(x))
        ys.append(float(y))
    return xs,ys

#####################
# GENERAL FUNCTIONS #
#####################

#obter os taxis de forma random
def random_index():
    return random.randint(0,1660)


#ver os taxis que estao dentro do circulo de infecao
def isInside(circle_x, circle_y, rad, x, y): 
    if ((x - circle_x) * (x - circle_x) + 
        (y - circle_y) * (y - circle_y) <= rad * rad): 
        return True
    else: 
        return False

def prob_inf():
    prob = random.randint(0,100)
    if prob < 10:
        return True
    else:
        return False

def infected(offsets, index):
    print("taxi a infetar = ", index)
    inf_color = []
    taxis_inf = []
    all_t = []
    for j in range(0, 500, 10): #precorre o tempo
        print(j)
        for k in range(0,1659,1):
            c= offsets[j][index] #coordenadas do taxi infetado no tempo j
            for i in offsets[j]: #precorre os offsets
                if (c[0] != 0.0 and c[1] != 0.0): #para garantir que nao estao no ponto 0.0
                    inside = isInside(c[0], c[1], 50, i[0], i[1])
                    if inside == True:
                        prob = prob_inf()
                        if (prob == True) and ( k not in taxis_inf):
                            taxis_inf.append(k)
                            inf_color.append('red')
                        else:
                            inf_color.append('green')
    t = len(taxis_inf)
    all_t.append(t)
    return taxis_inf, inf_color, all_t

def bar_chart(barss, sizes):
    height = sizes
    bars = barss
    y_pos = np.arange(len(bars)) 
    # Create bars
    plt.bar(y_pos, height)
    # Create names on the x-axis
    plt.xticks(y_pos, bars)
    # Show graphic
    plt.show()
