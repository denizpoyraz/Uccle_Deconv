import pandas as pd
import numpy as np
import re
import glob
import math
from math import log

tslow = 25 * 60
tfast = 20
af = 1

def convolution_test(df, variable, tvariable, beta, boolib0, boolreconv, hv_hs):
    ''

    ''

    size = len(df)
    print(size)
    Islow = [0]*size; Islow_conv = [0]*size; Ifast = [0]*size; Ifastminib0 = [0]*size; Ifast_deconv = [0]*size; Ifastminib0_deconv=[0]*size
    Islow_deconv = [0]*size ; Ifast_conv = [0]*size
    Ifast_deconv_hv = [0]*size; Ifast_deconv_hs = [0]*size
    Ifastminib0_deconv_hv =[0]*size; Ifastminib0_deconv_hs =[0]*size


    for i in range(0, size - 1):

        df.at[i, 'iB0'] = 0.020

        t1 = df.at[i + 1, tvariable]
        t2 = df.at[i, tvariable]

        Xs = np.exp(-(t1 - t2) / tslow)
        Xf = np.exp(-(t1 - t2) / tfast)

        Islow[i] = beta * df.at[i, variable]
        Islow[i + 1] = beta * df.at[i + 1, variable]

        Islow_conv[i + 1] = Islow[i + 1] - (Islow[i + 1] - Islow_conv[i]) * Xs


        Ifast[i + 1] = af * (df.at[i + 1, variable] - Islow_conv[i + 1])
        Ifast[i] = af * (df.at[i, variable] - Islow_conv[i])

        Ifast_deconv[i + 1] = (Ifast[i + 1] - Ifast[i] * Xf) / (1 - Xf)


        if hv_hs == True:
            Ifast_deconv_hv[i + 1] = Ifast[i + 1] + (tfast / (t1 - t2) * (Ifast[i + 1] - Ifast[i]))
            Ifast_deconv_hs[i + 1] = Ifast[i] + (tfast / (t1 - t2) * (Ifast[i + 1] - Ifast[i]))

        if boolib0 == True:
            Ifastminib0[i] = af * (df.at[i, variable] - Islow_conv[i] - df.at[i, 'iB0'])
            Ifastminib0[i + 1] = af * (df.at[i + 1, variable] - Islow_conv[i + 1] - df.at[i + 1, 'iB0'])
            Ifastminib0_deconv[i + 1] = (Ifastminib0[i + 1] - Ifastminib0[i] * Xf) / (1 - Xf)
            if hv_hs == True:
                Ifastminib0_deconv_hv[i + 1] = Ifastminib0[i + 1] + (
                            tfast / (t1 - t2) * (Ifastminib0[i + 1] - Ifastminib0[i]))
                Ifastminib0_deconv_hs[i + 1] = Ifastminib0[i + 1] + (
                            tfast / (t1 - t2) * (Ifastminib0[i + 1] - Ifastminib0[i]))

        if boolreconv == True:
            Islow_deconv[i + 1] = (Islow_conv[i + 1] - Islow_conv[i] * Xs) / (1 - Xs)
            Ifast_conv[i + 1] = Ifast_deconv[i + 1] - (Ifast_deconv[i + 1] - Ifast_conv[i]) * Xf


        # if boolib0:
    return Islow, Islow_conv, Ifast, Ifast_deconv, Ifastminib0, Ifastminib0_deconv
        # if hv_hs: return Islow, Islow_conv, Ifast, Ifast_deconv, Ifastminib0, Ifastminib0_deconv,\
        #                  Ifast_deconv_hv, Ifastminib0_deconv_hv, Ifast_deconv_hs, Ifastminib0_deconv_hs
        # if boolreconv: return Islow, Islow_conv, Ifast, Ifast_deconv, Ifastminib0, Ifastminib0_deconv, Islow_deconv, Ifast_conv
        # else:
        #     return Islow, Islow_conv, Ifast, Ifast_deconv


def convolution(df, variable1, variable2, tvariable, beta, boolib0):

    size = len(df)
    Islow = [0]*size; Islow_conv = [0]*size; Ifast = [0]*size; Ifastminib0 = [0]*size; Ifast_deconv = [0]*size; Ifastminib0_deconv=[0]*size


    for i in range(size - 1):

        t1 = df.at[i + 1, tvariable]
        t2 = df.at[i, tvariable]

        Xs = np.exp(-(t1 - t2) / tslow)
        Xf = np.exp(-(t1 - t2) / tfast)

        Islow[i] = beta * df.at[i, variable1]
        Islow[i + 1] = beta * df.at[i + 1, variable1]

        Islow_conv[i + 1] = Islow[i + 1] - (Islow[i + 1] - Islow_conv[i]) * Xs

        Ifast[i + 1] = af * (df.at[i + 1, variable2] - Islow_conv[i + 1])
        Ifast[i] = af * (df.at[i, variable2] - Islow_conv[i])

        Ifast_deconv[i + 1] = (Ifast[i + 1] - Ifast[i] * Xf) / (1 - Xf)

        if boolib0 == True:
            Ifastminib0[i] = af * (df.at[i, variable2] - Islow_conv[i] - df.at[i, 'iB0'])
            Ifastminib0[i + 1] = af * (df.at[i + 1, variable2] - Islow_conv[i + 1] - df.at[i + 1, 'iB0'])
            Ifastminib0_deconv[i + 1] = (Ifastminib0[i + 1] - Ifastminib0[i] * Xf) / (1 - Xf)




    if boolib0:
        return Islow, Islow_conv, Ifast, Ifast_deconv, Ifastminib0, Ifastminib0_deconv
    else:
        return Islow, Islow_conv, Ifast, Ifast_deconv

def smooth_and_convolute(df, variable, tvariable, windowlen,  beta, boolib0):

    size = len(df)
    Islow = [0]*size; Islow_conv = [0]*size; Ifast = [0]*size; Ifastminib0 = [0]*size; Ifast_deconv = [0]*size; Ifastminib0_deconv=[0]*size


    df['variable_smoothed'] = df[variable].rolling(window=windowlen, center=True).mean()

    for i in range(size - 2):

        t1 = df.at[i + 1, tvariable]
        t2 = df.at[i, tvariable]

        Xs = np.exp(-(t1 - t2) / tslow)
        Xf = np.exp(-(t1 - t2) / tfast)

        Islow[i] = beta * df.at[i, variable]
        Islow[i + 1] = beta * df.at[i + 1, variable]


        Islow_conv[i + 1] = Islow[i + 1] - (Islow[i + 1] - Islow_conv[i]) * Xs


        Ifast[i + 1] = af * (df.at[i + 1, 'variable_smoothed'] - Islow_conv[i + 1])
        Ifast[i] = af * (df.at[i, 'variable_smoothed'] - Islow_conv[i])

        Ifast_deconv[i + 1] = (Ifast[i + 1] - Ifast[i] * Xf) / (1 - Xf)

        print(i, Ifast_deconv[i+1])

        if boolib0 == True:
            Ifastminib0[i] = af * (df.at[i, 'variable_smoothed'] - Islow_conv[i] - df.at[i, 'iB0'])
            Ifastminib0[i + 1] = af * (df.at[i + 1, 'variable_smoothed'] - Islow_conv[i + 1] - df.at[i + 1, 'iB0'])
            Ifastminib0_deconv[i + 1] = (Ifastminib0[i + 1] - Ifastminib0[i] * Xf) / (1 - Xf)



    return Islow, Islow_conv, Ifast, Ifast_deconv, Ifastminib0, Ifastminib0_deconv
