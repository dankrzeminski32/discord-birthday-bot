import psycopg2
from psycopg2 import Error
from config import POSTGRES_BIRTHDAYBOT_DBNAME, POSTGRES_USER, POSTGRES_PASS

try:
    # Connect to an existing database
    connection = psycopg2.connect(user=POSTGRES_USER,
                                  password=POSTGRES_PASS,
                                  host="127.0.0.1",
                                  port="5432",
                                  database=POSTGRES_BIRTHDAYBOT_DBNAME)

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")