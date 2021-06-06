import cv2 as cv
import fonctionReconnaissance as fctReco
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer
import readDataFile as rdf
import sys
import time
import tkinter
  
class Window(QMainWindow):
    
    def __init__(self, numCam):
        super().__init__()

        self.initVariable()
        self.initDisplay()

        self.modelFile = fctReco.getModelFile()
        self.configFile = fctReco.getConfigFile()
        self.face_model = fctReco.getFaceModel()
        self.landmark_model = fctReco.getLandmark_model()

        self.cap = cv.VideoCapture(numCam)
        if not self.cap.isOpened:
            print('--(!)Error opening video capture')
            exit(0)

        self.timer=QTimer()
        self.timer.timeout.connect(self.timerCaptureFrame)
        self.timer.start(100)


    def initDisplay(self):
        """
        initialize the screen with the different shapes
        """
        self.setWindowTitle("face tracker")
        self.setGeometry(0, 0, self.widthScreen, self.heightScreen)
        self.creationOfFace()


    def initVariable(self):
        """
        initialize the different variables
        """
        (self.bornMinAxeX, self.bornMaxAxeX, self.bornMinAxeY, self.bornMaxAxeY) = rdf.getMinMaxXY('fileDataFace.xls')

        root = tkinter.Tk()
        self.widthScreen = root.winfo_screenwidth()
        self.heightScreen = root.winfo_screenheight()-150

        self.ratioPositionViewX = (self.widthScreen)/(self.bornMaxAxeX-self.bornMinAxeX)
        self.ratioPositionViewY = (self.heightScreen)/(self.bornMaxAxeY-self.bornMinAxeY)


    def creationOfFace(self):
        """
        creation of the different parts of the face
        """
        # creation of left eye
        self.eyeLeft = QLabel('', self)
        self.eyeLeft.setStyleSheet("border-image: url('./images/image visage de fer/eye.png') 0 0 0 0 stretch stretch;")

        # creation of right eye
        self.eyeRight = QLabel('', self)
        self.eyeRight.setStyleSheet("border-image: url('./images/image visage de fer/eye.png') 0 0 0 0 stretch stretch;")

        # creation of nose
        self.nose = QLabel('', self)
        self.nose.setStyleSheet("border-image: url('./images/image visage de fer/nose.png') 0 0 0 0 stretch stretch;")

        # creation of face
        self.face = QLabel('', self)
        self.face.setStyleSheet("border: 3px solid red; border-radius: 40px;")

        # creation watch zone
        self.watchZone = QLabel('', self)
        self.watchZone.resize(100, 100)
        self.watchZone.setStyleSheet("border : 4px solid darkgreen; background : lightgreen; border-radius: 40px;")

        # display of the different forms
        self.show()


    def detectAndDisplay(self, img):
        """
        detects the position of the face and the position looking
        then change the displayed positions 
        """
        self.height, self.width = img.shape[:2]
        self.rationHeight = self.heightScreen/self.height
        self.ratioWidth = self.widthScreen/self.width

        faces = fctReco.find_faces(img, self.face_model)

        if(len(faces)==1):
            face = faces[0]
            marks = fctReco.detect_marks(img, self.landmark_model, face)

            image_points = fctReco.getTabPointsFace(marks)

            for p in image_points:
                cv.circle(img, (int(p[0]), int(p[1])), 4, (0,0,255), -1)

            topNose = image_points[0]
            bottomNose = image_points[1]
            eyeLeftLeft = image_points[3]
            eyeLeftRight = image_points[4]
            eyeRightLeft = image_points[5]
            eyeRightRight = image_points[6]
            chin = image_points[2]

            self.changePosition(face, topNose, bottomNose, eyeLeftLeft, eyeLeftRight, eyeRightLeft, eyeRightRight, chin)


    def changePosition(self, face, topNose, bottomNose, eyeLeftLeft, eyeLeftRight, eyeRightLeft, eyeRightRight, chin):
        """
        Changes the position of different objects from the positions detected on the camera
        """
        self.face.move(
                        int(((face[0])*self.ratioWidth)),
                        int((face[1])*self.rationHeight)
                        )
        self.face.resize(
                        int((face[2]-face[0])*self.ratioWidth),
                        int((face[3]-face[1])*self.rationHeight)
                        )

        self.eyeLeft.move(
                        int(((eyeLeftLeft[0])*self.ratioWidth)),
                        int((eyeLeftLeft[1]-((eyeLeftRight[0] - eyeLeftLeft[0])//3))*self.rationHeight)
                        )
        self.eyeLeft.resize(
                        int((eyeLeftRight[0] - eyeLeftLeft[0])*self.ratioWidth),
                        int(((eyeLeftRight[0] - eyeLeftLeft[0])//1.5)*self.rationHeight)
                        )
        
        self.eyeRight.move(
                        int(((eyeRightLeft[0])*self.ratioWidth)),
                        int((eyeRightLeft[1]-((eyeRightRight[0] - eyeRightLeft[0])//3))*self.rationHeight)
                        )
        self.eyeRight.resize(
                        int((eyeRightRight[0] - eyeRightLeft[0])*self.ratioWidth),
                        int(((eyeRightRight[0] - eyeRightLeft[0])//1.5)*self.rationHeight)
                        )

        self.nose.move(
                        int(((topNose[0]-((bottomNose[1]-topNose[1])//4))*self.ratioWidth)), 
                        int((topNose[1])*self.rationHeight)
                        )
        self.nose.resize(
                        int(((bottomNose[1]-topNose[1])//2)*self.ratioWidth),
                        int((bottomNose[1] - topNose[1])*self.rationHeight)
                        )

        self.watchZone.move(
                        int(((((eyeLeftLeft[0]+eyeRightRight[0])/topNose[0])*1000)-self.bornMinAxeX) * self.ratioPositionViewX),
                        int(((bottomNose[1]-topNose[1])-self.bornMinAxeY) * self.ratioPositionViewY)
                        )

        self.show()
        

    def timerCaptureFrame(self):
        """
        function call regularly to capture and process the filmed pictures
        """
        self.ret, self.frame = self.cap.read()
        if not self.frame is None:
            self.detectAndDisplay(self.frame)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape or e.key() == Qt.Key_Q:
            self.close()

def visageLife(numero):
    try:
        numeroCamera = int(numero)
    except ValueError:
        print("Ce n'est pas un entier!")
        exit(0)
        
    # create pyqt5 app
    App = QApplication([])
    
    # create the instance of our Window
    window = Window(numeroCamera)

    # start the app
    sys.exit(App.exec())
    


def main(argv):
    if(len(argv)==1):
        visageLife(argv[0])
    else:
        print("visageFilDeFer opérande manquant.\n")
        exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
