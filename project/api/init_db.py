import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="iot_db",
    user="postgres",
    password="password",  # غيرها إذا عندك باسورد مختلف
    port=5432
)

cur = conn.cursor()

cur.execute("""
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
""")

# USERS
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# DEVICES
cur.execute("""
CREATE TABLE IF NOT EXISTS devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id) ON DELETE CASCADE
);
""")

# TELEMETRY
cur.execute("""
CREATE TABLE IF NOT EXISTS telemetry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id UUID REFERENCES devices(id) ON DELETE CASCADE,
    key VARCHAR(100) NOT NULL,
    value FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
cur.close()
conn.close()

print("Tables created ")