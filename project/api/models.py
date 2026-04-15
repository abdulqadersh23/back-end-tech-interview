import psycopg2
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="iot_db",
        user="postgres",
        password="password",  
        port=5432
    )