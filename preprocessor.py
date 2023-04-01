import cv2
import numpy as np
# from PIL import Image


# TODO: Extend to work with multiple images (we want to do it pairwise)
img1 = cv2.imread("img1.png")
img2 = cv2.imread("img2.png")

# Find keypoints and descriptors in both images
orb = cv2.ORB_create()
keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
keypoints2, descriptors2 = orb.detectAndCompute(img2, None)

# Match the keypoints
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(descriptors1, descriptors2)
matches = sorted(matches, key = lambda x : x.distance)
print("Number of matching points:", len(matches))

# Choose the top 50 matches  # TODO: Can reduce the candidate number for performance
good_matches = matches[:50]

# Get the coordinates of the matched keypoints in both images
src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)

# Find the homography between the two sets of points
M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

# Use the homography to warp img1 onto img2
res = cv2.warpPerspective(img1, M, (img1.shape[1] + img2.shape[1], img2.shape[0]))
res[0 : img2.shape[0], 0 : img2.shape[1]] = img2

cv2.imwrite("result.png", res)  # TODO: Add date & time in the name

print(res.shape)


# TODO: Cut down the final image to not include the empty portion.


# Display the result
# cv2.imshow("Stiched image", res)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# TODO: Save to file
