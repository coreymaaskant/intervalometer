import datetime
import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial('COM7', 57600, timeout=1)
time.sleep(3)
while 1:
        try:
            msg = ser.readline()
            msg=msg.decode('utf-8')
            print(msg)
        except ser.SerialTimeoutException:
            print("Data could not be read")
ser.close()
