import time
import serial
import gpiozero as gpio
from pyzbar.pyzbar import decode
import gzip

ser = serial.Serial("/dev/ttyS0", 115200, timeout=0.5)
scanner = gpio.OutputDevice(4)
scanner.on()
if ser != None:
    print('serial connected')
    
else:
    print('failed')

x = b''
while True:
    x = ser.readline()
    print(tuple(list(x)))
    time.sleep(1)
    
wanted_x = [0, 0, 240, 0, 254, 0, 0, 240, 0, 254, 0, 0, 240, 0, 0, 240, 0, 0, 0, 192, 0, 254, 0, 0, 240, 0, 0, 240, 0, 0, 240, 0, 0, 240, 0, 0, 0, 0, 0, 0, 254, 0, 0, 240, 0, 254, 0, 254, 0, 0, 0, 0, 0, 0, 0, 240, 0, 254, 0, 0, 0, 0, 0]

if wanted_x == list(x):
    print('matched')
else:
    print('no match')



