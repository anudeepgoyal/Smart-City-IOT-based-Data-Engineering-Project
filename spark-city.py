import os
import threading
import json
from confluent_kafka import Consumer

# ✅ Detect if running inside Docker
if os.getenv("DOCKER_ENV"):
    KAFKA_BROKER = "kafka:9092"  # Docker uses 'kafka'
else:
    KAFKA_BROKER = "localhost:9092"  # PyCharm uses 'localhost'

# Define Topics and Consumer Groups
TOPIC_CONFIGS = {
    "vehicle_data": "vehicle-group",
    "gps_data": "gps-group",
    "traffic_data": "traffic-group",
    "weather_data": "weather-group",
    "emergency_data": "emergency-group"
}

def consume_kafka(topic, group_id):
    """Consumes messages from a specific Kafka topic and processes the data."""
    consumer_config = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_config)
    consumer.subscribe([topic])

    print(f"✅ Listening to Kafka topic: {topic} at {KAFKA_BROKER}...")

    while True:
        msg = consumer.poll(1.0)  # Wait for a message
        if msg is None:
            continue
        if msg.error():
            print(f"❌ Consumer error in {topic}: {msg.error()}")
            continue

        try:
            data = json.loads(msg.value().decode('utf-8'))
            print(f"🔹 Received from {topic}: {data}")
        except json.JSONDecodeError:
            print(f"❌ Failed to decode message from {topic}: {msg.value()}")

# ✅ Create and start a separate thread for each Kafka topic
threads = []
for topic, group_id in TOPIC_CONFIGS.items():
    thread = threading.Thread(target=consume_kafka, args=(topic, group_id))
    thread.daemon = True  # Allows process to exit if main thread exits
    thread.start()
    threads.append(thread)

# ✅ Keep all threads running
for thread in threads:
    thread.join()
