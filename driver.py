import observation
import preprocessor
import cv2
import RPi.GPIO as GPIO

if __name__ == '__main__':
    servo_pin = 22
    frequency = 50  # in hz

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo_pin, GPIO.OUT)

    pwm = GPIO.PWM(servo_pin, frequency)
    pwm.start(0)
    print("Capturing images")
    images = observation.capture_view(pwm)
    for i in range(len(images)):
        cv2.imwrite(f"img{i}.png", images[i])
    print("Combining images")
    result = preprocessor.combine_images(images)

    print("Writing result to file")
    cv2.imwrite("result.png", result)

    pwm.stop()
    GPIO.cleanup()
