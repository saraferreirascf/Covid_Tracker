import random
import sys

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

#####################
# GENERAL FUNCTIONS #
#####################

def get_infected(conn, s):
    cursor_psql = conn.cursor()
    cursor_psql.execute("select distinct taxi from tracks, cont_aad_caop2018 where concelho='"+str(s)+"' LIMIT 10")
    taxis = cursor_psql.fetchall()
    p = []
    for row in taxis:
        points = row[0].split(',')
        p.append(points)
    first_point = random.choice(p)
    return first_point

def linestring_to_points(line_string):
    xs, ys = [],[]
    points = line_string[11:-1].split(',')
    for point in points:
        (x,y) = point.split()
        xs.append(float(x))
        ys.append(float(y))
    return xs,ys


def get_taxis(conn):
    cursor_psql = conn.cursor()
    cursor_psql.execute("select taxi from tracks, cont_aad_caop2018 where concelho='PORTO'")
    taxis = cursor_psql.fetchall()
    return taxis

def get_tracks(conn, taxi):
    cursor_psql = conn.cursor()
    cursor_psql.execute("select proj_track from tracks where taxi='"+str(taxi)+"';")
    track = cursor_psql.fetchall()
    return track

def infected_area(taxi, coord_x, coord_y,conn):
    cursor_psql = conn.cursor()
    cursor_psql.execute("select taxi from tracks where \
        st_point_inside_circle('"+str(taxi)+"', \
        st_x('"+str(coord_x)+"'), st_y('"+str(coord_y)+"'), 50)")
    area = cursor_psql.fetchall()
    return area