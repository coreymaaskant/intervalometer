import datetime
import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)
time.sleep(1)
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

ser.close()

