from time import sleep

import camera

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
    print(f"Captured {len(images)} images.")
    if reverse:
        images.reverse()
    return images
