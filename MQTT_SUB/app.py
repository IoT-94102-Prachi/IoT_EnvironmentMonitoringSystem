from flask import Flask, render_template
import paho.mqtt.client as mqtt
import threading

app = Flask(__name__)

# Global variable to store the latest MQTT message
latest_message = "No data yet"

# MQTT configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/environment"  # Updated topic

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global latest_message
    latest_message = msg.payload.decode()
    print(f"Received '{latest_message}' on topic '{msg.topic}'")

# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start MQTT client in a separate thread
def start_mqtt():
    mqtt_client.loop_forever()

threading.Thread(target=start_mqtt, daemon=True).start()

# Flask route
@app.route("/")
def dashboard():
    return render_template("dashboard.html", message=latest_message)

if __name__ == "__main__":
    app.run(debug=True)
