import observation
import cv2
import RPi.GPIO as GPIO

if __name__ == '__main__':
    servo_pin = 22
    frequency = 50  # in hz

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo_pin, GPIO.OUT)

    pwm = GPIO.PWM(servo_pin, frequency)
    pwm.start(0)

    images = observation.capture_view(pwm)
    for i in range(len(images)):
        cv2.imwrite(f"result_{i}.png", images[i])

    pwm.stop()
    GPIO.cleanup()
