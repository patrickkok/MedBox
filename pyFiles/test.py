import pigpio
from time import sleep
print("starting")
pi = pigpio.pi()
pi.set_servo_pulsewidth(24,1400)#24
print('dispense pos')
sleep(1)
pi.set_servo_pulsewidth(24,0)
sleep(1)
print('turning to default')
pi.set_servo_pulsewidth(24,1580)
sleep(1)
pi.set_servo_pulsewidth(24,0)


print('done')