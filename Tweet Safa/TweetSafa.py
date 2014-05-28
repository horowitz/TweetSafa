
import lidstonLanguageClassification as llc


#sentence = 'Once upon a time there was a cat who wore boots'
sentence = 'this is a foo bar sentences and i want to ngramize it'
#sentence = 'O portugues foi usado, naquela epoca,'
#sentence = "una frase en espanol, es una mierda de programa"
#sentence = 'La France metropolitaine possede une grande variete de paysages, entre des plaines agricoles ou boisees, des chaines de montagnes plus ou moins erodees, des littoraux diversifies et des vallees melant villes et espaces neo-naturels.'

language = llc.lidstoneLanguageClassification(sentence)


print language