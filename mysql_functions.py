from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user="root",
        password="root",
    ) as connection:
        print("MYSQL CONNECTED " + str(connection))
except Error as e:
    print(e)
