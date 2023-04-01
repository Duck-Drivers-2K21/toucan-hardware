import RPi.GPIO as GPIO
import time

frequency = 50  # in hz
servo_pin = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, frequency)
pwm.start(0)

def set_pos(pwm, pos):
    dc_range = (5, 10)
    dc = dc_range[0] + (pos / 180) * (dc_range[1] - dc_range[0])  # Duty cycle
    pwm.ChangeDutyCycle(dc)
    time.sleep(0.1)
    pwm.ChangeDutyCycle(0)
    time.sleep(2)

try:
    for pos in range(0, 181, 90):
        print(pos)
        set_pos(pwm, pos)
    set_pos(pwm, 0)
    
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()

#try:
#  while True:
#    for x in range(11):
#      pwm.ChangeDutyCycle(control[x])
#      time.sleep(1)
#      print(x)
#    for x in range(9,0,-1):
#      pwm.ChangeDutyCycle(control[x])
#      time.sleep(1)
#      print(x)
#except KeyboardInterrupt:
#  GPIO.cleanup()

