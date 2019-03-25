# Image Processing Project
#### Authors: Giavinh Lam, Greg Hetherington and Petar Kenic
Created on March 23, 2019

### About
Open-ended project designed for CIS4720. Web application which detects and computes the ripeness of a banana.
React.js used for the frontend and Python used for the backend (image processing algorithm, file operations...)

### Running the webserver
* navigate to /backend/src

    ```
    export FLASK_APP=server.py
    flask run
    ```
    
### update npm files

* delete "package-lock.json" file
    
    ```
    npm install
    ```
    
### launch website
* navigate to main git folder

    ```
    npm start
    ```


### Notes:
* Images can be most file types (ie. PNG, JPG, TIFF, etc)
* Input image must have dimensions > 100x100 px
* Libraries that must be updated:
    * numpy
    * PIL
    * imageIO
    * cv2
    (pip can be used to update these)
