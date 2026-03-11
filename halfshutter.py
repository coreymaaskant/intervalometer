
import datetime
import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
time.sleep(1)
start = "1200"
end = "1300"
timer = "00"
shutter = "0"
temp = "20"
halfshutter = "1"
dateSt=""
x = datetime.datetime.now()
dateSt = x.strftime('%y') + x.strftime('%m') + x.strftime('%d')+ x.strftime('%u') + x.strftime('%H') + x.strftime('%M') + x.strftime('%S') + timer + start + end + shutter + temp + halfshutter + 'x'
ser.write(dateSt.encode())
print(x)
print(dateSt)

ser.close()
