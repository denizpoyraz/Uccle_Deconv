import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

from Convolution_Functions import convolution, convolution_test, smooth_and_convolute

tslow = 25 * 60
tfast = 20

df = pd.read_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/UccleDataRaw.csv", low_memory=False)

df = df[(df.Date > 20190601) & (df.Date < 20190901)]



dfd = df.drop_duplicates('Date')
datelist = np.array(dfd['Date'])

beta = 0.155 * 0.1
af = 1

dft = {}
list_data = []

for j in range(len(datelist)):

    dft[j] = df[df.Date == datelist[j]]
    dft[j] = dft[j].reset_index()

    dft[j]['TS'] = pd.to_datetime(dft[j].Time, unit='s')

    dft[j] = dft[j].resample('3S', on='TS').mean().interpolate()
    dft[j] = dft[j].reset_index()

    dft[j]['nTime'] = (dft[j]['TS'] - datetime.datetime(1970, 1, 1)).dt.total_seconds()

    dft[j]['I_sm'] = dft[j]['I'].rolling(window=8).mean()
    dft[j]['I_sm20'] = dft[j]['I'].rolling(window=20).mean()
    dft[j]['I_sm40'] = dft[j]['I'].rolling(window=40).mean()

    # dft[j] = dft[j][40:-40]

    Islow, Islow_conv, Ifast, Ifast_deconv, Ifastminib0, Ifastminib0_deconv = convolution(dft[j], 'I', 'I', 'nTime', beta, 1)

    dft[j]['I_slow'] = Islow
    dft[j]['I_slow_conv'] = Islow_conv
    dft[j]['I_fast'] = Ifast
    dft[j]['Ifast_minib0'] = Ifastminib0
    dft[j]['Ifast_deconv'] = Ifast_deconv
    dft[j]['Ifast_minib0_deconv'] = Ifastminib0_deconv



    list_data.append(dft[j])

df_dc = pd.concat(list_data, ignore_index=True)

df_dc.to_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/Deconvoluted_UccleDataRaw_3secs.csv")
# df_dc.to_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/Deconvoluted_UccleDataRaw.csv")


#############################################################################################################################


# size = len(dft[j])
#
#     Islow = [0] * size
#     Islow_conv = [0] * size
#     Ifast = [0] * size
#     Ifast_deconv = [0] * size
#     Ifastminib0 = [0] * size
#     Ifastminib0_deconv = [0] * size

     # Islow_sm = [0] * size
    # Islow_conv_sm = [0] * size
    # Ifast_sm = [0] * size
    # Ifast_deconv_sm = [0] * size
    # Ifastminib0_sm = [0] * size
    # Ifastminib0_deconv_sm = [0] * size
    #
    # Islow_sm20 = [0] * size
    # Islow_conv_sm20 = [0] * size
    # Ifast_sm20 = [0] * size
    # Ifast_deconv_sm20 = [0] * size
    # Ifastminib0_sm20 = [0] * size
    # Ifastminib0_deconv_sm20 = [0] * size
    #
    # Islow_sm40 = [0] * size
    # Islow_conv_sm40 = [0] * size
    # Ifast_sm40 = [0] * size
    # Ifast_deconv_sm40 = [0] * size
    # Ifastminib0_sm40 = [0] * size
    # Ifastminib0_deconv_sm40 = [0] * size

    # ind = 1
    # for i in range(0, size - ind, ind):
    #     t1 = dft[j].at[i + ind, 'Time']
    #     t2 = dft[j].at[i, 'Time']
    #
    #     # print(i, t1-t2)
    #     Xs = np.exp(-(t1 - t2) / tslow)
    #     Xf = np.exp(-(t1 - t2) / tfast)
    #
    #     Islow[i] = beta * dft[j].at[i, 'I']
    #     Islow_conv[i + ind] = Islow[i] - (Islow[i] - Islow_conv[i]) * Xs
    #     Ifast[i + ind] = af * (dft[j].at[i + ind, 'I'] - Islow_conv[i + ind])
    #     Ifastminib0[i + ind] = af * (dft[j].at[i + ind, 'I'] - Islow_conv[i + ind] - dft[j].at[i + ind, 'iB0'])
    #     Ifast_deconv[i + ind] = (Ifast[i + ind] - Ifast[i] * Xf) / (1 - Xf)
    #     Ifastminib0_deconv[i + ind] = (Ifastminib0[i + ind] - Ifastminib0[i] * Xf) / (1 - Xf)

# Islow_sm[i] = beta * dft[j].at[i, 'I_sm']
# Islow_conv_sm[i + 1] = Islow_sm[i] - (Islow_sm[i] - Islow_conv_sm[i]) * Xs
# Ifast_sm[i + 1] = af * (dft[j].at[i + 1, 'I_sm'] - Islow_conv_sm[i + 1])
# Ifastminib0_sm[i + 1] = af * (dft[j].at[i + 1, 'I_sm'] - Islow_conv_sm[i + 1] - dft[j].at[i + 1, 'iB0'])
# Ifast_deconv_sm[i + 1] = (Ifast_sm[i + 1] - Ifast_sm[i] * Xf) / (1 - Xf)
# Ifastminib0_deconv_sm[i + 1] = (Ifastminib0_sm[i + 1] - Ifastminib0_sm[i] * Xf) / (1 - Xf)
#
# Islow_sm20[i] = beta * dft[j].at[i, 'I_sm20']
# Islow_conv_sm20[i + 1] = Islow_sm20[i] - (Islow_sm20[i] - Islow_conv_sm20[i]) * Xs
# Ifast_sm20[i + 1] = af * (dft[j].at[i + 1, 'I_sm20'] - Islow_conv_sm20[i + 1])
# Ifastminib0_sm20[i + 1] = af * (dft[j].at[i + 1, 'I_sm20'] - Islow_conv_sm20[i + 1] - dft[j].at[i + 1, 'iB0'])
# Ifast_deconv_sm20[i + 1] = (Ifast_sm20[i + 1] - Ifast_sm20[i] * Xf) / (1 - Xf)
# Ifastminib0_deconv_sm20[i + 1] = (Ifastminib0_sm20[i + 1] - Ifastminib0_sm20[i] * Xf) / (1 - Xf)
#
# Islow_sm40[i] = beta * dft[j].at[i, 'I_sm40']
# Islow_conv_sm40[i + 1] = Islow_sm40[i] - (Islow_sm40[i] - Islow_conv_sm40[i]) * Xs
# Ifast_sm40[i + 1] = af * (dft[j].at[i + 1, 'I_sm40'] - Islow_conv_sm40[i + 1])
# Ifastminib0_sm40[i + 1] = af * (dft[j].at[i + 1, 'I_sm40'] - Islow_conv_sm40[i + 1] - dft[j].at[i + 1, 'iB0'])
# Ifast_deconv_sm40[i + 1] = (Ifast_sm40[i + 1] - Ifast_sm40[i] * Xf) / (1 - Xf)
# Ifastminib0_deconv_sm40[i + 1] = (Ifastminib0_sm40[i + 1] - Ifastminib0_sm40[i] * Xf) / (1 - Xf)


# dft[j]['I_slow_sm'] = Islow_sm
# dft[j]['I_slow_conv_sm'] = Islow_conv_sm
# dft[j]['I_fast_sm'] = Ifast_sm
# dft[j]['Ifast_minib0_sm'] = Ifastminib0_sm
# dft[j]['Ifast_deconv_sm'] = Ifast_deconv_sm
# dft[j]['Ifast_minib0_deconv_sm'] = Ifastminib0_deconv_sm
#
# dft[j]['I_slow_sm40'] = Islow_sm40
# dft[j]['I_slow_conv_sm40'] = Islow_conv_sm40
# dft[j]['I_fast_sm40'] = Ifast_sm40
# dft[j]['Ifast_minib0_sm40'] = Ifastminib0_sm40
# dft[j]['Ifast_deconv_sm40'] = Ifast_deconv_sm40
# dft[j]['Ifast_minib0_deconv_sm40'] = Ifastminib0_deconv_sm40
#
# dft[j]['I_slow_sm20'] = Islow_sm20
# dft[j]['I_slow_conv_sm20'] = Islow_conv_sm20
# dft[j]['I_fast_sm20'] = Ifast_sm20
# dft[j]['Ifast_minib0_sm20'] = Ifastminib0_sm20
# dft[j]['Ifast_deconv_sm20'] = Ifast_deconv_sm20
# dft[j]['Ifast_minib0_deconv_sm20'] = Ifastminib0_deconv_sm20