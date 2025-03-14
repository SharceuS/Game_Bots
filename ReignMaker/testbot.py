import cv2
import numpy as np
import pyautogui

# Load the reference image in color
reference_image = cv2.imread('tiles/void.png')

# Initialize the ORB detector with more features
orb = cv2.ORB_create(nfeatures=1000)

# Find the keypoints and descriptors with ORB in the reference image
kp1, des1 = orb.detectAndCompute(reference_image, None)

# Take a screenshot
screenshot = pyautogui.screenshot()
screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# Find the keypoints and descriptors with ORB in the screenshot
kp2, des2 = orb.detectAndCompute(screenshot, None)

# Initialize the FLANN-based matcher
FLANN_INDEX_LSH = 6
index_params = dict(algorithm=FLANN_INDEX_LSH, table_number=6, key_size=12, multi_probe_level=1)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

# Match descriptors using KNN
matches = flann.knnMatch(des1, des2, k=2)

# Apply ratio test
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

# Draw the matches
result_image = cv2.drawMatches(reference_image, kp1, screenshot, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# Display the result
cv2.imshow('Matches', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print the number of good matches found
print(f'Number of good matches found: {len(good_matches)}')