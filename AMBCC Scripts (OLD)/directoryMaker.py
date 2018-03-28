import datetime
import os

def throwSomeException(str):
    print('-- ')
    print('-- ')
    print(str)
    print('-- ')
    print('-- ')
    print("Unexpected error:", sys.exc_info()[0])

def makeFileIfNotThere(Path):
    if not os.path.exists(Path):
        os.makedirs(Path)
        print ('Making directory at ' + Path)
    else:
        throwSomeException("Could not make directory at "+ Path)
    pass

def makeResultsFile(SQLFileName, fNameDat ,curDir = os.path.abspath(os.path.curdir)):

    SQLFileName, _ = os.path.splitext(SQLFileName)

    date = datetime.datetime.now()

    resultsDir = curDir + '\\Image-Analysis-Results\\'

    # if it's the first run of the program, we need to make a new results file
    if not os.path.exists(resultsDir):
        os.makedirs(resultsDir)
        print ('Making cropped image directory at ' + resultsDir)

# make a cropped image dump file in the experiment output folder
    instanceDir = curDir + '\\CroppedImageDirectory\\' + fNameDat[0] + '__'+ fNameDat[3]

    if not os.path.exists(instanceDir):
        print('Making cropped image directory at ' + instanceDir)
        os.makedirs(instanceDir)

    return instanceDir
