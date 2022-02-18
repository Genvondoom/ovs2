import mysql.connector
from mysql.connector import Error


def insertUsers(cursor, connection, values):
    try:
        query = """INSERT INTO users (matricno, email, password)VALUES (%s, %s, %s)"""

        cursor.execute(query, values)
        connection.commit()
        return "done"
    except mysql.connector.errors.IntegrityError:
        return "duplicate"


def insertElection(cursor, connection, values):
    try:
        query = """INSERT INTO elections (electionid, name, sch, date, startTime, duration, stopTime, status)VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        cursor.execute(query, values)
        connection.commit()
        return "done"
    except mysql.connector.errors.IntegrityError:
        return "duplicate"
    except mysql.connector.errors.ProgrammingError:
        return "duplicate"


def checkLogin(cursor, matric, password):
    cursor.execute(f"select matricno,password from users where matricno = '{matric}'")

    result = cursor.fetchone()

    if result is not None:
        if result[1] == password:

            return True
        else:
            return False
    else:
        return False


def selectElection(cursor, electionid):
    cursor.execute(f"select * from elections where electionid = '{electionid}'")

    result = cursor.fetchall()

    if result:
        return result
    else:
        return False


def getElections(cursor):
    cursor.execute("select electionid, name from elections")
    return cursor.fetchall()


def joinElection(cursor, connection, values):
    try:
        query = """INSERT INTO electionUsers (electionToken,userId,electionid,role,status)VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, values)
        connection.commit()
        return "done"
    except mysql.connector.errors.IntegrityError:
        return "duplicate"



try:
    connection = mysql.connector.connect(host='localhost',
                                         database='ovs',
                                         user='ovs',
                                         password='Vondoom1&2')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)


except Error as e:
    print("Error while connecting to MySQL", e)
except mysql.connector.errors.IntegrityError as e:
    print(e)
