import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("/home/poyraden/Analysis/Uccle_Deconvolution/Proccessed/UccleDataRaw.csv", low_memory=False)

dfd = df.drop_duplicates('Date')
datelist = np.array(dfd['Date'])

dft = {}

for j in range(len(datelist)):





