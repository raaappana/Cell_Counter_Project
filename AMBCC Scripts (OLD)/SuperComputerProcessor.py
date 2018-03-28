# --------------------------------------------------------------------------------------------------
# Send the picture to WATSON in a Jquery, with some other information

# curl -X POST -F "images_file=@fruitbowl.jpg"
# curl -k -X POST -F "images_file=@fruitbowl.jpg" "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=371b13123bc441ab07ea52be4f2b01e1565f896b&version=2016-05-20"

# -k gets rid of security verification
# -X makes the curl listen for the POST command, which subsequently uses -F's to determine that there's more fields up ahead to analyze images.
# -F gets into field of image_file

from _collections import defaultdict
import numpy as np
import subprocess
import sys
import os
import json

import VRInterface
import excelWriter

def alternateConnectionMethod():

    # url = "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key={api-key}
    #
    # 593b9b3a1c763d32832b01aa9345dfcc0721c2d7
    # &version=2016-05-20"
    # data = ""
    # headers = {}



    # req = urllib2.Request(url, data, headers)
    # response = urllib2.urlopen(req)
    # result = response.read()

    # urllib2.Request()

    return 1

def getJSONDat(JSONPath):

    #default dictionary will make a new key if you try to append a "not-already there" key/score into it.
    defaultdictHelper = defaultdict(list)

    objectJSON = json.load(open(JSONPath))

    try:
        objectClassandScoreArray = objectJSON['images'][0]['classifiers'][0]['classes']

        # Go through the object results
        for objectClassandScoreDicts in objectClassandScoreArray:
            # And append them into the default dictionary

            objectClass = objectClassandScoreDicts['class']
            classScore = objectClassandScoreDicts['score']

            defaultdictHelper[objectClass].append(classScore)

    except:
        print('Error: File invalid or exceeded daily limit')
        pass

    return defaultdictHelper

def processJSONdat(JSONDat):

    #default dictionary will make a new key if you try to append a "not-already there" key/score into it.
    defaultdictHelper = defaultdict(list)
    #
    # # navigate the JSON file
    for JSONPath in JSONDat:

        objectJSON = json.load(open(JSONPath))

        try:
            objectClassandScoreArray = objectJSON['images'][0]['classifiers'][0]['classes']

                #Go through the object results
            for objectClassandScoreDicts in objectClassandScoreArray:
                #And append them into the default dictionary

                objectClass =objectClassandScoreDicts['class']
                classScore = objectClassandScoreDicts['score']

                defaultdictHelper[objectClass].append(classScore)

        except:
            print ('Error: File invalid or exceeded daily limit')
            pass

    # # Parse the results of the classifier. Store the score of the class into an image
    # for classAndScore in objectClassificationArray:
    #
    #     hClass = classAndScore['class']
    #     hScore = classAndScore['score']
    #     # If the class hasn't been found yet in this image, add the class to the list.
    #     if hClass not in classScores:
    #         classScores[hClass] = []
    #     # Add score to image's list of scores
    #     classScores[hClass].append(hScore)
    #
    #
    # return objectClassificationArray

    resultsDictionary = defaultdictHelper

    return resultsDictionary



def ProcessImageDataPaths(paths):

    objectTOTALData = []

    ScriptDir = os.path.dirname(os.path.realpath(__file__))
    print('Script dir =' + ScriptDir)

    curDir = os.path.abspath(os.path.curdir)
    print('Current dir =' + curDir)

    # debugLimit=0
    # for path in paths:
    #
    #     debugLimit = debugLimit + 1
    #     if debugLimit == 2:
    #         break

        folder = path[0].split('\\')
        folder = folder[len(folder)-2]

        # os.system(r'''curl -k -X POST -F "imagesfiles=@C:\Users\Andrew Raappana\Desktop
        #     ...: \Andrews Magic BCC\Results\iiiii\CroppedImageDirectory\n__1\overlap1--Sample--1
        #     ...: --Object--1.jpg" -F "parameters=@C:\Users\Andrew Raappana\Desktop\Andrews Magic
        #     ...:  BCC\AMBCC Scripts\myparams.json" "https://gateway-a.watsonplatform.net/visual-
        #     ...: recognition/api/v3/classify?api_key=593b9b3a1c763d32832b01aa9345dfcc0721c2d7&ve
        #     ...: rsion=2016-05-20"''')
        # curlHelper = ScriptDir+'\\CurlHelper.bat'
        # CWDh = curDir+"\\CroppedImageDirectory\\"+folder
        # print(CWDh)
        # os.system('''"'''+curlHelper+'''"''''')
        # input()
        # subprocess.Popen(curlHelper,cwd=CWDh,shell=True).wait()

        #
        # debugger2 = 0
        #
        # for f in os.listdir(curDir+'\\CroppedImageDirectory\\'+folder):
        #
        #     debugger2 = debugger2+1
        #     if debugger2 == 3:
        #         break

            if not os.path.exists(curDir+'\\jsonDat\\'):
                print('Making jsonDat file in '+curDir)
                os.makedirs(curDir+'\\jsonDat\\')


            fname, fext = os.path.splitext(f)

            # If the object is an image being looked at, get the data from it, curl it to the super computer, and then send the output to a json
            if (fext == '.jpg'):
                fpath = curDir + '\\CroppedImageDirectory\\' + folder+'\\'+f

                fsplit = fname.split('--')
                imName = fsplit[0]
                imSampleNum = fsplit[2]
                objNum = fsplit[4]
                print(f)

                params = ScriptDir+'''\\myparams.json"'''
                JSONPath = curDir + '\\jsonDat\\' + fname+'''.json'''
                gateway = '''"https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=593b9b3a1c763d32832b01aa9345dfcc0721c2d7&version=2016-05-20" '''

                inputer = r'''curl -k -X POST -F "imagesfiles=@''' + fpath + r'''" -F "parameters=@'''+params+ " " + gateway+ r''' > "''' + JSONPath + '''"'''
                print(inputer)
                input('CHECK PLEASE ' + 'experiment-'+folder + 'image'+fname)
                os.system(inputer)

                objectClassArray = getJSONDat(JSONPath)
                objectTOTALData.append([imName, imSampleNum, objNum, objectClassArray])

    return objectTOTALData



def analyzeClassDict(classDictionary):

    # for hclassScoresList in classDictionary:
    #     for score in hclassScoresList:
    #
    return 1






def processImageFiles(paths):




    SynopsisPageInfo = []

    totalDATA = ProcessImageDataPaths(paths)

    return totalDATA













if __name__ == '__main__':

    # url = 'https://gateway-a.watsonplatform.net/visual-recognition/api/v3/detect_faces'
    # images = {'images_file': open('prez.jpg', 'rb')}
    # payload = {'api_key': "{{{}}}".format(api_key), 'version': '2016-05-20'}
    # r = requests.post(url, files=images, params=payload)


    import requests

    url = "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify"
    images = {'imagesfiles':open(r'''C:\Users\Andrew Raappana\Desktop\Andrews Magic BCC\Results\iiii\CroppedImageDirectory\n__1\overlap1--Sample--1--Object--1.jpg''','rb')}
    payload = {'api_key': '593b9b3a1c763d32832b01aa9345dfcc0721c2d7', 'version':'2016-05-20'}

    r = requests.post(url=url,files=images,params=payload)


    ProcessImageDataPaths()
