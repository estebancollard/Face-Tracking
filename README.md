# Face tracking

## Objective of the project
Detect the direction of the head in order to be able to use this position to avoid using the mouse in certain situations.

## libraries 
For the execution of this project you will need several libraries, here is how to install them.
```
pip3 install imutils
sudo apt-get install python3-tk
pip3 install opencv-python
pip3 install tensorflow
pip3 install pandas
pip3 install pyqt5
pip3 install sklearn
pip3 install xlrd
pip3 install xlwt
```

## Launch the program
You have 2 options to launch the program,
the first is to run the program allProgramme.py for this you can type the command :

```
python3 allProgramme.py
```

The second solution has conditions, it is necessary to have executed the program at least once via the first method in order to have a fileDataFace.xls with the different positions of the face. The second solution consists in executing the following command:

```
python3 visageFilDeFer.py cameraNumber
```

cameraNumber is the camera number detected by open-cv, usually 0.

## Reference
https://github.com/vardanagarwal/Proctoring-AI
