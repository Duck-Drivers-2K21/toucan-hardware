import cv2
import RPi.GPIO as GPIO
import time

def set_pos(pwm, pos):
    dc_range = (5, 10)
    dc = dc_range[0] + (pos / 180) * (dc_range[1] - dc_range[0])  # Duty cycle
    pwm.ChangeDutyCycle(dc)
    time.sleep(0.1)
    pwm.ChangeDutyCycle(0)
    time.sleep(2)

def capture_image(camera):
    rtrn, frame = camera.read()
    if not rtrn:
        print("Failed to capture image!")
    return frame

def capture_view(camera, pwm):
    images = []
    for pos in range(0, 181, 45):
        print(f"Capturing image at angle {pos}.")
        images.append(capture_image(camera))
        time.sleep(10)
        set_pos(pwm, pos)
    set_pos(pwm, 0)  # Reset camera position
    # Save images to file  # TODO: We can simply pass them to the other script.
    for i in range(len(images)):
        cv2.imwrite(f"result_{i}.png", images[i])

if __name__ == '__main__':
    # Camera setup
    camera = cv2.VideoCapture(0)  # We're using a single camera
    if not camera.isOpened():
        print("Failed to open camera! Restart.")
        exit()

    frequency = 50  # in hz
    servo_pin = 22

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo_pin, GPIO.OUT)

    pwm = GPIO.PWM(servo_pin, frequency)
    pwm.start(0)

    capture_view(camera, pwm)

    camera.release()
    pwm.stop()
    GPIO.cleanup()
