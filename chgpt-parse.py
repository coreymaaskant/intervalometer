import serial
import json
import random
from paho.mqtt import client as mqtt_client
import datetime
import time


# MQTT Broker settings
broker = "2strader.duckdns.org"       # Change to your broker's address if needed
port = 80
topic = "/camera/sensor"
client_id = f'python-mqtt-{random.randint(0, 1000)}'


# Configure the serial port
comport = 'COM7'
baud_rate = 57600


try:
    # Open serial connection
    ser = serial.Serial(comport, baud_rate, timeout=None)
    print(f"Opened serial port {port} at {baud_rate} baud.")
    client = mqtt_client.client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.connect(broker, port)
    print("start time:")
    start = input()
    print("end time:")
    end = input()
    print("timer 00-99:")
    timer = input()
    dateSt=""
    x = datetime.datetime.now()
    dateSt = x.strftime('%y') + x.strftime('%m') + x.strftime('%d')+ x.strftime('%u') + x.strftime('%H') + x.strftime('%M') + x.strftime('%S') + timer + start + end + 'x'
    ser.write(dateSt.encode())
    print(x)
    print(dateSt)
    time.sleep(5)
    read = ser.readline()
    print(read)
    
    while True:
        print("Waiting for ASCII string of numbers...")
        data_bytes = ser.readline()  # Waits for a line ending in '\n'
        data_str = data_bytes.decode('ascii', errors='ignore').strip()
        
        print(f"Received: {data_str}")
        # Split the string into parts
        date_part, time_part, temp_part, humidity_part, pressure_part = data_str.split()

        # Parse date
        year, month, day = map(int, date_part.split('-'))
        year += 2000  # Adjust year if needed (assuming '25' means 2025)

        # Parse time
        hour, minute, second = map(int, time_part.split(':'))

        # Parse sensor data
        temp = float(temp_part.split(':')[1])
        humidity = float(humidity_part.split(':')[1])
        pressure = float(pressure_part.split(':')[1])

        # Print the parsed variables
        print(f"Year: {year}, Month: {month}, Day: {day}")
        print(f"Hour: {hour}, Minute: {minute}, Second: {second}")
        print(f"Temp: {temp}, Humidity: {humidity}, Pressure: {pressure}")



        data = {
            "day": day,
            "month": month,
            "year": year,
            "hour": hour,
            "minute": minute,
            "second": second,
            "temp": temp,
            "humidity": humidity,
            "pressure": pressure
        } 
        json_payload = json.dumps(data)
        result = client.publish(topic, json_payload)


except KeyboardInterrupt:
    print("\nProgram stopped by user.")

except serial.SerialException as e:
    print(f"Serial error: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial connection closed.")
        client.disconnect()
        print("MQTT client disconnected.")
