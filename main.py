from time import sleep
from io import BytesIO
import uuid
import cv2
import boto3
import os
import json
# from botocore.exceptions import NoCredentialsError

RPI = False  # Set to `True` if you're using our embedded set-up
CAMERA_IDX = 0  # The camera number to use
DELAY = 60  # The time interval at which images are taken (in seconds)

if RPI:
  from rpi import get_frame
else:
  from camera import get_frame

# AWS Settings
BUCKET_NAME = 'toucan-data'
QUEUE_URL = 'https://sqs.eu-west-2.amazonaws.com/083551419963/toucan-ingestion'
REGION = "eu-west-2"
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# In order to uniquely identify the various cameras in our network, we use each device's MAC address
MAC_ADDRESS = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 48, 8)])

def upload_image_to_s3(frame, bucket_name, s3_key):
  """
  Uploads an image to an S3 bucket.
  :param frame: The image to upload.
  :param bucket_name: The name of the S3 bucket to upload the image to.
  :param s3_key: The key (path) where the image will be stored in the S3 bucket.
  :return: A dictionary with the result of the operation, including success status and error messages if any.
  """

  s3 = boto3.client('s3', region_name=REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
  sqs = boto3.client('sqs', region_name="eu-west-2", aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

  # Encode the frame as a JPEG image
  retval, buffer = cv2.imencode('.jpg', frame)
  if not retval:
    return {'success': False, 'message': "Error encoding frame as JPEG image."}

  # Upload the encoded image to S3
  byte_data = BytesIO(buffer)
  s3.upload_fileobj(byte_data, bucket_name, s3_key)

  sqs_payload = {
    's3_key' : s3_key,
    'mac_address' : MAC_ADDRESS,
    'size' : frame.shape
  }
  message_body = json.dumps(sqs_payload)
  response = sqs.send_message(
    QueueUrl=QUEUE_URL,
    MessageBody=message_body
  )
  return {'success': True, 'message': "Image uploaded to S3 successfully."}


def main():
  i = 0
  while True:
    try:
      frame = get_frame(CAMERA_IDX)
      cv2.imwrite(f'out{i}.png', frame)  # TODO: Remove save
      i += 1
      print(upload_image_to_s3(frame, BUCKET_NAME, str(uuid.uuid4()) + '.jpg'))
    except Exception as E:
      print(E)
      continue
    sleep(DELAY)


if __name__ == '__main__':
  main()
