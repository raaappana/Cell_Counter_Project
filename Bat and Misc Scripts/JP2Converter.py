from PIL import Image
import glymur


from os import listdir
from os.path import isfile,join

import os

curDir = os.path.abspath(os.path.curdir)

def ConvertJP2FilesFromCurDirToJpg():

    jp2files = []
    for f in listdir(curDir):
        fname , fext = os.path.splitext(f)
        if (fext=='.jp2')&(isfile(join(curDir,f))):
            jp2 = glymur.Jp2k(f)
            fullresImage = jp2[:]
            JPEG = Image.fromarray(fullresImage, 'RGB')
            newName = fname+'.jpg'
            print('Converting '+f+' to jpeg file format')
            JPEG.save(newName,"JPEG")
            print(f + ' saved as ' + newName)

    return 1

ConvertJP2FilesFromCurDirToJpg()

#img = jpp.ImageFile.Image.open('questionable2.jp2')
#img.save('classy',"JPEG")  # Output Image

#    .open('questionable2.jp2') # Input Image
#img.show()
#