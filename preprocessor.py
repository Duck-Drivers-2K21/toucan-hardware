import cv2
import numpy as np
# from PIL import Image

def pair_wise_match(img1, img2):
  # Find keypoints and descriptors
  orb = cv2.ORB_create()
  keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
  keypoints2, descriptors2 = orb.detectAndCompute(img2, None)

  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
  matches = bf.match(descriptors1, descriptors2)
  matches = sorted(matches, key = lambda x : x.distance)
  print("Number of matching points:", len(matches))

  good_matches = matches[:50]  # Can reduce the candidate number for performance

  # Get the coords of matched points
  src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
  dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)

  # Calculate homography
  homography, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

  # Warp images
  res = cv2.warpPerspective(img1, homography, (img1.shape[1] + img2.shape[1], img2.shape[0]))
  res[0 : img2.shape[0], 0 : img2.shape[1]] = img2
  print(res.shape)
  cv2.imwrite("result.png", res)  # TODO: Add date & time in the name
  cv2.imwrite("cropped_res.png", crop_image(res))
  return res

def crop_image(img):
  # Go from the rightmost position and start moving left
  columns = img.sum(axis=0)
  co_point = 0  # Cutoff point
  for col in range(columns.shape[0] - 1, -1, -1):
    if np.all(columns[col] == 0):
      co_point = col
    else:
      break
  print(co_point)
  return img[:, :co_point]

def combine_images(images: list):
  # TODO: Extend to work with multiple images (we want to do it pairwise)
  pass


image1 = cv2.imread('image1.png')
image2 = cv2.imread('image2.png')
pair_wise_match(image1, image2)
