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
import time

#Global Variable
inputFilename = "Bananas.jpg"

def algorithm(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    weaker = np.array([12,80,80])
    stronger = np.array([41,255,255])
    mask = cv2.inRange(hsv, weaker, stronger)
    imageMasked = cv2.bitwise_and(image,image, mask= mask)

    return imageMasked
    
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(os.path.join("Images/", "inputfile.jpg"))
    return "Success"

@app.route('/banana')
def fireDetection():
    inputImage = "Images/inputfile.jpg"
    
    img = cv2.imread(inputImage)
    
    newImage = algorithm(img)
    
    #outpur file
    cv2.imwrite("outputImage.jpg", newImage)
    return send_file("outputImage.jpg", mimetype='image/gif')
        
if __name__ == '__main__':
    app.run(debug=True)


