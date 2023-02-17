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
        cursor = connection.cursor()
    except Error as e:
        print(e)


def exec_query(query_string, commit=False):
    try:
        res = cursor.execute(query_string)
        if commit:
            connection.commit()
        print(res)
    except Error as e:
        print(e)


def close_connection():
    connection.close()

