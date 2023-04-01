import cv2

def capture_image(camera_idx):
  camera = cv2.VideoCapture(camera_idx)
  try:
    if not camera.isOpened():
      raise Exception(f"Failed to open camera {camera_idx}.")
    rtrn, frame = camera.read()
    if not rtrn:
      raise Exception("Failed to capture image.")
  finally:
    camera.release()  # Force flush the camera
  return frame
