import os
import json
import time
import uuid
import random
from datetime import datetime, timedelta
from confluent_kafka import SerializingProducer

# ✅ Detect if running inside Docker
if os.getenv("DOCKER_ENV"):
    KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"  # Docker uses 'kafka'
else:
    KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"  # PyCharm uses 'localhost'

VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vehicle_data')
GPS_TOPIC = os.getenv('GPS_TOPIC', 'gps_data')
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC', 'traffic_data')
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC', 'weather_data')
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC', 'emergency_data')

# Initializing Global Variables
LONDON_COORDINATES = {'latitude': 51.5074, 'longitude': -0.1278}
BIRMINGHAM_COORDINATES = {'latitude': 52.4862, 'longitude': -1.8904}
LATITUDE_INCREMENT = (BIRMINGHAM_COORDINATES['latitude'] - LONDON_COORDINATES['latitude']) / 100
LONGITUDE_INCREMENT = (BIRMINGHAM_COORDINATES['longitude'] - LONDON_COORDINATES['longitude']) / 100
start_time = datetime.now()
start_location = LONDON_COORDINATES.copy()

# Kafka Producer Configuration
producer_config = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'security.protocol': 'PLAINTEXT',
    'error_cb': lambda err: print(f'Kafka error: {err}')
}
producer = SerializingProducer(producer_config)

def get_next_time():
    global start_time
    start_time += timedelta(seconds=random.randint(30, 60))
    return start_time

def simulate_vehicle_movement():
    global start_location
    start_location['latitude'] += LATITUDE_INCREMENT
    start_location['longitude'] += LONGITUDE_INCREMENT
    start_location['latitude'] += random.uniform(-0.0005, 0.0005)
    start_location['longitude'] += random.uniform(-0.0005, 0.0005)
    return start_location

def generate_vehicle_data(device_id):
    location = simulate_vehicle_movement()
    return {
        'id': str(uuid.uuid4()),
        'deviceId': device_id,
        'timestamp': get_next_time().isoformat(),
        'location': location,
        'speed': random.uniform(0, 40),
        'direction': 'North-East',
        'vehicleType': 'private'
    }

def generate_traffic_camera_data(device_id, camera_id):
    return {
        'id': str(uuid.uuid4()),
        'deviceId': device_id,
        'cameraId': camera_id,
        'timestamp': get_next_time().isoformat(),
        'snapshot': 'Base64EncodedString'
    }

def generate_weather_data(device_id):
    return {
        'id': str(uuid.uuid4()),
        'deviceId': device_id,
        'location': start_location,
        'timestamp': get_next_time().isoformat(),
        'temperature': random.uniform(-5, 26),
        'weatherCondition': random.choice(['Sunny', 'Cloudy', 'Rain', 'Snow']),
        'precipitation': random.uniform(0, 25),
        'windSpeed': random.uniform(0, 100),
        'humidity': random.randint(0, 100),
        'airQualityIndex': random.uniform(0, 500)
    }

def generate_emergency_incident_data(device_id):
    return {
        'id': str(uuid.uuid4()),
        'deviceId': device_id,
        'incidentId': str(uuid.uuid4()),
        'type': random.choice(['Accident', 'Fire', 'Medical', 'Police', 'None']),
        'timestamp': get_next_time().isoformat(),
        'location': start_location,
        'status': random.choice(['Active', 'Resolved'])
    }

# ✅ Improved error handling (Retries if Kafka is unavailable)
def produce_data_to_kafka(topic, data):
    for attempt in range(5):  # Retry up to 5 times
        try:
            producer.produce(topic, key=data['id'], value=json.dumps(data))
            producer.flush()
            print(f"✅ Sent to {topic}: {data}")
            break  # Exit loop if successful
        except Exception as e:
            print(f"❌ Kafka Error: {e} (Attempt {attempt + 1}/5)")
            time.sleep(2)  # Wait before retrying

if __name__ == "__main__":
    device_id = str(uuid.uuid4())
    while True:
        vehicle_data = generate_vehicle_data(device_id)
        gps_data = generate_vehicle_data(device_id)
        traffic_camera_data = generate_traffic_camera_data(device_id, 'CAM-001')
        weather_data = generate_weather_data(device_id)
        emergency_incident_data = generate_emergency_incident_data(device_id)

        produce_data_to_kafka(VEHICLE_TOPIC, vehicle_data)
        produce_data_to_kafka(GPS_TOPIC, gps_data)
        produce_data_to_kafka(TRAFFIC_TOPIC, traffic_camera_data)
        produce_data_to_kafka(WEATHER_TOPIC, weather_data)
        produce_data_to_kafka(EMERGENCY_TOPIC, emergency_incident_data)

        print(f"Produced: {vehicle_data}")
        time.sleep(5)
