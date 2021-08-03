import pigpio
# import os
# os.system("sudo pigpiod")
from time import sleep
print("starting")
pi = pigpio.pi()
# pi.set_servo_pulsewidth(24,1400)#24
# print('dispense pos')
# sleep(0.9)
# pi.set_servo_pulsewidth(24,0)
# sleep(1)
# print('turning to default')
# pi.set_servo_pulsewidth(24,1580)
# sleep(0.9)
# pi.set_servo_pulsewidth(24,0)
max_val = 1200
min_val = 700
try:
    for i in range (max_val, min_val+1, -25):
        pi.set_servo_pulsewidth(24, i)
        sleep(0.2)
    sleep(2)
    pi.set_servo_pulsewidth(24,max_val)
    sleep(2)
    pi.set_servo_pulsewidth(24,0)
except KeyboardInterrupt:
    pi.set_servo_pulsewidth(24,max_val)
print('done')