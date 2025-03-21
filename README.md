# 🚀 Smart City Data Processing Pipeline

## 📌 Project Overview
The **Smart City Data Processing Pipeline** is a real-time data streaming and processing system that simulates and analyzes urban mobility, weather conditions, traffic monitoring, and emergency incidents. It leverages **Apache Kafka**, **Apache Spark Streaming**, and **Docker** to create a scalable and efficient data pipeline.

---

## ⚙️ Tech Stack
- **Apache Kafka** - Real-time event streaming
- **Apache Spark (PySpark)** - Data processing and analytics
- **Docker & Docker-Compose** - Containerized environment
- **Python** - Data simulation and processing
- **Bitnami Spark & Confluent Kafka Images**

---

## 📁 Project Structure

```
📂 Smart-City-Data-Pipeline
│── docker-compose.yml     # Defines Kafka, Zookeeper, Spark services
│── main.py                # Kafka producer to simulate city data
│── spark_streaming.py      # Spark streaming job to process Kafka data
│── spark-city.py          # Kafka consumer for real-time monitoring
└── README.md              # Project documentation
```

---

## 🔄 System Workflow
1. **Data Simulation (`main.py`)**
   - Simulates vehicle movement, traffic camera data, weather conditions, and emergency incidents.
   - Publishes data to Kafka topics.

2. **Real-time Streaming (`spark_streaming.py`)**
   - Reads data streams from Kafka.
   - Uses Spark Streaming to process and transform data.
   - Outputs results to the console for testing.

3. **Kafka Consumer (`spark-city.py`)**
   - Consumes processed Kafka topics for visualization or external system integration.
   - Prints incoming messages for validation.

4. **Dockerized Deployment (`docker-compose.yml`)**
   - Sets up **Kafka**, **Spark Master/Workers**, and **Zookeeper** for distributed computing.
   - Runs the Spark application automatically.

---

## 🛠️ Setup & Installation
### **1️⃣ Prerequisites**
Ensure you have installed:
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- Python 3.7+

### **2️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/Smart-City-Data-Pipeline.git
cd Smart-City-Data-Pipeline
```

### **3️⃣ Build and Start Services**
```sh
docker-compose up -d --build
```

### **4️⃣ Verify Running Containers**
```sh
docker ps
```
Expected output:
```
CONTAINER ID   IMAGE                   PORTS                  STATUS
123abc456def   bitnami/spark:3.4.1      7077/tcp, 8080/tcp     Up
789xyz012ghi   confluentinc/cp-kafka   9092/tcp               Up
```

### **5️⃣ View Real-time Kafka Topics**
```sh
docker logs -f spark-app
```

---

## 🚀 Running the Project Manually
If you prefer running scripts without Docker:

### **1️⃣ Start Kafka & Zookeeper**
```sh
docker-compose up -d kafka zookeeper
```

### **2️⃣ Run Data Producer**
```sh
python main.py
```

### **3️⃣ Run Spark Streaming Job**
```sh
python spark_streaming.py
```

### **4️⃣ Start Kafka Consumer**
```sh
python spark-city.py
```

---

## 📊 Example Output
```
✅ Sent to vehicle_data: {'id': 'abc123', 'speed': 45, 'location': {'lat': 51.5, 'lon': -0.1}}
✅ Sent to weather_data: {'temperature': 22.5, 'humidity': 60, 'windSpeed': 5.0}
✅ Spark Streaming Processing vehicle_data...
🔹 Received from weather_data: {'temperature': 22.5, 'humidity': 60}
```

---

## 📌 Future Enhancements
- 🔹 **Integrate Data Storage (HDFS, Delta Lake, or PostgreSQL)**
- 🔹 **Visualize Processed Data with Grafana or Power BI**
- 🔹 **Deploy on Cloud (AWS, Azure, or GCP)**


