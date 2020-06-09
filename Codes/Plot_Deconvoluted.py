import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


df = pd.read_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/Deconvoluted_UccleDataRaw.csv", low_memory=False)

dfs = df[(df.Date > 20190601) & (df.Date < 20190901)]
dfnd = dfs.drop_duplicates('Date')
datelist = np.array(dfnd['Date'])
monthlist = np.array(dfnd['Month'])
daylist = np.array(dfnd['Day'])
yearlist = np.array(dfnd['Year'])



dft = {}

for j in range(len(datelist)):

    dft[j] = df[df.Date == datelist[j]]
    dft[j] = dft[j][(dft[j].I > 0)]
    dft[j] = dft[j][(dft[j].I_sm > 0)]
    dft[j] = dft[j][(dft[j].I < 10)]
    dft[j] = dft[j][(dft[j].I_sm < 10)]

    maxh = dft[j].Height.max()
    index = dft[j][dft[j]["Height"] == maxh].index[0]

    descentlist = dft[j][dft[j].index > index].index.tolist()
    ascentlist = dft[j][dft[j].index < index].index.tolist()

    dfa = dft[j].drop(descentlist)
    dfd = dft[j].drop(ascentlist)

    maintitle = str(daylist[j])+ '/' + str(monthlist[j]) + '/' + str(yearlist[j])

    fig, ax = plt.subplots()
    plt.title(maintitle)
    plt.xlabel(r'Current($\mu$A)')
    plt.ylabel('Pressure')
    ax.set_yscale('log')
    plt.xlim(0, 5)
    plt.ylim(980, 5)

    plt.plot(dfa.I, dfa.Pressure, label = 'Ascent', linewidth = 3)
    plt.plot(dfa.Ifast_minib0_deconv.rolling(window=8).mean(), dfa.Pressure, label='Ascent corrected')
    # plt.plot(dfa.Ifast_minib0_deconv_sm, dfa.Pressure.rolling(window=8).mean(), label='Ascent smoothed corrected')


    plt.plot(dfd.I, dfd.Pressure, label = 'Descent', linewidth = 3)
    plt.plot(dfd.Ifast_minib0_deconv.rolling(window=8).mean(), dfd.Pressure, label='Descent corrected')

    ax.legend(loc='best', frameon=False, fontsize='x-small')

    plt.show()

