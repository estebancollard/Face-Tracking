import apprentissagePhoto
import capturePhotoApprentissage
import os
import numCamera
import sys
import visageFilDeFer

def main(argv):
    numeroCamera = numCamera.testCameraChoix()
    capturePhotoApprentissage.capturePhoto(numeroCamera, "./images/image texte apprentissage/")
    apprentissagePhoto.getDataPhoto()
    visageFilDeFer.visageLife(numeroCamera)

if __name__ == "__main__":
   main(sys.argv[1:])
