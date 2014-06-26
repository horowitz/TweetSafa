# -*- coding: utf-8 -*-
from __future__ import division
import ReadData as read
import PreprocessTweets as preprocess
import UtilsTweetSafa as utils
import Smoothing as linear
import numpy as np
import CrossValidation as cv

import sys

maxNgram = 3

# 1-. Read dataset and create tweetList fullfilled of Tweet object*

dataset = "../Dataset/output_complete.txt"

tweetList = read.read_tweets_dataset(dataset)

# 2-. Pre-process state

tweetListPreProcessed = preprocess.main(tweetList)
corpusNgrams, arrayLanguages,arrayLanguagesFull = utils.obtainNgrams(tweetListPreProcessed, maxNgram+1)
arrayLanguagesFull = utils.orderVector(arrayLanguagesFull)
    # Raw data -> tweetList
    # Clean data -> tweetListPreProcessed

#utils.printTweets(tweetListPreProcessed)

# 3-. Algorithms
#
# 3.1-. OBTAIN N-GRAMS



#print(corpusNgrams.get(str(4)).get('es'))

# Example:  print(corpusNgrams.get(str(3)).get('pt'))

# Clean data -> Algorithm



# 3.2-. Algorithms: Bayesian Networks
#   3.2.1-. Linear interpolation
#       Generate linear coefficients: input (n-grams and language)
#       Smooth data

linearCoefficients = list()
for language in arrayLanguages:
    grams = []
    for gram in xrange(1, maxNgram+1):
        grams.append(corpusNgrams.get(str(gram)).get(language))
    linearCoefficients.append(linear.getlinearcoefficients(language, grams, maxNgram))

max = 0;
tweetEN = "Tomorrow is going to be a good day to go to the beach."
tweetPT = "Amanhã será um dia muito bom, como ir para a praia."
tweetCA = "Demà farà un dia molt bo, com per anar a la platja."
tweetEU = "Bihar egun oso ona egingo du, hondartzara joateko modukoa."
tweetGL = "Mañá será un día moi bo, como ir á praia."
tweetES = "Mañana hará un dia muy bueno, como para ir a la playa."

realEN = "'Where is the moment when we need it the most' @ Salvador de Bahía, Brasil http://instagram.com/p/lX9he2CrnF/ "
realPT = "Faltam 11 dias para fazer anos, hmm"
realCA = "Comença al Centre Fraternal la Jornada de Cooperaciò i defensa dels DDHH al Sàhara Occidental pic.twitter.com/lmOEAfww7K"
realEU = "@ErrealaAle @rnrjukebox hori ere pentsatu det, km mordoxka zegoen bukaera arte bakarrik juteko,... bestela oso erraz jun da,..."
realGL = "Pouco frío tiña eu logo no carnaval en Abadín"
realES = "#Lugo #a6 (amarillo) obras en #PedrafitaDoCebreiro carril izquierdo cerrado km431,3~430 decreciente #dgt #trafico http://tuitrafico.com/estado-del-trafico/galicia/lugo/pedrafita-do-cebreiro/199833/ …"
realUND = "Hhhhhhhhhhhhjjhhhhhhhhhhhh"
realOTHER = "Buongiorno ai nostri ascoltatori in Italia :)) pic.twitter.com/zfGpYc3oxo"

text = preprocess.preprocessText(realOTHER)

print text

for linearCoefficients in linearCoefficients:
    # print str(linearCoefficients[0])+" "+str(linearCoefficients[1])+" "+str(linearCoefficients[2]) + " " + str(linearCoefficients[3])+"\n"

    prob = 1.0;

    for i in range(0, len(text)-maxNgram):
        t = list()
        for g in xrange(0, maxNgram):
            t.append(text[i+g])
            grams = []
            for gram in xrange(1, maxNgram+1):
                grams.append(corpusNgrams.get(str(gram)).get(linearCoefficients[0]))
        probability = linear.probability(grams, linearCoefficients, t, maxNgram)
        prob = prob * probability

    if prob >= max:
        language = linearCoefficients[0]
        max = prob

    sys.stdout.write("Sequence probability in "+str(linearCoefficients[0])+": "+str(prob)+"\n")


sys.stdout.write("\n    Tweet:  "+str(text.encode("utf-8")))
sys.stdout.write("\n    Tweet language:   "+str(language)+"\n    Probability of:  "+str(max)+"\n")

# 3.3-. Algorithms: Ranking Methods
# print(arrayLanguagesFull)
# cv.nestedCrossValidation(tweetListPreProcessed,5,5,[0,0,0],arrayLanguagesFull)
# cv.crossValidation(tweetListPreProcessed,1,[0,0,0],arrayLanguagesFull)
# 3.4-. Out-of-place Measure



# EVALUATION:

# PARA USAR EL tweetLID_eval.pl TENEMOS QUE CREAR UN FICHERO EN EL QUE LOS TWEETS ESTEN DE LA SIGUIENTE MANERA:

#   tweet_id<TAB>language
#
#   HE PUESTO UN EJEMPLO COGIENDO TWEETS DE OUTPUT_COMPLETE LOS HE GUARDADO EN EL FICHERO result.txt
#
#   Para probar el codigo ejecutar la siguiente linea:
#
#    perl tweetLID_eval.pl -d ../Dataset/result.txt -r ../Dataset/output_complete.txt ->../Dataset/evaluation_ouput.txt
#
#   LO QUE HACE ESTA LINEA ES MIRAR EL RESULT.TXT CREADO POR NOSOTROS, COMPARARLO CON EL OUTPUT_COMPLETE.TXT Y GUARDAR LOS
#       RESULTADOS EN EL EVALUATION_OUTPUT.TXT
#
#   AHI ESTA TODA LA INFORMACION DE LA PRECISION RECAL ETC... EXPLICADA.