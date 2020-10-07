import pandas as pd
import numpy as np
import re
import glob

from datetime import datetime

## raw 1 second data
rfiles = glob.glob("/home/poyraden/Analysis/Uccle_Deconvolution/Files/KNMI/All/*.00o")
#vaisala output
vfiles = glob.glob("/home/poyraden/Analysis/Uccle_Deconvolution/Files/KNMI/All/*.00a")
#filled put meta data
fmfiles = glob.glob("/home/poyraden/Analysis/Uccle_Deconvolution/Files/KNMI/All/*.00p")
## corrected profiles
cfiles = glob.glob("/home/poyraden/Analysis/Uccle_Deconvolution/Files/KNMI/All/*.00z")

# 1 time after launch [s]
# 2 geopotential height [m]
# 3 pressure [hPa]
# 4 temperature [C]
# 5 relative humidity w.r.t. liquid water [%]
# 6 pump temperature [C]
# 7 ozone partial pressure [hPa]
# 8 pump voltage [V]
# 9 pump current [mA]
# 10 cell current [uA]
# 11 ozone mixing ratio [ppmv]
# 12 GPS longitude [degrees east]
# 13 GPS latitude [degrees west]
# 14 wind speed [m/s]
# 15 wind direction [degrees from north]
# 16 ozone partial pressure uncertainty [mPa]
# 17 pump frequency [Hz]
# 18 pump frequency anomaly [-]
# 19 GPS altitude [m]
#
cString = "Time Altitude Pair Tair Humidity TPump PO3 PumpV PumpC CellC OMR Lon Lat  WindSp WindDir PO3unc PFreq PFreqAn gpsAltitude"
cStr = cString.split(" ")

rString = "Time Altitude Pair Tair Humidity TPump PO3 PumpV PumpC CellC OMR Lon Lat  WindSp WindDir PO3unc PFreq PFreqAn gpsAltitude"
rStr = cString.split(" ")

vString = "Time Altitude Pair Tair Humidity TPump PO3 OMR x y z t"
vStr = vString.split(" ")

df = pd.read_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/UccleDataRaw.csv")


list_data_c = []
list_data_v = []
list_data_r = []

for cfilename, vfilename, rfilename in zip(cfiles, vfiles, rfiles):
    date_tmp = cfilename.split('.')[0].split('/')[8][0:6]
    # print(date_tmp)

    date = datetime.strptime(date_tmp, '%y%m%d')
    datef = date.strftime('%Y%m%d')
    print(datef, type(datef))

    dft = df[df.Date == int(datef)]

    # dr = pd.read_csv(rfilename, sep = "\s *", engine="python", skiprows=4)
    dv = pd.read_csv(vfilename, sep = "\s *", engine="python", skiprows=2, names = vStr)
    dc = pd.read_csv(cfilename, sep = "\s *", engine="python", skiprows=2,  names=cStr)
    dv['Date'] = datef
    dc['Date'] = datef
    if (datef == '20190715'):
        dv['pf'] = 100 / 30.480
        dv['CF'] = 1.0274
        # dc['pf'] = 100 / 30.480
    if (datef == '20190726'):
        dv['pf'] = 100 / 29.43
        dv['CF'] = 1.0274

        # dc['pf'] = 100 / 29.43
    if (datef == '20190729'):
        dv['pf'] = 100 / 29.93
        dv['CF'] = 1.0274

        # dc['pf'] = 100 / 29.93


    dv['iB0'] = dft.at[dft.first_valid_index(),'iB0']
    dv['iB1'] = dft.at[dft.first_valid_index(),'iB1']
    print(dft.at[dft.first_valid_index(),'iB0'],dft.at[dft.first_valid_index(),'iB1'] )

    dv['TboxK'] = dv['TPump'] + 273
    dv['I_cal'] = dv['PO3'] * dv['pf'] / (dv['TboxK'] * 0.043085)
    dv['I_cal_corr'] = dv['PO3'] * dv['pf'] * dv['CF'] / (dv['TboxK'] * 0.043085)
    dv['I_cal_ib1'] = dv['I_cal'] + dv['iB1']
    dv['I_cal_corr_ib1'] = dv['I_cal_corr'] + dv['iB1']

    print(dv.at[dv.first_valid_index(),'iB0'], dv.at[dv.first_valid_index(),'I_cal'], dv.at[dv.first_valid_index(),'I_cal_ib1'] )


    list_data_c.append(dc)
    list_data_v.append(dv)
    # list_data_r.append(dr)

dfc = pd.concat(list_data_c,ignore_index=True)
dfv = pd.concat(list_data_v,ignore_index=True)
# dfr = pd.concat(list_data_r,ignore_index=True)




dfc.to_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/KNMI_uccle_corrected.csv")
dfv.to_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/KNMI_uccle_vaisala.csv")
# dfr.to_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/KNMI_uccle_raw.csv")

# now do deconvlution to vaisala data set
# dfvc = dfv.copy()











