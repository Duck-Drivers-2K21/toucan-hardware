from time import sleep
import cv2
import RPi.GPIO as GPIO

import preprocessor
import camera

# SERVO SETTINGS
SERVO_PIN = 22
FREQUENCY = 50  # in hz

# Field of View for Camera
START = 60
END = 120
INC = 20

def set_pos(pwm, pos):
    dc_range = (5, 10)
    dc = dc_range[0] + (pos / 180) * (dc_range[1] - dc_range[0])  # Duty cycle
    pwm.ChangeDutyCycle(dc)
    sleep(0.1)
    pwm.ChangeDutyCycle(0)

def capture_view(camera_idx, pwm, reverse = False) -> list:
    images = []
    start = START if not reverse else END
    end = END + 1 if not reverse else START - 1
    inc = INC if not reverse else -INC
    for pos in range(start, end, inc):
        set_pos(pwm, pos)
        images.append(camera.get_frame(camera_idx))
        sleep(0.75)
    if reverse:
        images.reverse()
    return images


reverse = False  # Optimization - please ignore

def get_frame(camera_idx):
    global reverse
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    pwm = GPIO.PWM(SERVO_PIN, FREQUENCY)
    pwm.start(0)

    print(f"Capturing images (reverse={reverse})")
    images = capture_view(camera_idx, pwm, reverse)
    # for i in range(len(images)):
    #     cv2.imwrite(f"img{i}.png", images[i])
    pwm.stop()
    GPIO.cleanup()
    print(f"Combining {len(images)} images")
    return preprocessor.combine_images(images)
