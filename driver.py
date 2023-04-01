import cv2
import time

import RPi.GPIO as GPIO

import observation
import preprocessor


if __name__ == '__main__':
    servo_pin = 22
    frequency = 50  # in hz

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo_pin, GPIO.OUT)

    pwm = GPIO.PWM(servo_pin, frequency)
    pwm.start(0)

    reverse = False
    for i in range(2):
        print(f"Capturing images (reverse={reverse})")
        images = observation.capture_view(pwm, reverse)
        for i in range(len(images)):
            cv2.imwrite(f"img{i}.png", images[i])
        print("Combining images and writing to file")
        cv2.imwrite("result.png", preprocessor.combine_images(images))
        reverse = not reverse
        time.sleep(2)

    pwm.stop()
    GPIO.cleanup()
