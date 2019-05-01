# Image Processing Project
#### Authors: Giavinh Lam, Greg Hetherington and Petar Kenic
Created on March 23, 2019

### About
Open-ended project designed for CIS4720. Web application which detects and computes the ripeness of a banana.
React.js used for the frontend and Python 3 used for the backend (image processing algorithm, file operations...).

React.js frontend deployed on xx.xx and Flask Web App (used as a server to handle requests) deployed using pythonanywhere.

### Running the webserver

* install python dependencies
    ```
    pip install flask
    pip install flask-cors --upgrade
    ```
* navigate to /backend/src

    ```
    export FLASK_APP=server.py
    flask run
    ```
* common errors
    * use 'set' instead of 'export' for Windows
    * under PowerShell (ex. when using VS code) use the following command
        ```
        $env:FLASK_APP = "server.py"
        flask run
        ```
      
### Updating npm files

* delete "package-lock.json" file
    
    ```
    npm install
    ```
    
### Launching website
* navigate to root folder

    ```
    npm start
    ```


### Notes:
* Images can be most file types (ie. PNG, JPG, TIFF, etc)
* Input image must have dimensions > 100 x 100 pixels
* Libraries that must be updated:
    * numpy
    * PIL
    * imageIO
    * cv2
    (pip can be used to update these)
