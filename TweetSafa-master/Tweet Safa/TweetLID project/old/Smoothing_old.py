from __future__ import division

def getlinearcoefficients(language, unigrams, bigrams, trigrams):
    lambda1 = 0; lambda2 = 0; lambda3 = 0;
    linearCoefficients = list()

    for tg in trigrams.items():
        unigram = tg[0][0]
        bigram = tg[0][0] + tg[0][1]
        trigram = tg[0][0] + tg[0][1] + tg[0][2]
        count_tg = tg[1]

        for bg in bigrams.items():
            if bigram == bg[0][0] + bg[0][1]:
                count_bg = bg[1]
                for ug in unigrams.items():
                    if unigram == ug[0][0]:
                        count_ug = ug[1]

        prob_tg = count_tg / count_bg
        # print prob_tg
        caseli = list()
        if (count_tg > 0):
            case = 0;
            try:
                case1 = (count_ug - 1) / (unigrams.N() - 1);
            except ZeroDivisionError:
                case1 = 0;

            try:
                case2 = (count_bg - 1) / (count_ug - 1);
            except ZeroDivisionError:
                case2 = 0;

            try:
                case3 = (count_tg - 1) / (count_bg - 1);
            except ZeroDivisionError:
                case3 = 0;

            if (case1 > case2):
                if (case1 > case3):
                    case = 1;
                elif (case3 > case2):
                    case = 3;
            elif (case2 > case3):
                case = 2;
            else:
                case = 3;

            if (case == 1):
                lambda1 = lambda1 + count_tg;
            if (case == 2):
                lambda2 = lambda2 + count_tg;
            if (case == 3):
                lambda3 = lambda3 + count_tg;


    # print unigrams.N()  #samples
    # print unigrams.B()  #outcomes
    # print unigrams.items

    normLambda1 = 0; normLambda2 = 0; normLambda3 = 0;

    lambdaSum = lambda1+lambda2+lambda3;

    normLambda1 = lambda1/lambdaSum;
    normLambda2 = lambda2/lambdaSum;
    normLambda3 = lambda3/lambdaSum;

    linearCoefficients.append(language)
    linearCoefficients.append(normLambda1)
    linearCoefficients.append(normLambda2)
    linearCoefficients.append(normLambda3)

    return linearCoefficients


def probability(corpusNgrams, lic, x, y, z):
    trigrams = corpusNgrams.get('3').get(str(lic[0]))
    bigrams = corpusNgrams.get('2').get(str(lic[0]))
    unigrams = corpusNgrams.get('1').get(str(lic[0]))

    for ug in unigrams.items():
        if z == ug[0][0]:
            count_ug = ug[1]
    try:
        px = (lic[1] * count_ug) / unigrams.N();
    except ZeroDivisionError:
        px = 0;
    except UnboundLocalError:
        px = 0;

    for bg in bigrams.items():
        if y+z == bg[0][0] + bg[0][1]:
            count_bg = bg[1]
    try:
        pxy = (lic[2] * count_bg) / count_ug ;
    except ZeroDivisionError:
        pxy = 0;
    except UnboundLocalError:
        pxy = 0;

    for tg in trigrams.items():
        if x+y+z == tg[0][0] + tg[0][1] + tg[0][2]:
            count_tg = tg[1]
    try:
        pxyz = (lic[3] * count_tg) / count_bg
    except ZeroDivisionError:
        pxyz = 0;
    except UnboundLocalError:
        pxyz = 0;


    return px + pxy + pxyz + 0.000000000001;
