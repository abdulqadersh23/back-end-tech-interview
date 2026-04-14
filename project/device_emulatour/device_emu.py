import asyncio
import json
import random
import signal
import aiomqtt
from os import environ

devices_ids = environ.get('DEVICES_IDS_LIST').split(',')

async def publish_random_data():
    """Continuously publish random data every 10 seconds."""
    while True: 
        try:
            async with aiomqtt.Client(hostname="mqtt", port=1883) as client:
                print("✅ Connected to MQTT broker")

                while True:
                    payload = {
                        "value": random.randint(0, 100),
                        "key": random.choice(['Temperature','Humidity','Lux'])
                    }
                    message = json.dumps(payload)
                    
                    TOPIC = f"v1/data/{random.choice(devices_ids)}"
                    
                    await client.publish(TOPIC, message)
                    print(f"📤 Sent: {message} → {TOPIC}")

                    await asyncio.sleep(10)

        except aiomqtt.MqttError as e:
            print(f"⚠️ MQTT error: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)


async def main():
    stop_event = asyncio.Event()

    # Graceful shutdown on Ctrl+C or SIGTERM
    for sig in (signal.SIGINT, signal.SIGTERM):
        asyncio.get_event_loop().add_signal_handler(
            sig, stop_event.set
        )

    publisher_task = asyncio.create_task(publish_random_data())

    await stop_event.wait()
    print("\n🛑 Stopping publisher...")
    publisher_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
