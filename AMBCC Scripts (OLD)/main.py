import os
import datetime as date

import SQLProcessor
import directoryMaker
import objectProcessing
import SuperComputerProcessor
import excelWriter

def get_file_meta_data(fileName):
    fname, _ = os.path.splitext(f)
    dat = fname.split("__")
    print(dat)
    return dat


def main():

    curDirr = os.path.abspath(os.curdir)

    print(curDirr)

    topDir = curDirr.split('\\')

    # Make a workbook using the experiments name
    topDir = topDir[len(topDir)-1]

    excelBook,synopsis = excelWriter.makeNewExperimentWorkBook(topDir)

    SynopsisPageInfo = []

    row =0
    sampleSeth=''

    for SAMPLE in SQLProcessor.getSQLFileFromOperatingDir():

        SQLFilePath= curDirr+"\\"+SAMPLE

        imageDat, objectDat, nameDat = SQLProcessor.getAndExtractImageAndObjectDataFromSQLfile(SAMPLE,SQLFilePath)

        workingDir = directoryMaker.makeResultsFile(topDir,nameDat)

        croppedImagePathList = objectProcessing.processImageandObjectData(imageDat, objectDat, workingDir)

        totalDataOnObjects=SuperComputerProcessor.processImageFiles(croppedImagePathList)

        if sampleSeth != (nameDat[0]):
            row = 0
            sampleSeth = nameDat[0]
            sampleSetPage = excelBook.add_worksheet(nameDat[0])

        # Get the total number of cells above the 50%, 80%, 90%, 95% and 99% threshold
        malaboveThreshold,uninfectedAboveThreshold,row=excelWriter.WriteReportExcelSheet(sampleSetPage,totalDataOnObjects,row)

        # thresh = [50, 60, 70, 80, 90, 95, 99]
        # name of sample, ___, and number of cells above a certain threshold
        SynopsisPageInfo.append([nameDat[0],nameDat[3],malaboveThreshold, uninfectedAboveThreshold])

    excelWriter.WriteSynopsis(synopsis,SynopsisPageInfo)

    excelBook.close()


if __name__ == "__main__":
    main()
    print ('--- Super Computer Processing Finished. Exiting main.py ---')
    # Export number of uninfected, infected, and non-cell objects to Excel

#C:\Users\Andrew Raappana\BloodCellObjects1.db

