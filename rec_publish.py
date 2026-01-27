import serial
import json
import re
import time
import paho.mqtt.client as mqtt

# ==========================
# SERIAL CONFIGURATION
# ==========================
SERIAL_PORT = "/dev/ttyUSB0"   # Windows example: "COM3"
BAUD_RATE = 57600
SERIAL_TIMEOUT = 1

# ==========================
# MQTT CONFIGURATION
# ==========================
MQTT_BROKER = "192.168.0.35"      # e.g. "192.168.1.10"
MQTT_PORT = 1883
MQTT_TOPIC = "intervalometer/sensors"
MQTT_CLIENT_ID = "serial_to_mqtt"

# ==========================
# REGEX PARSER
# ==========================
FIELD_REGEX = re.compile(
    r'(\w+):([+-]?\d+(?:\.\d+)?)'
)

def parse_telemetry(line: str) -> dict:
    """
    Parse telemetry string into a dictionary
    """
    data = {}
    matches = FIELD_REGEX.findall(line)

    for key, value in matches:
        # Try numeric conversion
        try:
            if ":" in value:
                data[key] = value  # time fields
            elif "." in value:
                data[key] = float(value)
            else:
                data[key] = int(value)
        except ValueError:
            data[key] = value

    # Add timestamp
    data["timestamp"] = time.time()

    return data


def main():
    # --------------------------
    # Setup Serial
    # --------------------------
    ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        timeout=SERIAL_TIMEOUT
    )

    print(f"Connected to serial port {SERIAL_PORT}")

    # --------------------------
    # Setup MQTT
    # --------------------------
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_start()

    print(f"Connected to MQTT broker {MQTT_BROKER}")

    # --------------------------
    # Main Loop
    # --------------------------
    try:
        while True:
            line = ser.readline().decode("utf-8", errors="ignore").strip()

            if not line:
                continue

            print("RAW:", line)

            telemetry = parse_telemetry(line)
            payload = json.dumps(telemetry)

            client.publish(MQTT_TOPIC, payload)

            print("JSON:", payload)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        ser.close()
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
