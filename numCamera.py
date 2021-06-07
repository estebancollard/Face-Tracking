import cv2 as cv
import sys

def getListNumCamera():
    '''
    returns the list of available camera numbers
    '''
    l = []
    for i in range(16):
        vidcap = cv.VideoCapture(i)
        if vidcap.isOpened():
            l.append(i)
    return l

def testCameraChoix():
    '''
    function that makes the user test the selected camera number
    '''
    l=getListNumCamera()
    if(len(l)>0):
        print(str(len(l))+" camera found.")
        print("the numbers found are", end="")
        for n in l:
            print(" "+str(n), end="")
        print("\n")

        numSaisie = 0
        while(numSaisie!=-1):
            numSaisie = int(input("Enter the camera number you wish to test, -1 if you have finished : "))
            
            if(numSaisie in l):
                print("press escape to close the window.")
                cap = cv.VideoCapture(numSaisie)
                while True:
                    ret, frame = cap.read()
                    if frame is None:
                        print('--(!) No captured frame -- Break!')
                        break
                    cv.imshow('Capture - Face detection', frame)
                    if cv.waitKey(10) == 27:
                        break
                cv.destroyAllWindows()
        while(numSaisie not in l):
            numSaisie = int(input("Enter the number of the camera you wish to use : "))
            if(numSaisie not in l):
                print("Invalid camera number.")
        return numSaisie
    else:
        print("No camera found.")
        exit(0)

def main(argv):
    testCameraChoix()

if __name__ == "__main__":
   main(sys.argv[1:])
