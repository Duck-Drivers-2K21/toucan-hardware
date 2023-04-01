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
  # TODO: Cut down the final image to not include the empty portion.

def combine_images(images: list):
  # TODO: Extend to work with multiple images (we want to do it pairwise)
  pass
