import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

    dft[j]['I_sm'] = dft[j]['I'].rolling(window=8).mean()
    dft[j] = dft[j][8:-8]

    size = len(dft[j])

    Islow = [0] * size
    Islow_conv = [0] * size
    Ifast = [0] * size
    Ifast_deconv = [0] * size
    Ifastminib0 = [0] * size
    Ifastminib0_deconv = [0] * size

    Islow_sm = [0] * size
    Islow_conv_sm = [0] * size
    Ifast_sm = [0] * size
    Ifast_deconv_sm = [0] * size
    Ifastminib0_sm = [0] * size
    Ifastminib0_deconv_sm = [0] * size

    for i in range(8, size - 8):
        t1 = dft[j].at[i + 1, 'Time']
        t2 = dft[j].at[i, 'Time']
        Xs = np.exp(-(t1 - t2) / tslow)
        Xf = np.exp(-(t1 - t2) / tfast)

        Islow[i] = beta * dft[j].at[i, 'I']
        Islow_conv[i + 1] = Islow[i] - (Islow[i] - Islow_conv[i]) * Xs
        Ifast[i + 1] = af * (dft[j].at[i + 1, 'I'] - Islow_conv[i + 1])
        Ifastminib0[i + 1] = af * (dft[j].at[i + 1, 'I'] - Islow_conv[i + 1] - dft[j].at[i + 1, 'iB0'])
        Ifast_deconv[i + 1] = (Ifast[i + 1] - Ifast[i] * Xf) / (1 - Xf)
        Ifastminib0_deconv[i + 1] = (Ifastminib0[i + 1] - Ifastminib0[i] * Xf) / (1 - Xf)

        Islow_sm[i] = beta * dft[j].at[i, 'I_sm']
        Islow_conv_sm[i + 1] = Islow_sm[i] - (Islow_sm[i] - Islow_conv_sm[i]) * Xs
        Ifast_sm[i + 1] = af * (dft[j].at[i + 1, 'I_sm'] - Islow_conv_sm[i + 1])
        Ifastminib0_sm[i + 1] = af * (dft[j].at[i + 1, 'I_sm'] - Islow_conv_sm[i + 1] - dft[j].at[i + 1, 'iB0'])
        Ifast_deconv_sm[i + 1] = (Ifast_sm[i + 1] - Ifast_sm[i] * Xf) / (1 - Xf)
        Ifastminib0_deconv_sm[i + 1] = (Ifastminib0_sm[i + 1] - Ifastminib0_sm[i] * Xf) / (1 - Xf)

    dft[j]['I_slow'] = Islow
    dft[j]['I_slow_conv'] = Islow_conv
    dft[j]['I_fast'] = Ifast
    dft[j]['Ifast_minib0'] = Ifastminib0
    dft[j]['Ifast_deconv'] = Ifast_deconv
    dft[j]['Ifast_minib0_deconv'] = Ifastminib0_deconv

    dft[j]['I_slow_sm'] = Islow_sm
    dft[j]['I_slow_conv_sm'] = Islow_conv_sm
    dft[j]['I_fast_sm'] = Ifast_sm
    dft[j]['Ifast_minib0_sm'] = Ifastminib0_sm
    dft[j]['Ifast_deconv_sm'] = Ifast_deconv_sm
    dft[j]['Ifast_minib0_deconv_sm'] = Ifastminib0_deconv_sm

    list_data.append(dft[j])

df_dc = pd.concat(list_data, ignore_index=True)

df_dc.to_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/Deconvoluted_UccleDataRaw.csv")