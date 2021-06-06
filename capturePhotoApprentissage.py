import cv2
import glob
import imutils
import os
import shutil
import sys
import tkinter


def getNameFile(chemin):
    c = chemin.split("/")
    c2 = c[-1].split(".")
    valRet = c2[0]
    for i in range(1,len(c2)-1):
        valRet += "."+c2[1]

    return valRet

def capturePhoto(numeroCamera, dossierPhoto):
    # creation dossier photo
    if os.path.exists("./photo/"):
        shutil.rmtree('./photo/')
    os.mkdir("./photo/")

    listImg = glob.glob(dossierPhoto+"*.png")
    listImg.sort()
    vidcap = cv2.VideoCapture(numeroCamera)

    success = True

    numImg = 0

    #recuperer taille ecran
    root = tkinter.Tk()
    widthScreen = root.winfo_screenwidth()
    heightScreen = root.winfo_screenheight()-150
    
    img=cv2.imread(listImg[numImg])
    cv2.namedWindow("screen")
    cv2.moveWindow("screen", 0,0)
    output = cv2.resize(img, (widthScreen, heightScreen))
    cv2.imshow("screen", output)

    
    while success and numImg<len(listImg):

        success, image = vidcap.read()

        if(cv2.waitKey(1) & 0xFF == ord(' ')):
            cv2.imwrite("./photo/"+getNameFile(listImg[numImg])+".jpg", image)
            numImg+=1
            if(numImg<len(listImg)):
                img=cv2.imread(listImg[numImg])
                cv2.namedWindow("screen")
                cv2.moveWindow("screen", 0,0)
                output = cv2.resize(img, (widthScreen, heightScreen))
                cv2.imshow("screen", output)
    
    cv2.destroyAllWindows()

    vidcap.release()

def main(argv):
    if(len(argv)==2):
        try:
            numeroCamera = int(argv[0])
        except ValueError:
            print("It's not an integer !\n")
            exit(0)
        if not os.path.exists(argv[1]):
            print("Folder name not found.\n")
            exit(0)
            
        capturePhoto(numeroCamera, argv[1])
    else:
        print("capturePhotoApprentissage missing operand.\n")
        exit(0)
    

if __name__ == "__main__":
   main(sys.argv[1:])