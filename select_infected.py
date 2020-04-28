def get_infected(conn):
    cursor_psql = conn.cursor()
    cursor_psql.execute("select distinct taxi from tracks, cont_aad_caop2018 where concelho='PORTO' LIMIT 10")
    taxis = cursor_psql.fetchall()
    p = []
    for row in taxis:
        points = row[0].split(',')
        p.append(points)
    first_point = random.choice(p)
    return first_point