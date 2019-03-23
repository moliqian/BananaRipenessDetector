from flask import Flask, request, send_file, Response
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

import sys
import os

curDir = sys.path[0]
sys.path.append(curDir + '/pythonTOOLBOX')

from imageIO import *
import imageIO
from PIL import Image
import cv2
import numpy as np
import argparse
import imutils
import glob

#Global Variable
inputFilename = "Bananas.jpg"
counter = 0
bananaFound = 0  # 1 - true
orientation = 0  # keeps track of input image orientation
ripe = 0

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])

	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def checkRipeness(found, image, tW, tH):
	(_, maxLoc, r) = found
	(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
	(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
	endY = endY-(int)((endY-startY)*0.05)
	startY = startY+(int)((endY-startY)*0.05)
	startX = startX + (int)((endX-startX)*0.05)
	endX = endX - (int)((endX - startX) * 0.05)
	banana = image[startY:endY, startX:endX]

	hsv = cv2.cvtColor(banana, cv2.COLOR_BGR2HSV)  # convert to HSV color space
	mask = cv2.inRange(hsv, (17, 100, 0), (36, 255, 255))
	dst = cv2.bitwise_and(banana, banana, mask=mask)
	global counter
	counter = counter + 1
	#print(mse(banana, dst))
	if mse(banana, dst) < 1000:  # if there is 1 found in the dst array, a red pixel as outlined by our boundaries exist
		return True
	else:
		return False

def imageFix(image):
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # convert to HSV color space
	mask1 = cv2.inRange(hsv, (36, 50, 0), (70, 255, 255))  # green HSV mask
	mask2 = cv2.inRange(hsv, (17, 100, 0), (36, 255, 255))  # yellow HSV mask
	mask = cv2.bitwise_or(mask1, mask2)
	mask3 = cv2.inRange(hsv, (0, 50, 0), (179, 255, 162))  # brown mask
	mask = cv2.bitwise_or(mask, mask3)
	dst = cv2.bitwise_and(image, image, mask=mask)  # generates image containing only yellow parts
	return dst

def identifyBanana(template, image):
    # imageFix(template)
    # cv2.imshow("Template", template)

    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]

    # load the image, convert it to gray-scale, and initialize the
    # bookkeeping variable to keep track of the matched region
    original = image
    image = imageFix(image)
    # cv2.imshow("image", image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    found = None

    # loop over the scales of the image
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        # resize the image according to the scale, and keep track
        # of the ratio of the resizing

        resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
        r = gray.shape[1] / float(resized.shape[1])

        # if the re-sized image is smaller than the template, then break
        # from the loop
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break
        # detect edges in the re-sized, gray-scale image and apply template
        # matching to find the template in the image

        # cv2.imshow("resize", resized)

        edged = cv2.Canny(resized, 50, 200)
        #cv2.imshow("blah", edged)
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
        # print(result)
        (minVal, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        # w, h = template.shape[::-1]
        # threshold = 0.99
        # loc = np.where(result >= threshold)
        # for pt in zip(*loc[::-1]):
        # 	cv2.rectangle(original, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        # check to see if the iteration should be visualized
        # if args.get("visualize", False):
        #     # draw a bounding box around the detected region
        #     clone = np.dstack([edged, edged, edged])
        #     cv2.rectangle(clone, (maxLoc[0], maxLoc[1]), (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
        #     cv2.imshow("Visualize", clone)
        #     cv2.waitKey(0)

        # if we have found a new maximum correlation value, then update
        # the bookkeeping variable
        if (found is None or maxVal > found[0]) and maxVal > 3000000:
            #print(minVal)
            previousfound = found
            found = (maxVal, maxLoc, r)
            if checkRipeness(found, image, tW, tH):  # Comment out this line and the two below to disable simple clothes color check
                ripe = 1
            else:
                ripe = 0

            # # exit(0)
            # (_, maxLoc, r) = found
            # (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
            # (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
            #
            # # draw a bounding box around the detected result and display the image
            # cv2.rectangle(original, (startX, startY), (endX, endY), (0, 0, 255), 2)
            # cv2.putText(original, "Ripe", (int((startX + endX) / 2.2), int(startY + ((endY - startY) * 0.1))), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)

            # if not checkClothes(found, image):  # Comment out this line and the two below to disable simple clothes color check
            # 	if previousfound is not None:
            # 		found = previousfound

    # unpack the bookkeeping variable and compute the (x, y) coordinates
    # of the bounding box based on the re-sized ratio

    if found is None:
        print('No banana found')
        # exit(0)
    (_, maxLoc, r) = found
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

    # draw a bounding box around the detected result and display the image
    # cv2.rectangle(original, (startX, startY), (endX, endY), (0, 0, 255), 2)
    if ripe == 1:
        cv2.putText(original, "Ripe", (int((startX + endX)/2.2), int(startY+((endY-startY)*0.1))), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    else:
        print(startX)
        print(endX)
        cv2.putText(original, "Not ripe", (int((startX + endX) / 2.2), int(startY + ((endY - startY) * 0.1))), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    # if not checkClothes(found, image):  # Comment out this line and the two below to disable simple clothes color check
    # image = cv2.resize(image, (1400, 900))  # resize if necessary
    # cv2.imshow("Image", original)
    # cv2.imwrite('output.png', original)  # save image as output.png in source folder
    # cv2.waitKey(0)
    return original
    
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(os.path.join("Images/", "inputfile.jpg"))
    return "Success"

@app.route('/banana')
def banana():
    inputImage = "Images/inputfile.jpg"
    img = cv2.imread(inputImage)
    template = cv2.imread('Images/bananatemplatetest.jpg')
    
    newImage = identifyBanana(template, img)
    
    #output file
    cv2.imwrite("outputImage.jpg", newImage)
    return send_file("outputImage.jpg", mimetype='image/gif')
        
if __name__ == '__main__':
    app.run(debug=True)


