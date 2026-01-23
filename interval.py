from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import threading
import time
import serial
latest_data = {}
import json
import paho.mqtt.client as mqtt

MQTT_BROKER = "192.168.0.35"
MQTT_PORT = 1883
MQTT_TOPIC = "intervalometer/sensors"

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()  # background network thread


app = Flask(__name__)
ser = serial.Serial("/dev/ttyUSB0", 57600, timeout=1)
serial_lock = threading.Lock()
latest_data = {}

intervalometer_running = False

def intervalometer(start, end, interval):
    global intervalometer_running
    intervalometer_running = True

    while intervalometer_running:
        #print("Shutter triggered")
        # trigger_camera()
        time.sleep(interval)

def read_serial():
    global latest_data

    while True:
        try:
            with serial_lock:
                line = ser.readline().decode(errors="ignore").strip()

            if not line:
                continue

            # Example: "Temp:18.65 Humidity:27.68 Pressure:99493.50"
            parts = line.split()
            data_dict = {}

            for part in parts:
                if ":" in part:
                    key, value = part.split(":", 1)
                    data_dict[key] = value

            if data_dict:
                latest_data = data_dict

                payload = json.dumps({
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": data_dict
                })

                mqtt_client.publish(MQTT_TOPIC, payload)

        except Exception as e:
            print("Serial/MQTT error:", e)
            time.sleep(1)

threading.Thread(target=read_serial, daemon=True).start()

def send_serial(cmd):
    print("Sending:", cmd)
    ser.write(cmd.encode())

def build_serial_string(
    shutter_interval=0,
    start_time=None,
    end_time=None,
    alarm_enable=0,
    manual_shutter=0,
    temp_setpoint=0
):
    now = datetime.now()

    # Date / time
    YY = f"{now.year % 100:02d}"
    MM = f"{now.month:02d}"
    DD = f"{now.day:02d}"
    w  = f"{now.isoweekday()}"  # 1–7
    HH = f"{now.hour:02d}"
    MN = f"{now.minute:02d}"
    SS = f"{now.second:02d}"

    # Shutter interval
    SH = f"{shutter_interval:02d}"

    # Start / End times
    if start_time and end_time:
        sh, sm = start_time.split(":")
        eh, em = end_time.split(":")
    else:
        sh = sm = eh = em = "00"

    A1H = f"{int(sh):02d}"
    A1M = f"{int(sm):02d}"
    A2H = f"{int(eh):02d}"
    A2M = f"{int(em):02d}"

    A  = str(alarm_enable)
    T  = str(manual_shutter)
    Te = f"{int(temp_setpoint):02d}"

    command = (
        YY + MM + DD + w +
        HH + MN + SS +
        SH +
        A1H + A1M +
        A2H + A2M +
        A + T +
        Te +
        "x"
    )

    return command



@app.route("/", methods=["GET", "POST"])
def index():
    global intervalometer_running

    if request.method == "POST":
        if "set" in request.form:
            start = request.form["start"]
            end = request.form["end"]
            interval = int(request.form["interval"])
            print("start:", start)
            print("end:", end)
            print("interval:", interval)
            cmd = build_serial_string(
                shutter_interval=interval,
                start_time=start,
                end_time=end,
                alarm_enable=1,
                manual_shutter=0,
                temp_setpoint=20  # or from another form field
            )
            send_serial(cmd)

            threading.Thread(
                target=intervalometer,
                args=(start, end, interval),
                daemon=True
            ).start()

        elif "shutter" in request.form:
            print("Manual shutter pressed")
            # trigger_camera()
            
            cmd = (
                "00" "00" "00" "0"
                "00" "00" "00"
                "00"
                "00" "00"
                "00" "00"
                "0" "1"
                "00"
                "x"
            )

            cmd = cmd.replace(" ", "")
            send_serial(cmd)

    return render_template("index.html", data=latest_data)
@app.route("/stop")
def stop():
    global intervalometer_running
    intervalometer_running = False
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
