import sqlite3


#(1, 'DWC', 132235728582213632, 5)

def fetchPointList():

    con = sqlite3.connect("pseapoints.db")
    cursor = con.cursor()

    points = cursor.execute("""
    SELECT * FROM points ORDER BY name;
    """)

    nomes = []
    pontos = []
    total = 0

    # get points from cursor
    for i in cursor.fetchall():
        nomes.append(i[1])
        pontos.append(i[3])

    # format text
    op = "[PSEAPOINTS]:\n"
    for i in range(len(nomes)):
        op = op + "[{0}: {1}] ".format(nomes[i], pontos[i])
        total = total + pontos[i]


    op = op + "[TOTAL: {0}]".format(total)
    con.close()

    return op

def checkID(id):

    idv = False

    con = sqlite3.connect("pseapoints.db")
    cursor = con.cursor()

    user = cursor.execute("""
    SELECT user_id FROM points;
    """)

    return id in cursor.fetchall()

    con.close()

def addUser(id, name, points):
    con = sqlite3.connect("pseapoints.db")
    cursor = con.cursor()

    if checkID(id):
        print("Usuario ja existe, seu bobao.")
    else:
        new_user = cursor.execute("""
        INSERT INTO points (name, user_id, ppoints) VALUES (?, ?, ?)
        """, (name, id, points))


    con.commit()
    con.close()
    return True

def getUserPoints(id):
    con = sqlite3.connect("pseapoints.db")
    cursor = con.cursor()

    points = cursor.execute("""
    SELECT * FROM points
""")

    op = 0

    if checkID(id):
        for i in cursor.fetchall():
            if i[2] == id:
                op = i[3]
                break

    con.close()
    return op

def addPoints(id, name, points, minus):
    con = sqlite3.connect("pseapoints.db")
    cursor = con.cursor()
    ppoints = getUserPoints(id)
    queryv = ppoints

    if checkID(id):
        if minus:
            if type(int(points[1:])) is int:
                queryv = ppoints - int(points[1:])

        else:
                queryv = ppoints + points

        pontos = cursor.execute("""
        UPDATE points
        SET ppoints = ?
        WHERE user_id = ?
        """, (queryv, id))

        con.commit()
        con.close()

    else:
        addUser(id, name ,points)
        print("{0} ainda nao faz parte do pseaclube, adicionando usuario...".format(name))





