import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

# Delay Spark startup to allow Kafka topics to be created by the producer
print("Waiting for Kafka topics to be created by the producer...")
time.sleep(30)  # Wait 30 seconds (adjust as necessary)

# Use the correct Kafka broker based on environment
if os.getenv("DOCKER_ENV"):
    KAFKA_BROKER = "kafka:9092"   # Use service name inside Docker
else:
    KAFKA_BROKER = "localhost:9092"  # Outside Docker

# Define Kafka Topics (comma-separated)
KAFKA_TOPICS = "vehicle_data,gps_data,traffic_data,weather_data,emergency_data"

# Create Spark Session
spark = (SparkSession.builder
         .appName("Kafka-Spark-Streaming")
         .master("spark://spark-master:7077")
         .config("spark.sql.streaming.schemaInference", "true")
         .config("spark.ui.port", "4040")
         .config("spark.ui.host", "0.0.0.0")
         .getOrCreate())
spark.sparkContext.setLogLevel("DEBUG")

# ---------------------------
# Define Schemas for each topic
# ---------------------------
vehicle_schema = StructType([
    StructField("id", StringType()),
    StructField("deviceId", StringType()),
    StructField("timestamp", StringType()),
    StructField("location", StructType([
        StructField("latitude", DoubleType()),
        StructField("longitude", DoubleType())
    ])),
    StructField("speed", DoubleType()),
    StructField("direction", StringType()),
    StructField("vehicleType", StringType())
])

traffic_schema = StructType([
    StructField("id", StringType()),
    StructField("deviceId", StringType()),
    StructField("cameraId", StringType()),
    StructField("timestamp", StringType()),
    StructField("snapshot", StringType())
])

weather_schema = StructType([
    StructField("id", StringType()),
    StructField("deviceId", StringType()),
    StructField("location", StructType([
        StructField("latitude", DoubleType()),
        StructField("longitude", DoubleType())
    ])),
    StructField("timestamp", StringType()),
    StructField("temperature", DoubleType()),
    StructField("weatherCondition", StringType()),
    StructField("precipitation", DoubleType()),
    StructField("windSpeed", DoubleType()),
    StructField("humidity", IntegerType()),
    StructField("airQualityIndex", DoubleType())
])

emergency_schema = StructType([
    StructField("id", StringType()),
    StructField("deviceId", StringType()),
    StructField("incidentId", StringType()),
    StructField("type", StringType()),
    StructField("timestamp", StringType()),
    StructField("location", StructType([
        StructField("latitude", DoubleType()),
        StructField("longitude", DoubleType())
    ])),
    StructField("status", StringType())
])

# ---------------------------
# Read raw data from Kafka
# ---------------------------
df_raw = (spark.readStream
          .format("kafka")
          .option("kafka.bootstrap.servers", KAFKA_BROKER)
          .option("subscribe", KAFKA_TOPICS)
          .option("startingOffsets", "latest")
          .option("failOnDataLoss", "false")  # Do not crash if topics are temporarily missing
          .load())

# Convert binary 'value' to string and keep the topic for routing
df_raw = df_raw.selectExpr("topic", "CAST(value AS STRING) as json_str")

# ---------------------------
# Parse each topic's data using its schema
# ---------------------------
vehicle_df = (df_raw.filter(col("topic") == "vehicle_data")
              .select(from_json(col("json_str"), vehicle_schema).alias("data"))
              .select("data.*"))

gps_df = (df_raw.filter(col("topic") == "gps_data")
          .select(from_json(col("json_str"), vehicle_schema).alias("data"))
          .select("data.*"))

traffic_df = (df_raw.filter(col("topic") == "traffic_data")
              .select(from_json(col("json_str"), traffic_schema).alias("data"))
              .select("data.*"))

weather_df = (df_raw.filter(col("topic") == "weather_data")
              .select(from_json(col("json_str"), weather_schema).alias("data"))
              .select("data.*"))

emergency_df = (df_raw.filter(col("topic") == "emergency_data")
                .select(from_json(col("json_str"), emergency_schema).alias("data"))
                .select("data.*"))

# ---------------------------
# Write each stream to the console for testing
# ---------------------------
vehicle_query = (vehicle_df.writeStream
                 .format("console")
                 .outputMode("append")
                 .queryName("vehicle_view")
                 .start())

gps_query = (gps_df.writeStream
             .format("console")
             .outputMode("append")
             .queryName("gps_view")
             .start())

traffic_query = (traffic_df.writeStream
                 .format("console")
                 .outputMode("append")
                 .queryName("traffic_view")
                 .start())

weather_query = (weather_df.writeStream
                 .format("console")
                 .outputMode("append")
                 .queryName("weather_view")
                 .start())

emergency_query = (emergency_df.writeStream
                   .format("console")
                   .outputMode("append")
                   .queryName("emergency_view")
                   .start())

print("✅ Streaming queries started. Waiting for data...")
spark.streams.awaitAnyTermination()
