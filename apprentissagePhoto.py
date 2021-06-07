import cv2 
import glob
import xlwt
import sys
import fonctionReconnaissance as fctReco


def writeOnFile(sheet, topNose, bottomNose, eyeLeftLeft, eyeLeftRight, eyeRightLeft, eyeRightRight, chin, photo, indice):
    '''
    writes in the excel file passed in parameter the various information of the face
    '''
    photoSplit = photo.split(",")
    sheet.write(indice, 0, int(photoSplit[0][-3:]))
    sheet.write(indice, 1, int(photoSplit[1][:3]))

    sheet.write(indice, 2, topNose[0])
    sheet.write(indice, 3, topNose[1])

    sheet.write(indice, 4, bottomNose[0])
    sheet.write(indice, 5, bottomNose[1])

    sheet.write(indice, 6, eyeLeftLeft[0])
    sheet.write(indice, 7, eyeLeftLeft[1])

    sheet.write(indice, 8, eyeLeftRight[0])
    sheet.write(indice, 9, eyeLeftRight[1])

    sheet.write(indice, 10, eyeRightLeft[0])
    sheet.write(indice, 11, eyeRightLeft[1])

    sheet.write(indice, 12, eyeRightRight[0])
    sheet.write(indice, 13, eyeRightRight[1])

    sheet.write(indice, 14, chin[0])
    sheet.write(indice, 15, chin[1])


def initialisationExcel(sheet):
    '''
    initialize the excel file where the results will be written
    '''
    sheet.write(0, 0, "X")
    sheet.write(0, 1, "Y")
    sheet.write(0, 2, "topNoseX")
    sheet.write(0, 3, "topNoseY")
    sheet.write(0, 4, "bottomNoseX")
    sheet.write(0, 5, "bottomNoseY")
    sheet.write(0, 6, "eyeLeftLeftX")
    sheet.write(0, 7, "eyeLeftLeftY")
    sheet.write(0, 8, "eyeLeftRightX")
    sheet.write(0, 9, "eyeLeftRightY")
    sheet.write(0, 10, "eyeRightLeftX")
    sheet.write(0, 11, "eyeRightLeftY")
    sheet.write(0, 12, "eyeRightRightX")
    sheet.write(0, 13, "eyeRightRightY")
    sheet.write(0, 14, "chinX")
    sheet.write(0, 15, "chinY")


def getDataPhoto():
    '''
    retrieves jpg files from the photo folder performs facial recognition on them
    '''
    listPhoto = glob.glob("./photo/*.jpg")
    listPhoto.sort()

    modelFile = fctReco.getModelFile()
    configFile = fctReco.getConfigFile()
    face_model = fctReco.getFaceModel()
    landmark_model = fctReco.getLandmark_model()

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('feuille1')
    initialisationExcel(sheet)
    indice = 1


    for photo in listPhoto:

        img = cv2.imread(photo)
        
        faces = fctReco.find_faces(img, face_model)
        for face in faces:
            marks = fctReco.detect_marks(img, landmark_model, face)
                
            image_points = fctReco.getTabPointsFace(marks)
            
            writeOnFile(sheet, image_points[0], image_points[1], image_points[3], image_points[4], image_points[5], image_points[6], image_points[2], photo, indice)

            indice+=1
        
    workbook.save('fileDataFace.xls')

def main(argv):
    getDataPhoto()

if __name__ == "__main__":
   main(sys.argv[1:])