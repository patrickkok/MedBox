import time
import serial
import gpiozero as gpio
from pyzbar.pyzbar import decode
import gzip
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
ser = serial.Serial("/dev/ttyS0", 115200, timeout=0.5)
scanner = gpio.OutputDevice(4)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)
scanner.on()
if ser != None:
    print('serial connected')
    
else:
    print('failed')

x = b''
time.sleep(2)
print('button pressed')
GPIO.output(27, GPIO.LOW)
while x == b'':
    x = ser.readline()
    print(tuple(list(x)))
    time.sleep(1)




