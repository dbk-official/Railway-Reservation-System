
import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password_here", 
            database="railway_db"
        )
        return connection

    except Error as error:
        print("Database connection failed:", error)
        return None


if __name__ == "__main__":
    connection = get_connection()

    if connection is not None and connection.is_connected():
        print("Railway database connected successfully!")
        connection.close()
