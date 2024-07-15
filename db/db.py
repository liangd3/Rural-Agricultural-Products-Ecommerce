import mysql.connector
import connect as connect


def get_connection():
    return mysql.connector.connect(user=connect.dbuser, \
            password=connect.dbpass, host=connect.dbhost, \
            database=connect.dbname, autocommit=True)

def query(queryString):
    connection = get_connection()
    with connection as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(queryString)
            result = cursor.fetchall()
    return result

def queryOneResult(queryString):
    connection = get_connection()
    with connection as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(queryString)
            result = cursor.fetchone()
    return result


def querywithLastID(queryString):
    connection = get_connection()
    with connection as connection:
        with connection.cursor() as cursor:
            cursor.execute(queryString)
            connection.commit()
            id = cursor.lastrowid
    return id