from gpiozero.pins.pigpio import PiGPIOFactory
import gpiozero as GPIO
from time import sleep

GPIO.Device.pin_factory = PiGPIOFactory()

servo = GPIO.AngularServo(14)

servo.value = 0.5
sleep(10)
servo.value = 0
