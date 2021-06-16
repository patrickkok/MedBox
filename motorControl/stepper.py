from time import sleep
import RPi.GPIO as GPIO

DIR = 20
STEP = 26
CW = 1
CCW = 0
SPR = 200

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

MODE = (14, 15, 18)
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full' : (0, 0, 0),
              'Half' : (1, 0, 0),
              '1/4' : (0, 1, 0),
              '1/8' : (1, 1, 0),
              '1/16' : (0, 0, 1),
              '1/32' : (1, 0, 1)}

GPIO.output(MODE, RESOLUTION['Half'])

step_count = SPR
delay = 0.0208

print('check')

for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)
    print(x)
    

