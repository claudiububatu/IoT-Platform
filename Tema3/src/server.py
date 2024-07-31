from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import paho.mqtt.client as mqtt
import subprocess
from datetime import datetime
import traceback

# Install influxdb package
subprocess.run(['python3', '-m', 'pip', 'install', 'influxdb-client'])

# MQTT Configuration
mqtt_broker_host = "172.28.42.208"  # Replace with the actual hostname
mqtt_broker_port = 1883
mqtt_topic = "#"

def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    
    try:
        data = json.loads(payload)
        
        # Perform data validation and processing
        if not isinstance(data, dict):
            print(f"Invalid data format for topic: {message.topic}")
            return

        # Create InfluxDB data point
        my_time = datetime.utcnow().isoformat() if "timestamp" not in data else data.get("timestamp")
        influx_data = [
            {
                "measurement": message.topic.replace("/", "_"),
                "time": my_time,
                "fields": {key: value for key, value in data.items() if isinstance(value, (int, float))}
            }
        ]
        
        print(influx_data)
        influx_client.write_api(write_options=SYNCHRONOUS).write("my_bucket", "SPRC", influx_data)
        
        # Log the successful processing
        print(f"Data processed and stored for topic: {message.topic}")
    except json.JSONDecodeError:
        # Log error for invalid JSON format
        print(f"Error decoding JSON for topic: {message.topic}")
    except Exception as e:
        # Log other exceptions
        print(f"Error processing message for topic {message.topic}: {str(e)}")
        traceback.print_exc()

def main():
    try:
        # Set up MQTT client
        print("Connecting to MQTT broker...")
        mqtt_client = mqtt.Client()
        mqtt_client.on_message = on_message
        mqtt_client.connect(mqtt_broker_host, mqtt_broker_port, 60)
        print("Subscribing to MQTT topic...")
        mqtt_client.subscribe(mqtt_topic)

        # Set up InfluxDB client
        print("Connecting to InfluxDB...")
        global influx_client
        influx_client = InfluxDBClient(
            url="http://172.28.42.208:8086", org="SPRC", token="DSLBVofZtyjjtuoRrN1-Vme_sA0ondSg0GNMkJqpGrNyvEJtAPk-MqYtgSBHpLZKxMvtbpL7RnjYXHu7j2Anww==")

        # Main loop to continuously listen for MQTT messages
        print("Entering main loop...")
        mqtt_client.loop_forever()
    except Exception as e:
        # Log other exceptions during setup
        print(f"Error during setup: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
