import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="iot_db",
        user="postgres",
        password="password",
        port=5432
    )
    print("DB Connected Successfully!")
except Exception as e:
    print("Error:", e)