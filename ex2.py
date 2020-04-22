#1 ponto a cada 100s, colocar numa matriz os pontos de cada carro sincronizados pelo ts e offsets
#sincronizar todos os trajetos em termos de tempos comuns.
#matriz index ts index carro, em q o carro vai ter uma lista com os pontos

#offsets sao sequencias de posicoes para o mesmo objeto.
#vamos ter posicoes diferentes em frames diferetes da mesma animacao
#precisamos de ter listas q tenham as coordenadas x,y em sequencia, mas para os dif pontos tempos de sincronizar temporalmente.
#Sincronização 
#Aplicar o ts, para a linestring representada na proj_track tem como tempo ts + n. Temos de criar uma estrutura que baseada no ts e no comprimento da linestring coloque no ponto certo dessa estrutura para cada identificador de táxi 

import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import math
from matplotlib.animation import FuncAnimation
def animate(i):
    scat.set_offsets([taxis_x[20000333],taxis_y[20000333]])
    scat.set_offsets([taxis_x[20012018],taxis_y[20012018]])

def linestring_to_points(line_string):
    xs, ys = [],[]
    points = line_string[11:-1].split(',')
    for point in points:
        (x,y) = point.split()
        xs.append(float(x))
        ys.append(float(y))
    return xs,ys

scale=1/60000
conn = psycopg2.connect("dbname=postgres")
cursor_psql = conn.cursor()

xs_min, xs_max, ys_min, ys_max = -50000, -30000, 160000, 172000
width_in_inches = (xs_max-xs_min)/0.0254*1.1
height_in_inches = (ys_max-ys_min)/0.0254*1.1
fig, ax = plt.subplots(figsize=(width_in_inches*scale, height_in_inches*scale))
ax.set(xlim=(xs_min, xs_max), ylim=(ys_min, ys_max))

taxis_x ={}
taxis_y ={}
ts_i = 1570665600
ts_f = 1570752000
 
taxis_x[int(20000333)] = np.zeros(8640)
taxis_y[int(20000333)] = np.zeros(8640)
taxis_x[int(20012018)] = np.zeros(8640)
taxis_y[int(20012018)] = np.zeros(8640)

x=[]
y=[]

for i in range(ts_i,ts_f,10):
	sql = "select taxi,st_astext(st_pointn(proj_track," + str(i) + "-ts)) from tracks where ts<" + str(i) + " and ts+st_numpoints(proj_track)>" + str(i) +"and taxi='20000333' or taxi='20012018'"
	cursor_psql.execute(sql)
	results2 = cursor_psql.fetchall()   
	for row2 in results2:  
		if row2[1] is None:
			continue
		x,y = row2[1][6:-1].split()   
		x = float(x)
		taxis_x[int(row2[0])][int((i-ts_i)/10)] = x    
		taxis_y[int(row2[0])][int((i-ts_i)/10)] = y


print(taxis_x)
scat = ax.scatter(taxis_x[20000333],taxis_y[20000333],s=10)
scat2 =ax.scatter(taxis_x[20012018],taxis_y[20012018],s=10)
anim = FuncAnimation(
fig, animate, interval=1, frames=len(taxis_y)-1)
plt.draw()
plt.show()
conn.close()