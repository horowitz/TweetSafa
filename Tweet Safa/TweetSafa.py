import UtilsTweetSafa as utils


#sentence = 'Once upon a time there was a cat who wore boots'
#sentence = 'this is a foo bar sentences and i want to ngramize it'
#sentence = 'O portugues foi usado, naquela epoca,'
#sentence = "una frase en espanol, es una mierda de programa"
#sentence = 'La France metropolitaine possede une grande variete de paysages, entre des plaines agricoles ou boisees, des chaines de montagnes plus ou moins erodees, des littoraux diversifies et des vallees melant villes et espaces neo-naturels.'

dataSet = utils.createDataSet("datasets/eng_tweets.txt","datasets/es_tweets.txt","datasets/fr_tweets.txt","datasets/pt_tweets.txt")
#
# error = utils.crossValidationLidstone(dataSet)
# print 'Lidstone error = ' + str(error)

dataSet = utils.cleanDataset(dataSet)
m = 80
n = 100
error = utils.crossValidationRanking(m, n, dataSet)


print 'Ranking model error = ' + str(error)

