import xlsxwriter
import os
import xlrd
import numpy as np

# Ihe first page of the worksheet will have a statistical synopsis of all the images processed.
# The subsequent pages are filled with the probabilities attained from the visual recognition server

def makeNewExperimentWorkBook(ExperimentName):
    #Make an excel sheet named "Experiment#.xlsx

    #This code tries to make a new experiment#.xlsx file for each experiment. (Experiment1.xlsx, Experiment2.xlsx, etc.)
    fileName = ExperimentName+'.xlsx'

    #
    # while os.path.exists(fileName):
    #     experimentNum = experimentNum + 1
    #     fileName = 'Experiment'+str(experimentNum)+'.xlsx'
    #
    #    if experimentNum == 100:
    #        fileName = input('Too many experiments found, please specify excel file name (don\'t include .xlsx)')
    #        break

    workbook = xlsxwriter.Workbook(fileName)
    synopsis = workbook.add_worksheet('Synopsis')

    return workbook, synopsis

def WriteReportExcelSheet(hSheet,sampleSet,row):

    if row == 0:

        hSheet.write(0,0,'Malaria infected RBC')
        hSheet.write(0,1,'Malaria uninfected RBC')
        hSheet.write(0,2,'Sample number')
        hSheet.write(0,3,'Object number')
        hSheet.write(0,4, 'Root image')

        # move down a row
        row += 1

    mal_inf_tot=[]
    un_inf_tot=[]

    #should be object, not sample
    #and sample instead of sample
    for sample in sampleSet:

        # imName=sample[0]
        # imSampleNum = sample[1]
        # objNum = sample[2]
        mal_inf = sample[3]['malariaInfectedRBC']
        un_inf= sample[3]['malariaUninfectedRBC']

        #write the malaria infected, uninfected, sample number, and object number
        hSheet.write( row, 0, mal_inf[0])
        hSheet.write( row, 1, un_inf[0])
        hSheet.write( row, 2, int(sample[1][0]))
        hSheet.write( row, 3, int(sample[2]))

        mal_inf_tot.append(mal_inf)
        un_inf_tot.append(un_inf)

        #When new image, write new address
        if (int(sample[2])==1):
            hSheet.write(row,4,(sample[0])+'.jpg')


        row +=1

    m=np.matrix(mal_inf_tot)
    u=np.matrix(un_inf_tot)

    thresh = [.50,.60,.70,.80,.90,.95,.99]

    i =0
    m_above_thresh=[]
    u_above_thresh=[]

    m_d=[]
    u_d=[]

    for t in thresh:
        m_above_thresh.append(np.sum(m>t,axis=0))
        u_above_thresh.append(np.sum(u>t,axis=0))

        # m_d.append(np.sum(m>t,axis=0))
        # u_d.append(np.sum(u>t,axis=0))

    return m_above_thresh, u_above_thresh, row

        # # For each VR class, record the class and the probabilities of each image with it.
        # for hClass in sample:
        #     # Get the prob data associated with the class
        #     datForThatClass = sample[hClass]
        #     # Write the class name on the top
        #     hSheet.write(row, col, hClass)
        #     row = row + 1
        #     # Write the data from the class below
        #     for dat in datForThatClass:
        #         hSheet.write(row, col, dat)
        #         row = row + 1
        #
        #     ########################################################################
        #     # Reset the row and move onto the next class/collumn
        #     row = 0


def WriteSynopsis(hSheet, data ):

    row = 0

    # 50, 60, 70, 80, 90, 95, 99

    hSheet.write(0,0, 'Sample Set Name')
    hSheet.write(0,1, 'Sample Number')
    hSheet.write(0,2, 'Malaria Infected: Above 50%')
    hSheet.write(0,3, 'Malaria Infected: Above 60%')
    hSheet.write(0,4, 'Malaria Infected: Above 70%')
    hSheet.write(0,5, 'Malaria Infected: Above 80%')
    hSheet.write(0,6, 'Malaria Infected: Above 90%')
    hSheet.write(0,7, 'Malaria Infected: Above 95%')



    hSheet.write(0,9, 'Uninfected: Above 50%')
    hSheet.write(0,10, 'Uninfected: Above 60%')
    hSheet.write(0,11, 'Uninfected: Above 70%')
    hSheet.write(0,12, 'Uninfected Above 80%')
    hSheet.write(0,13, 'Uninfected: Above 90%')
    hSheet.write(0,14, 'Uninfected: Above 95%')

    for dat in data:

        row = row + 1

        hSheet.write(row,0,str(dat[0]))
        hSheet.write(row,1,int(dat[1]))

        hSheet.write(row,2,int(dat[2][0]))
        hSheet.write(row,3,int(dat[2][1]))
        hSheet.write(row,4,int(dat[2][2]))
        hSheet.write(row,5,int(dat[2][3]))
        hSheet.write(row,6,int(dat[2][4]))
        hSheet.write(row,7,int(dat[2][5]))

        hSheet.write(row,9,int(dat[3][0]))
        hSheet.write(row,10,int(dat[3][1]))
        hSheet.write(row,11,int(dat[3][2]))
        hSheet.write(row,12,int(dat[3][3]))
        hSheet.write(row,13,int(dat[3][4]))
        hSheet.write(row,14,int(dat[3][5]))

        #
        # #Write the class names analyzed
        # col = 1
        # for classNameStr in classList:
        #     a = 1;
        #     a = classList[classNameStr]
        #     synopsisPage.write((row*3)-2,col,classNameStr)
        #     col = col+1
        #
        # for i in range(0,len(LowerConfidenceBound)):
        #     synopsisPage.write(row*3-1,i+1,str(UpperConfidenceBound[i]))
        #     synopsisPage.write(row*3,i+1,str(LowerConfidenceBound[i]))

#a = {'class' : 'red', 'num' : [1,2,3]}
#b = {'class' : 'blue', 'num' : [1,2,3,4,5,6]}



#First: make the workbook/synopysis page (makeNewExperimentWorkbook does both of these)
#workbook, synopsisPage = makeNewExperimentWorkBook()

#synopsisPage.write(0,0,'hello')


#second: take image data and store it in the excel sheet
#c = saveImageData(workbook, a, 'hello')
#saveImageData(workbook, b, 'bye')

#a = workbook.sheetnames;

#b = workbook.worksheets_objs

#b = 2
#third: analyze image data, and update synopsis sheet
#statResults = analyzeProbs(imageDat)
#a = updateSynopsys(workbook,synopsisPage,statResults)

#Close the workbook when done.
#workbook.close()



if __name__ =='__main__':
    dat= {'malariaInfectedRBC': [0.0445256, 0.0425729,0], 'malariaUninfectedRBC' : [0.580059, 0.591577,1]}
    setName='test1'
    ExperimentName = 'Test'

    dat = [dat,dat]

    XL, syn = makeNewExperimentWorkBook(ExperimentName)
    a,b = WriteReportExcelSheet(dat,XL,setName)

    WriteSynopsis()

    XL.close()
