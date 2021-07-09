import time
import serial
import gpiozero as gpio
from pyzbar.pyzbar import decode
import gzip

ser = serial.Serial("/dev/ttyS0", 115200, timeout=0.5)
scanner = gpio.OutputDevice(14)
if ser != None:
    print('serial connected')
    
else:
    print('failed')

x = b''
while x == b'':
    x = ser.readline()
    print(x)
    time.sleep(3)
    
txt = open('barcode.txt','a')
# txt.write(decode(x))