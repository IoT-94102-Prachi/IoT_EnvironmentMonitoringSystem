import json
import paho.mqtt.client as mqtt
import mysql.connector
import requests

#  for ThingSpeak
THINGSPEAK_API = "L3HNCJGGG0NXYU9K"

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="environment_monitor"
)
cursor = db.cursor()

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())

    temperature = data['temperature']
    humidity = data['humidity']
    gas = data['gas']

    # data inserted into MySQL
    sql = """INSERT INTO parameter
             (temperature, humidity, gas_level)
             VALUES (%s, %s, %s)"""
    cursor.execute(sql, (temperature, humidity, gas))
    db.commit()

    print("Inserted:", temperature, humidity, gas)

    #this Sends data to ThingSpeak
    url = (
        f"https://api.thingspeak.com/update?"
        f"api_key={THINGSPEAK_API}"
        f"&field1={temperature}"
        f"&field2={humidity}"
        f"&field3={gas}"
    )
    requests.get(url)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect("test.mosquitto.org", 1883, 60)
client.subscribe("iot/environment")
client.on_message = on_message

print("Subscriber started...")
client.loop_forever()