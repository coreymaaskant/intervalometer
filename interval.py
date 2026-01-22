from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import threading
import time
import serial
latest_data = {}

app = Flask(__name__)

intervalometer_running = False

def intervalometer(start, end, interval):
    global intervalometer_running
    intervalometer_running = True

    while intervalometer_running:
        #print("Shutter triggered")
        # trigger_camera()
        time.sleep(interval)

def read_serial(port="/dev/ttyUSB0", baud=57600):
    global latest_data
    ser = serial.Serial(port, baud, timeout=1)
    while True:
        line = ser.readline().decode().strip()
        if line:
            # Example line: "Temp:18.65 Humidity:27.68 Pressure:99493.50 TargetTemp:23°C ..."
            parts = line.split()
            data_dict = {}
            for part in parts:
                if ":" in part:
                    key, value = part.split(":", 1)
                    data_dict[key] = value
            latest_data = data_dict

threading.Thread(target=read_serial, daemon=True).start()

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

            threading.Thread(
                target=intervalometer,
                args=(start, end, interval),
                daemon=True
            ).start()

        elif "shutter" in request.form:
            print("Manual shutter pressed")
            # trigger_camera()

    return render_template("index.html", data=latest_data)
@app.route("/stop")
def stop():
    global intervalometer_running
    intervalometer_running = False
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
