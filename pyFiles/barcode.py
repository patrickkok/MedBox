import time
import serial
import gpiozero as gpio

ser = serial.Serial("/dev/ttyS0", 115200, timeout=0.5)
scanner = gpio.OutputDevice(14)
if ser != None:
    print('serial connected')
    
else:
    print('failed')
    
while 1:
    ser.write("Say something:\n")
    x = ser.readline()
    print(x)
    time.sleep(3)