import json
import psycopg2
import uuid
import paho.mqtt.client as mqtt


# DATABASE CONNECTION
def get_connection():
    return psycopg2.connect(
        host="iot_postgres",
        database="iot_db",
        user="postgres",
        password="password",
        port=5432
    )


# MQTT MESSAGE HANDLER
def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode()

        print(f"Received: {payload} from {topic}")

        # parse JSON safely
        data = json.loads(payload)

        value = data.get("value")
        key = data.get("key")

        # validation
        if value is None or key is None:
            print("Invalid payload, skipping insert")
            return

        # extract device_id from topic
        parts = topic.split("/")

        if len(parts) < 3:
            print("Invalid topic format")
            return

        device_id = parts[-1]

        # DB insert
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO telemetry (id, device_id, key, value)
            VALUES (%s, %s, %s, %s);
        """, (str(uuid.uuid4()), device_id, key, value))

        conn.commit()
        cur.close()
        conn.close()

        print("Saved to DB")

    except json.JSONDecodeError:
        print("Invalid JSON received")

    except Exception as e:
        print("Error:", str(e))


# MQTT SETUP
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe("v1/data/#")


client.on_connect = on_connect
client.on_message = on_message

print("MQTT Service Running...")

client.connect("mqtt", 1883, 60)

client.loop_forever()