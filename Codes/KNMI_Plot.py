import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import gridspec

# df = pd.read_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/Deconvoluted_UccleDataRaw_3secs.csv", low_memory=False)

dfc = pd.read_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/KNMI_uccle_corrected.csv", low_memory=False)
dfv = pd.read_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/KNMI_uccle_vaisala.csv",  low_memory=False)

print('dfc', list(dfc))
print('dfv', list(dfv))

dfnd = dfc.drop_duplicates('Date')
datelist = np.array(dfnd['Date'])

for j in range(len(datelist)):

    dc = dfc[dfc.Date == datelist[j]]
    dv = dfv[dfv.Date == datelist[j]]

    maxh = dc.Altitude.max()
    index = dc[dc["Altitude"] == maxh].index[0]

    descentlist = dc[dc.index > index].index.tolist()
    ascentlist = dc[dc.index < index].index.tolist()

    dfa = dc.drop(descentlist)
    dfd = dc.drop(ascentlist)

    print(len(dc), len(dfa), len(dfd))


    maxhv = dv.Altitude.max()
    print('maxhv', maxhv)
    indexv = dv[dv["Altitude"] == maxhv].index[0]

    descentlistv = dv[dv.index > indexv].index.tolist()
    ascentlistv = dv[dv.index < indexv].index.tolist()

    dfva = dv.drop(descentlistv)
    dfvd = dv.drop(ascentlistv)



    maintitle = str(int(datelist[j]))
    fig, ax0 = plt.subplots()

    plt.xlabel(r'PO3')
    # plt.xlabel(r'Current($\mu$A)')

    plt.ylabel('Altitude')
    # plt.ylabel('Time')

    # ax0.set_yscale('log')
    # plt.xlim(0, 5)
    # plt.ylim(1000, 5)
    plt.title(maintitle)
    #
    # plt.plot(dfa.PO3, dfa.Altitude/1000, label='Ascent corrected ')
    # plt.plot(dfd.PO3, dfd.Altitude/1000, label='Descent corrected ')

    plt.plot(dfva.PO3, dfva.Altitude/1000, label='Ascent Vaisala  ')
    plt.plot(dfvd.PO3, dfvd.Altitude/1000, label='Descent Vaisala  ')

    # plt.plot(dfa.CellC, dfa.Altitude/1000, label='Ascent corrected ')
    # plt.plot(dfd.CellC, dfd.Altitude/1000, label='Descent corrected ')
    # plt.plot(dfva.I_cal, dfva.Altitude/1000, label='Ascent Vaisala ')
    # plt.plot(dfvd.I_cal, dfvd.Altitude/1000, label='Descent Vaisala ')

    # plt.plot(dfd.Time, dfd.I, label='Descent ')
    # plt.plot(dfa.Time, dfa.I, label='Ascent ')
    ax0.legend(loc='best', frameon=False, fontsize='large')

    plt.savefig('/home/poyraden/Analysis/Uccle_Deconvolution/Plots/knmi/Vaisala_pre_' + maintitle + '.eps')
    plt.savefig('/home/poyraden/Analysis/Uccle_Deconvolution/Plots/knmi/Vaisala_pre_' + maintitle + '.png')

    plt.show()
