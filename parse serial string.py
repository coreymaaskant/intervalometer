import re
mystring = "25-6-11 9:50:44 Temp:22.90 Humidity:43.23 Pressure:100591.94"
parts = mystring.split()
print(parts)

date= parts[0].split('-')
year = int(date[0])
month = int(date[1])
day = int(date[2])

time= parts[1].split(':')
hour = int(time[0])
minute = int(time[1])
second = int(time[2])

print(year)
print(month)
print(day)

print(hour)
print(minute)
print(second)

temp = parts[2].split(':')
temp = float(temp[1])
print(temp)

hum = parts[3].split(':')
hum = float(hum[1])
print(hum)

pressure = parts[4].split(':')
pressure = float(pressure[1])
print(pressure)
