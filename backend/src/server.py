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

# Global Variables
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
    banana = image[startY:endY, startX:endX]

    hsv = cv2.cvtColor(banana, cv2.COLOR_BGR2HSV)  # convert to HSV color space
    mask = cv2.inRange(hsv, (17, 50, 0), (36, 255, 255))
    dst = cv2.bitwise_and(banana, banana, mask=mask)
    # cv2.imshow("og", dst)
    # cv2.imshow("og2", banana)
    global counter
    counter = counter + 1
    # print("WOOHOO" + str(mse(banana, dst)))
    if mse(banana, dst) < 5000:  # if yellow mask still very similar to original - ripe
        return 1
    else:
        mask = cv2.inRange(hsv, (36, 50, 0), (70, 255, 255))  # green mask
        dst = cv2.bitwise_and(banana, banana, mask=mask)
        # cv2.imshow("bladh", dst)
        # cv2.imshow("bladh2", banana)
        print("wahee" + str(mse(banana, dst)))
        if mse(banana, dst) < 6500:
            return 2  # unripe
        else:
            return 0  # overripe


def imageFix(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # convert to HSV color space
    mask = cv2.inRange(hsv, (3, 28, 0), (81, 255, 255))  # mask that extracts yellow/brown/green colors (allows only acceptable banana colors)
    dst = cv2.bitwise_and(image, image, mask=mask)  # generates image containing only yellow parts
    return dst

def identifyBanana(templatePath, image):
    global ripe
    # global counter
    dimensionMultiplier = 1  # for large input image cases, this var is used to label end image with correct x and y
    mH = 0  # dimensions for best match found
    mW = 0

    (imageX) = image.shape[1]
    original = image

    if imageX > 300:  # resize image if too large for better algorithm accuracy and runtime
        r = 300.0 / imageX  # 1000 pixels divided by the image's width (to find ratio difference)
        dim = (300, int(image.shape[0] * r))  # dimensions array containing new width and proper height
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)  # resize method
        # cv2.imshow("new?", image)
        dimensionMultiplier = r
        print('Resized')

    image = imageFix(image)  # get rid of most unnecessary colors except for yellow, brown, green colors
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    found = None

    for image_path in os.listdir(templatePath):
        # create the full input path and read the file
        input_path = os.path.join(templatePath, image_path)
        template = cv2.imread(input_path)

        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 50, 200)
        (tH, tW) = template.shape[:2]
        print('initial ' + input_path)
        # loop over the scales of the image changed from 0.2 to 0.1 to make certain images more accurate
        for scale in np.linspace(0.1, 1, 50)[::-1]:
            # resize the image according to the scale, and keep track of the ratio of the resizing
            resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
            r = gray.shape[1] / float(resized.shape[1])

            # if the re-sized image is smaller than the template, then return error image
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break

            # detect edges in the re-scaled gray-scale image and use template matching to find the template image
            edged = cv2.Canny(resized, 50, 200)
            # cv2.imshow("edged", edged)
            result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
            (minVal, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            # if we have found a new maximum correlation value, then update the bookkeeping variable
            if (found is None or maxVal > found[0]) and maxVal > 3000000:
                print('max: ' + str(maxVal))
                # print('min: ' + str(minVal))
                # > 4000000 good match
                print(input_path)
                found = (maxVal, maxLoc, r)
                mH = tH
                mW = tW

        # unpack the bookkeeping variable and compute the (x, y) coordinates
        # of the bounding box based on the re-sized ratio

    if found is None:
        # print('No banana found')
        h, w, d = original.shape
        cv2.rectangle(original, (int(w/2)-100, int(h/4)-20), (int(w/2)+100, int(h/4)+10), (0,0,0), cv2.FILLED)
        cv2.putText(original, "No banana found", (int(w/2)-95, int(h/4)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        return original
    else:
        tW = mW
        tH = mH
        ripe = checkRipeness(found, image, tW, tH)
        (_, maxLoc, r) = found
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

        # print(dimensionMultiplier)
        startX = int(startX * (1/dimensionMultiplier))
        startY = int(startY * (1/dimensionMultiplier))
        endX = int(endX * (1/dimensionMultiplier))
        endY = int(endY * (1/dimensionMultiplier))

        # draw a bounding box around the detected result and display the image
        cv2.rectangle(original, (startX, startY), (endX, endY), (0, 0, 255), 2)
        if ripe == 1:
            cv2.putText(original, "Ripe", (int((startX + endX) / 2) - 30, startY+17),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (40, 0, 255), 2)
        elif ripe == 0:
            cv2.putText(original, "Overripe", (int((startX + endX) / 2) - 40, startY+17),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (40, 0, 255), 2)
        else:
            cv2.putText(original, "Unripe", (int((startX + endX) / 2) - 35, startY+17),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (40, 0, 255), 2)
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
    # template = cv2.imread('Images/bananatemplatetest2.jpg')
    
    newImage = identifyBanana('template', img)
    
    #output file    
    cv2.imwrite("outputImage.jpg", newImage)
    return send_file("outputImage.jpg", mimetype='image/gif')
        
if __name__ == '__main__':
    app.run(debug=True)


