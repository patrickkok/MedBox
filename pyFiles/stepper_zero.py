from time import sleep
import gpiozero as gpio
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# setup all pins
#stepper motor
DIR = gpio.OutputDevice(21)
STEP = gpio.OutputDevice(20)
SLEEP = gpio.OutputDevice(26)
CW = 1
CCW = 0
SPR = 200
SLEEP.off() #puts the board in sleep mode
DIR.on() #sets to clockwise
delay = 0.0208

# setup pump pins
VALVE = gpio.OutputDevice(13)
# GPIO.setup(13, GPIO.OUT)
# GPIO.output(13, GPIO.HIGH)
PUMP = gpio.OutputDevice(19)
VALVE.on()
PUMP.on()

def turnStepper(deg, direction):
    DIR.on() if direction == 1 else DIR.off()
    steps = int(SPR*deg/360)
    SLEEP.on()
#     STEP.blink(n=steps)
    for x in range(steps):
        STEP.on()
        sleep(delay)
        STEP.off()
        sleep(delay)
        print(x)
    SLEEP.off()
    print('done')
    
