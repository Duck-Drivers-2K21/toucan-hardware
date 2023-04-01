import cv2
import RPi.GPIO as GPIO
import observation
import preprocessor

SERVO_PIN = 22
FREQUENCY = 50  # in hz

reverse = False
i = 0

def get_frame(camera_idx):
    global reverse
    global i  # TODO: Remove i
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    pwm = GPIO.PWM(SERVO_PIN, FREQUENCY)
    pwm.start(0)

    print(f"Capturing images (reverse={reverse})")
    images = observation.capture_view(camera_idx, pwm, reverse)
    # for i in range(len(images)):
    #     cv2.imwrite(f"img{i}.png", images[i])
    print("Combining images and writing to file")
    cv2.imwrite(f"result{i}.png", preprocessor.combine_images(images))  # Return the image instead of saving to file
    i += 1
    # TODO: Send result to pipeline
    reverse = not reverse

    pwm.stop()
    GPIO.cleanup()
