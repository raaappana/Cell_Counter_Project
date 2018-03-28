import os

from PIL import Image

import directoryMaker


def throwSomeException(str):
    print('-- ')
    print('-- ')
    print(str)
    print('-- ')
    print('-- ')
    print("Unexpected error:", sys.exc_info()[0])

def cropImage(image,Xcent,Ycent,sideLength):

    width, height = image.size

    halfLength = int(sideLength/2)

    xinit = int(Xcent - halfLength)
    xend = int(Xcent + halfLength)
    yinit = int(Ycent - halfLength)
    yend = int(Ycent + halfLength)

    if xinit < 0:
        xinit = 0
    if yinit < 0:
        yinit = 0
    if xend > width:
        xend = width
    if yend > height:
        yend = height

    try:
        croppedImage = image.crop((xinit,yinit,xend,yend))

    except:
        throwSomeException('Could not crop cell image, cropping radius may need to be adjusted')
        raise

    return croppedImage


# imageDat [0]= image id
# 1 = # cell objects in image
# 2 = file path
# 3 = image name

# object dat [0] = image id
# 1 = obId (starting at 1)
# 2 = x
# 3 = y

def processImage(imagedat):
    imageID = imagedat[0]
    numCellObjects = imagedat[1]
    parentDir = imagedat[2]
    imageNameWithext = imagedat[3]
    imageNameNoext, imageExt = os.path.splitext(imageNameWithext)

    imageAbsPath = os.path.join(parentDir, imageNameWithext)

    return imageID, numCellObjects, parentDir, imageNameWithext,imageNameNoext, imageAbsPath, imageExt

def processObject(objectdat):
    imageID = objectdat[0]
    objectID = objectdat[1]
    xcent = objectdat[2]
    ycent = objectdat[3]

    return imageID, objectID, xcent,ycent

def processImageandObjectData(imageData, objectData, resultsDirectoryPath):

    imageID = 0

    counter = 0

    croppedImPathList = []


    for object in objectData:

        counter = counter+1

        objImageID, objectID, xcent, ycent = processObject(object)

        if imageID != objImageID:

            #make a new array in the cropped image pathList for the image
            croppedImPathList.append([])

            imagedat = imageData[objImageID-1]
            imageID, numCellObjectsInImage, parentDir, imageNameWithext, imageNameNoext, imageAbsPath, imageExt = processImage(imagedat)

            print('Opening image ' + str(imageNameWithext) + ' at ' + str(imageAbsPath))

            sampleSplit=imageAbsPath.split('\\')
            sampleNum=sampleSplit[len(sampleSplit)-2]

            # Try opening the image from the absolute path
            try:
                image = Image.open(imageAbsPath)
            except:
                throwSomeException('Could not open ' + str(imageNameNoext) + ' at ' + str(
                    imageAbsPath) + ' make sure image is present at specified path')
                raise

        assert (imageID == objImageID)

        croppedObjImage = cropImage(image,xcent,ycent,70)

        #Save the cropped image
        croppedImPath=os.path.join(resultsDirectoryPath,imageNameNoext+'--Sample--'+sampleNum+"--Object--"+str(objectID)+imageExt)
        croppedObjImage.save(croppedImPath)

        croppedImPathList[objImageID-1].append(croppedImPath)

    return croppedImPathList

# # Go through every image, and process the image
# for imagedat in imageData:
#
#     imageID, numCellObjectsInImage, parentDir, imageNameWithext, imageNameNoext, imageAbsPath, imageExt = processImage(
#         imagedat)
#
#     print('Opening image ' + str(imageNameWithext) + ' at ' + str(imageAbsPath))
#
#     # Try opening the image from the absolute path
#     try:
#         image = Image.open(imageAbsPath)
#     except:
#         throwSomeException('Could not open ' + str(imageNameNoext) + ' at ' + str(
#             imageAbsPath) + ' make sure image is present at specified path')
#         raise
#
#     for object in objectData:
#         objImageID, objectID, xcent, ycent = processObject(object)
#
#         assert (imageID == objImageID)
#
#         croppedObjImage = cropImage(image, xcent, ycent, 70)
#
#         # Save the cropped image
#         croppedImPath = os.path.join(resultsDirectoryPath, imageNameNoext + "-object" + str(objectID) + imageExt)
#         croppedObjImage.save(croppedImPath)
#
#     pass
#
# return 1