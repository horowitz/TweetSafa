from __future__ import division
import numpy as np

def getlinearcoefficients(language, grams, maxNgrams):
    lambdas = [0]*(maxNgrams)

    totalCount = grams[0].N()

    for maxgram in grams[maxNgrams-1].items():
        count = []
        count.append(maxgram[1])
        maxCount = maxgram[1]
        # print maxgram[0] # ngram
        # print maxgram[1] # count

        for gram in reversed(xrange(0, maxNgrams-1)):
            # print grams[gram].items()
            compare = maxgram[0][0:gram+1]

            for g in grams[gram].items():
                if g[0] == compare:
                    count.append(g[1])
                    break

        count.append(totalCount)

        cases = list()
        max = 0.0
        temp = 0
        contador = 0
        for c in reversed(xrange(0, len(count)-1)):
            contador = contador + 1
            try:
                case = (count[c]-1)/(count[c+1]-1)
                if case >= max:
                    max = case
                    temp = contador-1
            except ZeroDivisionError:
                case = 0.0
            cases.append(case)

        lambdas[temp] = lambdas[temp] + maxCount

    all(lambdas)/sum(lambdas)

    linearCoefficients = list()

    linearCoefficients.append(language)

    for l in lambdas:
        linearCoefficients.append(l/sum(lambdas))


    return linearCoefficients


def probability(grams, lic, text, maxNgrams):
    text = tuple(text)
    totalCount = grams[0].N()
    count = []
    for gram in reversed(xrange(0, maxNgrams)):
        compare = text[0:gram + 1]
        a = True
        for g in grams[gram].items():
            if g[0] == compare:
                count.append(g[1])
                a = False
                break
        if a:
            count.append(0)
    count.append(totalCount)

    contador = 0
    probabilities = [0]*(maxNgrams)

    for c in reversed(xrange(0, len(count)-1)):
        contador = contador + 1
        try:
            prob = (lic[contador] * count[c])/(count[c+1])
        except ZeroDivisionError:
            prob = 0.0
        probabilities[contador-1] = prob
    return sum(probabilities)+0.000000000000000000001