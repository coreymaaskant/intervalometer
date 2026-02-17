import datetime
import time
import serial

# configure the serial connection
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)
time.sleep(1)

print("start time:")
start = input()

print("end time:")
end = input()

print("timer 00-99:")
timer = input()

print("alarm enable? (1 = ON, 0 = OFF):")
alarm = input()
if alarm not in ("0", "1"):
    print("Invalid alarm value. Use 1 for ON or 0 for OFF.")
    ser.close()
    exit()

print("Trigger shutter? (1 = Yes, 0 = No):")
trigger = input()
if trigger not in ("0", "1"):
    print("Invalid trigger value. Use 1 for ON or 0 for OFF.")
    ser.close()
    exit()

print("would you like to half press the shutter? (1 = Yes, 0 = No):")
half_press = input()
if half_press not in ("0", "1"):
    print("Invalid half press value. Use 1 for Yes or 0 for No.")
    ser.close()
    exit()

# get temperature setpoint (°C), max 30
while True:
    print("temperature setpoint (°C, max 30):")
    try:
        temp_c = float(input())
    except ValueError:
        print("Invalid temperature input.")
        continue

    if temp_c > 30:
        print("Temperature cannot exceed 30°C.")
        continue

    break

# round to nearest whole degree
temp_c_rounded = round(temp_c)

# pad to 3 digits
temp_str = str(temp_c_rounded).zfill(2)

x = datetime.datetime.now()

dateSt = (
    x.strftime('%y') +
    x.strftime('%m') +
    x.strftime('%d') +
    x.strftime('%u') +
    x.strftime('%H') +
    x.strftime('%M') +
    x.strftime('%S') +
    timer +
    start +
    end +
    alarm +
    trigger +
    temp_str +
    half_press +
    'x'
)

ser.write(dateSt.encode())

print(x)
print(dateSt)
print(temp_str)
ser.close()
