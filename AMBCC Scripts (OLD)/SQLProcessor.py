import os
import sqlite3
import sys

from os import listdir
from os.path import isfile,join

def throwSomeException(str):
    print('-- ')
    print('-- ')
    print(str)
    print('-- ')
    print('-- ')
    print("Unexpected error:", sys.exc_info()[0])


def getConnectionToSQLiteFile( SQLfilePath ):
    print ('connecting... ')
    print ('...')
    user_input = SQLfilePath
    assert os.path.exists(SQLfilePath), "Could not find a file at, " + SQLfilePath
    try:
        connectionToSQLite = sqlite3.connect(user_input)
    except:
        throwSomeException("The path specified at " + SQLfilePath + " did not point to an connectable SQLite file.")
        raise

    print ('connection successful')
    return connectionToSQLite

def extractImageDat(c):
    # Extract the image number ID, the number of cell-objects in the image, file location of the associated image, and the image name. Ordered by image number.
    c.execute('SELECT ImageNumber, Image_Count_Blood_Cells_Intensity_Parse, Image_PathName_BS_Ori, Image_FileName_BS_Ori  FROM Image_Per_Image ORDER BY ImageNumber')
    imageDat = c.fetchall()
    print('Image data collected')
    print('--')
    return imageDat

def extractObjectDat(c):
    # Extract image number, object number (relative to image), x, and y from image_per_object. This list is organized first by the image number, then the object number
    c.execute('SELECT ImageNumber, ObjectNumber, Blood_Cells_Intensity_Parse_Location_Center_X, Blood_Cells_Intensity_Parse_Location_Center_Y FROM Image_Per_Object ORDER BY ImageNumber, ObjectNumber')
    objectDat = c.fetchall()
    print('Cell Object data collected')
    print('--')
    return objectDat

def getSQLFileFromOperatingDir():

    curDir = os.path.abspath(os.path.curdir)

    print(curDir)

    for f in listdir(curDir):
        fname, fext = os.path.splitext(f)
        if (fext == '.db') & (isfile(join(curDir, f))):
            print(f)
            SQLFile = f

            yield SQLFile


def extractNameDat(SQLFileName):
    fname, _ = os.path.splitext(SQLFileName)
    nameDat = fname.split("__")
    return nameDat


def getAndExtractImageAndObjectDataFromSQLfile(SQLFileName,SQLPath):

    connection = getConnectionToSQLiteFile(SQLPath)
    c = connection.cursor()

    imageDat = extractImageDat(c)
    objectDat = extractObjectDat(c)

    nameDat = extractNameDat(SQLFileName)
    #os.path.dirname is the file containing the SQL file

    return imageDat, objectDat, nameDat


def fastImageCount():
    curDir = os.path.abspath(os.path.curdir)
    for f in listdir(curDir):
        fname, fext = os.path.splitext(f)
        if (fext == '.db') & (isfile(join(curDir, f))):

            fPath = curDir+'\\'+f

            try:
                connection = sqlite3.connect(fPath)
            except:
                throwSomeException(
                    "The path specified at " + SQLfilePath + " did not point to an connectable SQLite file.")
                raise

            c = connection.cursor()
            c.execute('SELECT ImageNumber, Image_Count_Blood_Cells_Intensity_Parse, Image_FileName_BS_Ori  FROM Image_Per_Image ORDER BY ImageNumber')

            imageDat = c.fetchall()

            for i in imageDat:
                print('Image number '+str(i[0])+ ' - '+ str(i[2]) + ' - has been found to have ' + str(i[1]) + ' cell objects')



if __name__ == "__main__":
    fastImageCount()