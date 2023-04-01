from time import sleep
import cv2

RPI = False  # Set to `True` if you're using our embedded set-up
CAMERA_IDX = 0  # The camera number to use

if RPI:
  from rpi import get_frame
else:
  from camera import get_frame

for i in range(5):
  cv2.imwrite(f'out{i}.png', get_frame(CAMERA_IDX))
