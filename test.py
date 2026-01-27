import json
import random
from paho.mqtt import client as mqtt_client



broker = "2strader.duckdns.org"       # Change to your broker's address if needed
port = 80
topic = "/camera/sensor"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
client.connect(broker, port)
result = client.publish(topic, "Test1")
client.disconnect()

