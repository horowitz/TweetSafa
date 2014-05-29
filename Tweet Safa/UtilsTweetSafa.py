import lidstonLanguageClassification as llc
import time


#_____________________________________________________
#
#
#                   Utils class
#
#
#
#_____________________________________________________

langArray = ['en','es','fr','pt']

##
#   CreateDataSet method
#
#       Input: engFilePath = English dataset path.
#              esFilePath = Spanish dataset path.
#              frFilePath = French dataset path.
#              ptFilePath = Portuguese dataset path.
#
#       Output: 

def createDataSet(engFilePath,esFilePath,frFilePath,ptFilePath):
    dataSet =  list()
    for line in open(engFilePath, 'r'):
        dataSet.append([line,'en'])
    for line in open(esFilePath, 'r'):
        dataSet.append([line,'es'])
    for line in open(frFilePath, 'r'):
        dataSet.append([line,'fr'])
    for line in open(ptFilePath, 'r'):
        dataSet.append([line,'pt'])

    return dataSet


def formatDataset(allTexts):
    dataSet = list()

    for textList in allTexts:
        text_string=''
        for sentence in textList:
            text_string+=str(sentence[0])
        dataSet.append(text_string)
    return dataSet


#Clean set of texts
def getAllItemsByLanguage(dataSet,value):
    result = list()
    for item in dataSet:
        if item[1] == value:
            result.append(item)
    return result


def getAllLanguagesSet(dataSet):
    langSet=list()
    for lang in langArray:
        langSet.append(getAllItemsByLanguage(dataSet,lang))
    return langSet

def crossValidationLidstone(dataSet):

    error = 0.0
    iter = 0
    step = 5

    while iter < len(dataSet):
        trainSet = dataSet

        testSet = trainSet.pop(iter)

        allTexts = getAllLanguagesSet(dataSet)

        allTexts = formatDataset(allTexts)

        t0 = time.time()

        preditectedLang = llc.lidstoneLanguageClassification(testSet[0],allTexts)

        print time.time()-t0


        if testSet[1] == 'en':
            language = 0
        elif(testSet[1] == 'es'):
            language = 1
        elif(testSet[1] == 'fr'):
            language = 2
        elif(testSet[1] == 'pt'):
            language = 3

        iter += step
        if preditectedLang == language:
            error += 0
        else:
            error += 1
        print 'error'+str(error)
    iter = (iter - step)/step+1
    error = error/iter
    print error
    return error