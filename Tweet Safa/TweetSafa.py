
import lidstonLanguageClassification as llc
import time

langArray = ['en','es','fr','pt']
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

#sentence = 'Once upon a time there was a cat who wore boots'
sentence = 'this is a foo bar sentences and i want to ngramize it'
#sentence = 'O portugues foi usado, naquela epoca,'
#sentence = "una frase en espanol, es una mierda de programa"
#sentence = 'La France metropolitaine possede une grande variete de paysages, entre des plaines agricoles ou boisees, des chaines de montagnes plus ou moins erodees, des littoraux diversifies et des vallees melant villes et espaces neo-naturels.'


# file = open("eng_tweets.txt", "r")
# en_text = file.readline()
# en_text = en_text.lower()
#
# file = open("es_tweets.txt", "r")
# es_text = file.read()
# es_text = es_text.lower()
#
# file = open("fr_tweets.txt", "r")
# fr_text = file.read()
# fr_text = fr_text.lower()
#
# file = open("pt_tweets.txt", "r")
# pt_text = file.read()
# pt_text = pt_text.lower()
#
# allTexts = [en_text, es_text, fr_text, pt_text]

# language = llc.lidstoneLanguageClassification(sentence, allTexts)

dataSet = createDataSet("eng_tweets.txt","es_tweets.txt","fr_tweets.txt","pt_tweets.txt")

error = crossValidationLidstone(dataSet)

print 'Error = '+ str(error)

