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

ts_i = 1570665600
ts_f = 1570667000

scale=1/3000000
conn = psycopg2.connect("dbname=postgres")
register(conn)
xs_min, xs_max, ys_min, ys_max = -120000, 165000, -310000, 285000
width_in_inches = (xs_max-xs_min)/0.0254*1.1
height_in_inches = (ys_max-ys_min)/0.0254*1.1
fig, ax = plt.subplots(figsize=(width_in_inches*scale, height_in_inches*scale))
ax.axis('off')
ax.set(xlim=(xs_min, xs_max), ylim=(ys_min, ys_max))
cursor_psql = conn.cursor()

#desenhar mapa#

sql = "select distrito,st_union(proj_boundary) from cont_aad_caop2018 group by distrito"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
xs , ys = [],[]
for row in results:
    geom = row[1]
    if type(geom) is MultiPolygon:
        for pol in geom:
            xys = pol[0].coords
            xs, ys = [],[]
            for (x,y) in xys:
                xs.append(x)
                ys.append(y)
            ax.plot(xs,ys,color='black',lw='0.2')
    if type(geom) is Polygon:
        xys = geom[0].coords
        xs, ys = [],[]
        for (x,y) in xys:
            xs.append(x)
            ys.append(y)
        ax.plot(xs,ys,color='black',lw='0.2')

# taxis #

offsets = []
with open('offsets3.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    i = 0
    for row in reader:
        l = []
        for j in row:
            x,y = j.split()
            x = float(x)
            y= float(y)
            l.append([x,y])
        offsets.append(l)

offsets = np.array(offsets)
x,y = [],[]
for i in offsets[0]:
    x.append(i[0])
    y.append(i[1])

def animate(i):
    ax.set_title(datetime.datetime.utcfromtimestamp(ts_i+i*10))
    scat.set_facecolors(colors)
    scat.set_offsets(offsets[i])
    return scat

#main#

taxis_left = np.arange(1660) #taxis nao infetados
taxis_infected = [] #taxis infetados
colors = [] #cores
sizes = [] #tamanhos
s = 0

p = random_index() #taxi aleatoriamente escolhido

for c in range(0,1660,1):
    colors.append('green')

for s in range(0,1660,1):
    sizes.append(0)

#atualizar os arrays

taxis_left = taxis_left[taxis_left != p]
taxis_infected.append(p)
colors.insert(p,'red')


for time in range(0, 8640, 10):
    print(time)
    for taxis in taxis_infected:
        for t in taxis_left:
            prob = prob_inf()
            if prob == True:
                taxis_infected.append(t)
                taxis_left = taxis_left[taxis_left != t]
                colors.insert(t,'red')

#taxi marker
fp = FontProperties(fname=r"./Font Awesome 5 Free-Solid-900.otf")

symbols = dict(taxi = "\uf1ba",car_side= "\uf5e4")

def get_marker(symbol):
    v, codes = TextToPath().get_text_path(fp, symbol)
    v = np.array(v)
    mean = np.mean([np.max(v,axis=0), np.min(v, axis=0)], axis=0)
    return Path(v-mean, codes, closed=False)
        
scat = ax.scatter(offsets[0][p][0],offsets[0][p][1],s=80,c="red",marker=get_marker(symbols["car_side"]),edgecolors="none", linewidth=1)
anim = FuncAnimation(fig, animate, interval=30, frames=len(offsets)-1, repeat = False)
plt.draw()
plt.show()