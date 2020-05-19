import numpy as np
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

def animate(i):
    ax.set_title(datetime.datetime.utcfromtimestamp(ts_i+i*10))
    sizes = np.random.randint(50,size=1660) #infe 
    #colors = np.random.random(size=(1660,3))
    scat.set_facecolors(inf_color)
    scat.set_offsets(offsets[i]) 

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


inf_color= []
index = random_index()
index1 = random_index()
index2 = random_index()
for i in range(0,1659):
    if i == index or i == index1 or i == index2:
        inf_color.append('red')
    else:
        inf_color.append('green')



scat = ax.scatter(x,y,s=2)

anim = FuncAnimation(fig, animate, interval=10, frames=len(offsets)-1, repeat = False)
plt.draw()
plt.show()

