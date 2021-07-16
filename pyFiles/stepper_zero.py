from time import sleep
import gpiozero as gpio
import RPi.GPIO as GPIO
import pigpio
import json

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
PUMP = gpio.OutputDevice(19)
DIST = gpio.InputDevice(23) #0 means that smth is close
VALVE.off()
PUMP.off()



def turn_stepper(deg, direction):
    DIR.on() if direction == 1 else DIR.off()
    steps = int(SPR*deg/360)
    SLEEP.on()
#     STEP.blink(n=steps)
    for x in range(steps):
        STEP.on()
        sleep(delay)
        STEP.off()
        sleep(delay)
    SLEEP.off()
    print('turnt')
    #add in an update of the current pos in json file

def turn_servo(pos):
    pi = pigpio.pi()
    if pos == 1500:
        for k in range (500, pos+1, 50):
            pi.set_servo_pulsewidth(24,k)
            sleep(0.1)
    elif pos == 500:
        for l in range (1500, pos-1, -50):
            pi.set_servo_pulsewidth(24,l)
            sleep(0.1)
    
    sleep(1)
    pi.set_servo_pulsewidth(24,0)
    
# turn_servo(500)
# sleep(3)
# print('done 500')
# for j in range(0,501, 50):
#     turn_servo(500+j)
#     sleep(0.05)
# turn_servo(1000)

def lower_nozzle():
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(17,2000)
    sleep(1) #delete later
    PUMP.on()
    VALVE.off()
    try:
        for i in range(0, 1001, 10):
            pi.set_servo_pulsewidth(17, 2000-i)
            sleep(0.3)
            if DIST.value == 0:
                pi.set_servo_pulsewidth(17, 2000)
                sleep(2)
                pi.set_servo_pulsewidth(17, 0)
                break
        
    except KeyboardInterrupt:
        pi.set_servo_pulsewidth(17, 2000)
        pi.set_servo_pulsewidth(17, 0)
        print('interrupted')

def calc_turn_angle(current, destination):
    ang = destination - current
    if 0 <= ang <= 6:
        return (30*ang),CW
    elif 7 <= ang <= 11:
        ang = 12-ang
        return (30*ang),CCW
    elif -11 <= ang <= -7:
        ang = 12 + ang
        return (30*ang),CW
    elif -6 <= ang <=-1:
        ang = (-1)*ang
        return (30*ang),CCW

def dispense(med_id, qty):
    default = 500
    dispense = 1500
    with open('/home/pi/Documents/MedBox/pyFiles/container.json', 'r') as f:
        container = json.load(f)
    current = int(container['current_pos'])
    print(current)
    for i in range(1,13):
        container_med_id = container['container_'+str(i)]['medicine']['id']
        if container_med_id == med_id:
            destination = i
            break
    print(destination)
    ang, dire = calc_turn_angle(current, destination)
    print(ang, dire)
    turn_stepper(ang, dire)
    lower_nozzle() #turns on pump and lowers vacuum nozzle, the nozzle will rise after getting clsoe to a pill
    turn_servo(dispense)#moves nozzle over the dispensing area
    VALVE.on()
    sleep(1)
    VALVE.on()
    PUMP.off()
    VALVE.off()
    turn_servo(default)
    #update pill amount in json
    return None
# dispense(1)
import os
# os.system('sudo pigpiod')

dispense(51,1)



    




 