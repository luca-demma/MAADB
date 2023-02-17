from mysql.connector import connect, Error

connection = ""
cursor = ""


def mysql_connect():
    try:
        global connection, cursor
        connection = connect(
            host="localhost",
            user="root",
            password="root",
            database="progetto",
        )
        cursor = connection.cursor(buffered=True)
    except Error as e:
        print(e)


def exec_query(query_string, commit=False, fetchOne=False):
    try:
        res = cursor.execute(query_string)
        if commit:
            connection.commit()
        if fetchOne:
            res = cursor.fetchone()
        # print(res)
        return res
    except Error as e:
        print(e)


def insert_many(query_string, records):
    try:
        cursor.executemany(query_string, records)
        connection.commit()
    except Error as e:
        print(e)


def close_connection():
    connection.close()

