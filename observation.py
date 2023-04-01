import cv2
import time

def capture_image(camera_idx):
    camera = cv2.VideoCapture(camera_idx)
    if not camera.isOpened():
        print("Failed to open camera! Restart.")
        exit()  # TODO: make exception
    rtrn, frame = camera.read()
    if not rtrn:
        print("Failed to capture image!")
    camera.release()  # Force-flush the camera
    return frame

def set_pos(pwm, pos):
    dc_range = (5, 10)
    dc = dc_range[0] + (pos / 180) * (dc_range[1] - dc_range[0])  # Duty cycle
    pwm.ChangeDutyCycle(dc)
    time.sleep(0.1)
    pwm.ChangeDutyCycle(0)

def capture_view(pwm) -> list:
    images = []
    for pos in range(60, 121, 20):
        set_pos(pwm, pos)
        images.append(capture_image(0))
        time.sleep(1)
    print(f"Captured {len(images)} images.")
    return images
