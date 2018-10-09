#Standard imports
import numpy as np
import cv2


#Read image
img = cv2.imread("goodSpinach.jpg")
#img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
imgOrig = img.copy()


#Create window
cv2.namedWindow('Images')


#Convert BGR to HSVimg
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


#Color strength parameters in HSV -- Full image
lower_full = np.array([1,70,30])
upper_full = np.array([255,255,255])


#Color strength parameters in HSV -- Brown spots
lower_brown = np.array([6, 100, 20])
upper_brown = np.array([39, 255, 200]) ######Tune this value ######


# Filtering
maskFull = cv2.inRange(hsv, lower_full, upper_full)
kernelFull = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(1,1))
resultFull = cv2.dilate(maskFull,kernelFull)

maskBrown = cv2.inRange(hsv, lower_brown, upper_brown)
kernelBrown = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
resultBrown = cv2.dilate(maskBrown, kernelBrown)
resultBrown = maskBrown


# Get full area from contouring
im2, contours, hierarchy = cv2.findContours(resultFull.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
resultFull = cv2.cvtColor(resultFull, cv2.COLOR_GRAY2BGR)
if len(contours) != 0:
    largestContourArea = 0
    for (i, c) in enumerate(contours):
        if cv2.contourArea(c) > largestContourArea:
            largestContourArea = cv2.contourArea(c)
    fullArea = largestContourArea
    print("Full area: " + str(fullArea))

# Contours -- Brown spots
im2, contours, hierarchy = cv2.findContours(resultBrown.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
resultBrown = cv2.cvtColor(resultBrown, cv2.COLOR_GRAY2BGR)
brownAreaSum = 0
brownAreaMax = 0
brownAreaMin = 0

if len(contours) != 0:
    for (i, c) in enumerate(contours):
        brownArea = cv2.contourArea(c)

        if brownArea > (fullArea * .001):

            # Set color of spots based on size
            brownAreaSum = brownAreaSum + brownArea

            if brownArea > brownAreaMax:
                brownAreaMax = brownArea
            if brownArea < brownAreaMin:
                brownAreaMin = brownArea

            range = (brownAreaMax - brownAreaMin)

            color = ((brownArea - brownAreaMin) / range) * 255

            cv2.drawContours(img, c, -1, (255, 255 - color, 0), 4)


brownRatio = (brownAreaSum / fullArea) * 100
print("Brown ratio: " + str(round(brownRatio,2)) + "%")


# Stack results
#output = np.vstack((imgOrig, img))
output = img

cv2.imwrite("/Users/rafrank/Desktop/CapstoneCV/static/spinOutA.jpg", output)

# Resize
max_dimension = float(max(resultBrown.shape))
scale = 900/max_dimension
result = cv2.resize(resultBrown, None, fx=scale, fy=scale)

#font = cv2.FONT_HERSHEY_SIMPLEX
#cv2.putText(output, ("Brown ratio: " + str(round(brownRatio,2)) + "%"),(5,385), font, 0.5, (0,0,0), 1, cv2.LINE_AA)
