import random
import sys
import numpy as np
import matplotlib.pyplot as plt


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




#FUNCOES QUE NAO ESTAO A SER USADAS |
#                                   V

def get_coords_infect(index, offsets):
    for i in offsets:
        j = 0
        while j < 8640:
            coords.append(offsets[j][index])
            j += 1
    return coords

def get_taxis(conn):
    cursor_psql = conn.cursor()
    cursor_psql.execute("select taxi from tracks, cont_aad_caop2018 where concelho='PORTO'")
    taxis = cursor_psql.fetchall()
    return taxis

def infect_taxis(x,y,conn):
    cursor_psql = conn.cursor()
    cursor_psql.execute("select st_x() from tracks \
        where st_distance(point("+str(x)+","+str(y)+"), proj_location) <= 50") 

def get_infected(conn, s):
    cursor_psql = conn.cursor()
    cursor_psql.execute("select distinct taxi, extract(hour from to_timestamp(ts)) as hora from cont_aad_caop2018, tracks \
        where st_contains(proj_boundary,proj_track) and  concelho='"+str(s)+"' order by hora asc limit 10;")
    taxis = cursor_psql.fetchall()
    p = []
    for row in taxis:
        points = row[0].split(',')
        p.append(points)
    first_point = random.choice(p)
    return first_point

def get_tracks(conn, taxi, ts_i, ts_f):
    taxis_x = {}
    taxis_y = {}
    step = 10
    array_size = int(24*60*60/step)
    
    for row in taxi:
        taxis_x[int(row[0])] = np.zeros(array_size)
        taxis_y[int(row[0])] = np.zeros(array_size)

      
    for i in range(ts_i, ts_f, 10):
        cursor_psql = conn.cursor()
        sql = "select taxi,st_pointn(proj_track," + str(i) + "-ts) \
            from tracks where ts<" + str(i) + " and ts+st_numpoints(proj_track)>" + str(i)
        cursor_psql.execute(sql)
        track = cursor_psql.fetchall()
        for row in track:
            x,y = row[2].coords
            taxis_x[int(row[0])][int((i-ts_i)/10)] = x
            taxis_y[int(row[0])][int((i-ts_i)/10)] = y

    track_offset = []
    for i in range(array_size):
        l = []
        for j in taxis_x:
            l.append([taxis_x[j][i],taxis_y[j][i]])
            track_offset.append(l)
    return track_offset

def infected_area(taxi, coord_x, coord_y,conn):
    cursor_psql = conn.cursor()
    cursor_psql.execute("select taxi from tracks where \
        st_point_inside_circle('"+str(taxi)+"', \
        st_x('"+str(coord_x)+"'), st_y('"+str(coord_y)+"'), 50)")
    area = cursor_psql.fetchall()
    return area


  