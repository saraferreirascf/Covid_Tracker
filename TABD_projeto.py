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
import seaborn as sb

<<<<<<< HEAD
=======
# library and dataset
import seaborn as sns

>>>>>>> b97fdb992bdd18c26ced1ad9323e40b2fe46c3ee
ts_i = 1570665600  #timestamp inicial
ts_f = 1570667000

scale=1/3000000
conn = psycopg2.connect("dbname=postgres")
register(conn)
xs_min, xs_max, ys_min, ys_max = -120000, 165000, -310000, 285000
width_in_inches = (xs_max-xs_min)/0.0254*1.1
height_in_inches = (ys_max-ys_min)/0.0254*1.1
cursor_psql = conn.cursor()
fig, ax = plt.subplots(figsize=(width_in_inches*scale, height_in_inches*scale))
ax.axis('off')
ax.set(xlim=(xs_min, xs_max), ylim=(ys_min, ys_max))

font = {'fontname':'Chalkduster'}
#Apple Chancery,Chalkduster, Courier New, Herculanum, Krungthep


#taxi marker
fp = FontProperties(fname=r"./Font Awesome 5 Free-Solid-900.otf")

symbols = dict(taxi = "\uf1ba",car_side= "\uf5e4")


def animate(i):
    fig.suptitle('Covid Tracker', fontsize=16, **font)
    ax.set_title(datetime.datetime.utcfromtimestamp(ts_i+i*10))
    scat.set_facecolors(colors)
    scat.set_offsets(offsets[i])
    return scat

def bar_animate(i):
    global taxis_left_time
    global taxis_infected_time
    height=[taxis_left_time[i],taxis_infected_time[i]]
    print("Tempo: ", i, "Taxis que estao bem: ", height[0], "Taxis que ja foram: ", height[1])
    barlist=plt.barh(y_pos, height)
    barlist[1].set_color('r')
    barlist[0].set_color('g')


def get_marker(symbol):
    v, codes = TextToPath().get_text_path(fp, symbol)
    v = np.array(v)
    mean = np.mean([np.max(v,axis=0), np.min(v, axis=0)], axis=0)
    return Path(v-mean, codes, closed=False)

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

#gráfico com o mapa de portugal
p = random_index() #taxi aleatoriamente escolhido

scat = ax.scatter(offsets[0][p][0],offsets[0][p][1],s=80,c="red",marker=get_marker(symbols["car_side"]),edgecolors="none", linewidth=1)
anim = FuncAnimation(fig, animate, interval=30, frames=len(offsets)-1, repeat = False)


#main#

taxis_left = np.arange(1660) #taxis nao infetados
taxis_infected = [] #taxis infetados
colors = [] #cores
sizes = [] #tamanhos
tempo = []
infetados = []
taxis_left_time = [0] * 8640
taxis_infected_time = [0] * 8640


for c in range(0,1660,1):
    colors.append('green')

for s in range(0,1660,1):
    sizes.append(0)

for tt in range(0,8640,360):
    tempo.append(tt)

#atualizar os arrays

taxis_left = taxis_left[taxis_left != p]
taxis_infected.append(p)
colors.insert(p,'red')
taxis_infected_time.insert(0, 1)
taxis_left_time.insert(0, 1659)

<<<<<<< HEAD
for time in range(0, 4000, 1):
=======
for time in range(0, 1000, 1):
>>>>>>> b97fdb992bdd18c26ced1ad9323e40b2fe46c3ee
    print(time)
    for taxis in taxis_infected: #condicao para fazer o grafico
        temp1=len(taxis_left)
        temp2=len(taxis_infected)
        for t in taxis_left:
            c_taxi = offsets[time][taxis]
            c_t = offsets[time][t]
            if (c_taxi[0] != 0.0 and c_taxi[1] != 0.0):
                inside = isInside(c_taxi[0], c_taxi[1], 50, c_t[0], c_t[1])
                if inside == True:
                    prob = prob_inf()
                    if prob == True:
                        print("Taxi infetado no tempo ", time)
                        taxis_infected.append(t)
                        taxis_left = taxis_left[taxis_left != t]
                        colors.insert(t,'red')
                        taxis_left_time.insert(time, len(taxis_left))
                        taxis_infected_time.insert(time, len(taxis_infected))
                        
    if(len(taxis_left)==temp1 and len(taxis_infected)==temp2): #Se nenhum taxi foi infetado neste tempo
        taxis_left_time.insert(time, len(taxis_left))
        taxis_infected_time.insert(time, len(taxis_infected))

<<<<<<< HEAD
=======


>>>>>>> b97fdb992bdd18c26ced1ad9323e40b2fe46c3ee
#Gráfico de barras
bar_plot=plt.figure()
bar_plot.suptitle("Infected Taxis vs NOT Infected Taxis",**font)
bars=('Healthy Taxis','Infected Taxis')
height=[taxis_left_time[0],taxis_infected_time[0]]
y_pos = np.arange(len(bars))

bar = plt.barh(y_pos, height)
bar[1].set_color('r')
bar[0].set_color('g')
plt.yticks(y_pos, bars)
        
anim_bar = FuncAnimation(bar_plot, bar_animate, interval=30, frames=len(offsets)-1, repeat = False)

<<<<<<< HEAD
#Outro gráfico
graph=plt.figure()
plt.title("Evolution of infection")
plt.plot(taxis_infected_time, color="red", label="infected") 
plt.plot(taxis_left_time, color = "green", label = "healthy")
plt.legend(loc='best')
plt.xlim(0,8640)
plt.xlabel("Time")
plt.ylabel("Number of infected")

#heatmaps
heat = plt.figure()
data = np.asmatrix(taxis_infected_time)   
heat_map = sb.heatmap(data, cmap="Reds")
heat_map.set_yticklabels(heat_map.get_yticklabels(), rotation=0)
ax=plt.gca()
ax.set_xlim(0, 8640)

heat_1 = plt.figure()
data = np.asmatrix(taxis_left_time)   
heat_map = sb.heatmap(data, cmap="Greens")
heat_map.set_yticklabels(heat_map.get_yticklabels(), rotation=0)
ax=plt.gca()
ax.set_xlim(0, 8640)
=======

#Outro gráfico
graph=plt.figure()
plt.plot(taxis_left, color="red", label="infected") 
plt.legend(loc='best')
>>>>>>> b97fdb992bdd18c26ced1ad9323e40b2fe46c3ee

plt.draw()
plt.show()

<<<<<<< HEAD
=======

>>>>>>> b97fdb992bdd18c26ced1ad9323e40b2fe46c3ee
