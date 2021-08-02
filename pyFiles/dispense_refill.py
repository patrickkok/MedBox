from time import sleep
import gpiozero as gpio
import RPi.GPIO as GPIO
import pigpio
import json
import serial
import pygame
pygame.init()
pygame.mixer.music.load('/home/pi/Documents/MedBox/pyFiles/smasho_mode_alarm.mp3')

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
delay = 1.2/SPR

# setup pump pins
VALVE = gpio.OutputDevice(13)
PUMP = gpio.OutputDevice(19)
DIST = gpio.InputDevice(23) #0 means that smth is close
VALVE.off()
PUMP.off()

# setup scanner pins
SCANNER = gpio.OutputDevice(4)
SCAN = gpio.OutputDevice(27)

# setup current sensor pins and variables
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)


def play_alarm():
    pygame.mixer.music.play()
    # sounds alarm 
    return True

def stop_alarm():
    pygame.mixer.music.stop()
    return True

def turn_servo(pos):
    pi = pigpio.pi()
#     pi.set_PWM_frequency(24, 50)
    pos_dict = {"default": 1580, "dispense": 1400}
    pi.set_servo_pulsewidth(24,pos_dict[pos])    
    sleep(1)
    pi.set_servo_pulsewidth(24,0)
    return True
# turn_servo("dispense")
# sleep(2)
# turn_servo("default")


def lower_nozzle():
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(17,2000)
    cutoff = 12450
    PUMP.on()
    VALVE.off()
    sleep(1)
    try:
        for i in range(0, 1001, 10):
            pi.set_servo_pulsewidth(17, 2000-i)
            sleep(0.3)
            print(chan.value, cutoff)
            if chan.value >= cutoff:
                pi.set_servo_pulsewidth(17, 2000)
                sleep(2)
                pi.set_servo_pulsewidth(17, 0)
                break
        
    except KeyboardInterrupt:
        pi.set_servo_pulsewidth(17, 2000)
        pi.set_servo_pulsewidth(17, 0)
        print('interrupted')
    pi.set_servo_pulsewidth(17, 2000)
    sleep(1)
    pi.set_servo_pulsewidth(17, 0)
    return True

def dispense(med_id, qty):
    qty_left = qty
    container = Containers(DIR, STEP, SLEEP)
    container_id = container.getContainer(med_id)
    container.rotateContainerToDispenseArea(container_id)
    while qty_left != 0:
        lower_nozzle() #turns on pump and lowers vacuum nozzle, the nozzle will rise after getting clsoe to a pill
        turn_servo("dispense")#moves nozzle over the dispensing area
        sleep(2)
        VALVE.on()
        sleep(1)
        PUMP.off()
        VALVE.off()
        sleep(2)
        turn_servo("default")
        qty_left = qty_left - 1
    container.updateContainerInformation(container_id, -qty)
    container.writeToFile()    
    return True


   # show all medicines 

    # [ (iterate for each medicine) state machine 
    # GUI prompt  to scan 
    # turn on scanner 
    # wait here untill scanner is pressed or back is pressed 
    # if scanner returns a value 
        # get medicine ID 
        # if container exists get id, else allocate and return id 
        # rotate the slot to the area 
        # prompt UI to enter number of pill and click next 
    # ]


def refillProcess() : 
    # pull updated prescription 
    container = Containers(DIR, STEP, SLEEP) 
    stateMachine = True ; 
    state = 'barcode'
    while(stateMachine) : 
        if (state=="barcode") : 
            #display the relevant details on the front end - Wentao
            # information on what medicine are to be filled up 
            medicine_id = checkBarcode() ; 
            if medicine_id!=None : 
                state = "rotate"

            # add GUI interrupt 
        elif (state=="rotate") : 
            container_id = container.getContainer(medicine_id)
            if container.rotateContainerToRefillArea() : 
                state="wait"
            else : 
                state = "error"
                message = "couldn't rotate container"
        elif (state=="wait") : 
            # wait for a button push on gui and number of pills form input 
            # update infromation i.e container.json
            if refillComplete() : 
                state = "finish"
            else : 
                state = "barcode" 
        elif (state=="finish"): 
            container.writeToFile() 
            stateMachine = False 
        elif  (state=="error") : 
            error = "there was some error" 
            stateMachine = False 
        else : 
            state = "error" 
            error = "invalid sate" 

    return  True     



def refillComplete() : 
    # return true if all the medicines have been refilled 
    # return false if more medicines have to be filled
    return 


def checkBarcode() :
    # turn on scanner and reads te barcode. returns a 5 digit id
    ser = serial.Serial("/dev/ttyS0", 115200, timeout=0.5)
    SCANNER.on()
    SCAN.off() #button not pressed
    info = b''
    sleep(1)
    while info == b'':
        print('scanning')
        SCAN.on()
        counter = 0
        while info == b'' and counter <= 4:
            info = ser.readline()
            sleep(1)
            counter += 1
        SCAN.off()
        sleep(1)
    f = open('med_id.json')
    med_id_check = json.load(f)
    info = str(tuple(list(info)))
    print(info)
    SCANNER.off()
    for i in med_id_check:
        if i == info:
            return med_id_check[i]["id"]
        else:
            None
    return None 
    


def pullPrescription() : 
    # if prescription is updated 
        # update the prescription 
    return True 


class Containers() : 
    def __init__(self, DIR, STEP, SLEEP) : 
        self.DIR = DIR
        self.STEP = STEP
        self.SLEEP = SLEEP
        self.data = None 
        self.filled_containers = {}
        self.unfilled_containers = [] 
        self.current_pos = None 
        self.extractContainerData() 
    
    def extractContainerData(self) : 
        f  = open('container.json')
        self.data = json.load(f)
        self.current_pos = self.data["current_pos"]
        for i in self.data:
            if i!="current_pos" : 
                if self.data[i]["filled"]==1 : 
                    self.filled_containers[self.data[i]["medicine"]["id"]] = i
                else : 
                    self.unfilled_containers.append(i) 
        f.close() 

    def getContainer(self, medicineID ) : 
        # if container exists get id, else allocate and return id 
        # if no free container return None 
        if medicineID in self.filled_containers : 
            return self.filled_containers[medicineID]
        else : 
            if len(self.unfilled_containers)==0 : 
                return None 
            else : 
                container_id  = self.unfilled_containers.pop(0) 
                self.data[container_id]["filled"] = 1 
                self.data[container_id]["quantity_left"] = 0 
                self.data[container_id]["medicine"] = {
                    "id": medicineID,
                    "name": None, # need to retrive somehow from db ? 
                    "message": None # need to retrive from db ? 
                }
                self.filled_containers[medicineID] = container_id
                return container_id
    
    def calc_turn_angle(self, current, destination):
        CW = 1
        CCW = 0
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

    def turn_stepper(self, deg, direction):
        SPR = 200
        delay = 1.2/SPR
        self.DIR.on() if direction == 1 else self.DIR.off()
        steps = int(SPR*deg/360)
        self.SLEEP.on()
        sleep(0.5)
        for x in range(steps):
            self.STEP.on()
            sleep(delay)
            self.STEP.off()
            sleep(delay)
        sleep(0.5)
        self.SLEEP.off()
        print('turnt')

    def updateContainerInformation(self, container_id, number_of_pills) : 
        # update infromation in the container.json file
        self.data[container_id]["quantity_left"] += number_of_pills 

    def rotateContainerToRefillArea(self,container_id) : 
        offset = 2
        ids = int(container_id[-1])
        current = int(self.data['current_pos'])  #current container at the refill spot
        destination = ids - offset
        if destination <= 0 :
            destination = 12 - destination
        else:
            None
        if current != destination:
            ang, dire = self.calc_turn_angle(current, destination)
            print(ang, dire)
            self.turn_stepper(ang, dire)
            self.data['current_pos'] = destination
            self.current_pos = destination
        else:
            None
        # return true upon success and false upon failure 
        return True 
        

    def rotateContainerToDispenseArea(self, container_id) : 
        ids = int(container_id[-1])
        current = int(self.data['current_pos'])
        destination = ids
        print(current, destination)
        if current != destination:
            ang, dire = self.calc_turn_angle(current, destination)
            print(ang, dire)
            self.turn_stepper(ang+10, dire)
            self.data['current_pos'] = destination
            self.current_pos = destination
        else:
            None
        # return true upon success and false upon failure 
        return True 
    
    
    def writeToFile(self) : 
        with open("container.json", 'w') as outfile:
            json.dump(self.data, outfile)

container = Containers(DIR, STEP, SLEEP)
# import os
# os.system('sudo killall pigpiod')
# os.system('sudo pigpiod')
container.rotateContainerToDispenseArea("container_6")
# dispense(52,1)


print('done')







 