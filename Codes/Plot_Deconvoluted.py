import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import gridspec


# df = pd.read_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/Deconvoluted_UccleDataRaw_original.csv", low_memory=False)
df = pd.read_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/Deconvoluted_UccleDataRaw_3secs.csv", low_memory=False)


df['km'] = round(df['Height'],2)/1000

dfs = df[(df.Date > 20190701) & (df.Date < 20190901)]
dfnd = dfs.drop_duplicates('Date')
datelist = np.array(dfnd['Date'])
monthlist = np.array(dfnd['Month'])
daylist = np.array(dfnd['Day'])
yearlist = np.array(dfnd['Year'])

print(list(df))

dft = {}

for j in range(len(datelist)):

    dft[j] = dfs[dfs.Date == datelist[j]]
    # dft[j] = dft[j].reset_index()
    dft[j] = dft[j][(dft[j].I > 0)]
    dft[j] = dft[j][(dft[j].I_sm > 0)]
    dft[j] = dft[j][(dft[j].I < 20)]
    dft[j] = dft[j][(dft[j].I_sm < 20)]

    maxh = dft[j].Height.max()
    index = dft[j][dft[j]["Height"] == maxh].index[0]

    descentlist = dft[j][dft[j].index > index].index.tolist()
    ascentlist = dft[j][dft[j].index < index].index.tolist()

    dfa = dft[j].drop(descentlist)
    dfd = dft[j].drop(ascentlist)

    # print(len(dfa), len(dfd))

    maxa = dfa.Time.max()
    mind = dfd.Time.min()
    maxd = dfd.Time.max()
    dif = maxd - mind



    # print(sd, dfd.fTime)
    # dftitle = dft[j].reset_index()

    print(daylist[j], monthlist[j], yearlist[j])
    # print(str(dftitle.at[0,'Date']))
    maintitle = str(int(daylist[j]))+ '/' + str(int(monthlist[j])) + '/' + str(int(yearlist[j]))
    # ptitle = str((int(dftitle.at[0,'Date'])))
    ptitle = str(int(daylist[j])) + str(int(monthlist[j])) +  str(int(yearlist[j]))

    print(maintitle, ptitle)
    # , ptitle)

    # fig = plt.figure()
    # # set height ratios for sublots
    # gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])
    # ax0 = plt.subplot(gs[0])

    fig, ax0 = plt.subplots()

    plt.xlabel(r'Current($\mu$A)')
    # plt.ylabel('Altitude')
    plt.ylabel('Pressure')

    # ax0.set_yscale('log')
    # plt.xlim(0, 5)
    # plt.ylim(1000, 5)
    plt.title(maintitle)

    # plt.plot(dfa.I.rolling(window=1, center=True).mean(), dfa.Height, label = 'Ascent', linewidth = 3 )
    # plt.plot(dfa.Ifast_minib0_deconv.rolling(window=3, center=True).mean(), dfa.Height, label='Ascent (Ifast - iB0) corrected .')
    # # plt.plot(dfa.I_slow_conv, dfa.Pressure, label='Ascent I slow conv ')
    # # plt.plot(dfa.iB0, dfa.Pressure, label='iB0')
    # # plt.plot(dfa.iB1, dfa.Pressure, label='iB1')
    #

    # dfd['vt'] = dfd.AscRate * dfd.Time
    #
    # plt.plot(dfd.I, dfd.Height, label = 'Descent', linewidth = 3)

    # plt.plot(dfd.Ifast_minib0_deconv.rolling(window=3, center=True).mean(), dfd.Height, label='Descent (Ifast - iB0)  corrected')
    # plt.plot(dfd.I_slow_conv, dfd.Pressure, label='Descent I slow conv ')
    # plt.plot(dfd.iB0, dfd.Pressure, label='iB0')
    # plt.plot(dfd.iB1, dfd.Pressure, label='iB1')
    # plt.plot(dfd.Ifast_deconv.rolling(window=9, center=True).mean(), dfd.Pressure, label='Descent (Ifast)  corrected')
    # plt.plot(dfd.I_slow_conv.rolling(window=1, center=True).mean(), dfd.Pressure, label='Descent I slow conv ')

    plt.plot(dfd.Time, dfd.I, label='Descent ')
    plt.plot(dfa.Time, dfa.I, label='Ascent ')

    plt.plot(dfd.Time, dfd.I, label='Descent ')
    plt.plot(dfa.Time, dfa.I, label='Ascent ')

    # plt.plot(dfa.AscRate, dfa.Height, label='Asscent rate')
    #
    # plt.plot(dfd.Windv, dfd.Height, label='Descent Windv')
    # plt.plot(dfa.Windv, dfa.Height, label='Asscent Windv')







    ax0.legend(loc='best', frameon=False, fontsize='large')


    dfa['rdif'] = 100 *(dfa.I - dfa.Ifast_minib0_deconv.rolling(window=10, center=True).mean())/ dfa.I

    # ax1 = plt.subplot(gs[1])
    # # plt.plot(dfa.I, dfa.km, label = 'Ascent', linewidth = 3 )
    # ax1.axvline(x=0, color='grey', linestyle='--')
    #
    #
    # plt.plot(dfa.rdif, dfa.Time, label = 'RDif', linewidth = 3 )


    # plt.plot(dfa.I_sm20, dfa.Height, label = 'Ascent', linewidth = 3 )
    # plt.plot(dfa.Ifast_minib0_deconv_sm20, dfa.Height, label='Ascent corrected')
    # plt.plot(dfd.I_sm20, dfd.Height, label = 'Descent', linewidth = 3)
    # plt.plot(dfd.Ifast_minib0_deconv_sm20, dfd.Height, label='Descent corrected')

    # plt.plot(dfa.I_sm20, dfa.Time, label = 'Ascent I', linewidth = 1.5)
    # plt.plot(dfa.I_fast_sm20, dfa.Time, label = 'Ascent Ifast', linewidth = 1)
    # plt.plot(dfa.Ifast_minib0_sm20, dfa.Time, label = 'Ascent Ifast - iB0', linewidth = 1)
    # plt.plot(dfa.I_slow_sm20, dfa.Time, label = 'Ascent Islow', linewidth = 1)
    # plt.plot(dfa.Ifast_minib0_deconv_sm20, dfa.Time, label='Ascent corrected')
    #
    # plt.plot(dfd.I, dfd.Height, label='Descent I', linewidth = 1)
    # plt.plot(dfd.I_fast_sm20, dfd.Height, label='Descent Ifast', linewidth = 1)
    # plt.plot(dfd.Ifast_minib0_sm20, dfd.Height, label='Descent Ifast - iB0', linewidth = 1)
    # plt.plot(dfd.I_slow_conv_sm20, dfd.Height, label='Descent Islow', linewidth = 1)
    pre = '3seconds_sm9_Data_AD_'
    # plt.savefig('/home/poyraden/Analysis/Uccle_Deconvolution/Plots/PerDay/' + pre + ptitle + '.eps')
    # plt.savefig('/home/poyraden/Analysis/Uccle_Deconvolution/Plots/PerDay/' + pre + ptitle + '.png')


    plt.show()

