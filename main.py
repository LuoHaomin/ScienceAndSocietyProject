#-- coding UTF-8--
import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import seaborn as sb



if __name__ == '__main__':
    df = pd.read_csv("../Data/T_DRIVE_SMALL_Feature.csv")
    print(df.columns.tolist())
    scaler = StandardScaler()
    scaler.fit(df[['row', 'column', 'total_in', 'w_in0', 'w_in1', 'w_in2', 'w_in3', 'w_in4', 'w_in5', 'w_in6', 'h_in0', 'h_in1', 'h_in2', 'h_in3', 'h_in4', 'h_in5',
                   'total_out', 'w_out0', 'w_out1', 'w_out2', 'w_out3', 'w_out4', 'w_out5', 'w_out6', 'h_out0', 'h_out1', 'h_out2', 'h_out3', 'h_out4', 'h_out5']])
    data = scaler.transform(df[['row', 'column', 'total_in', 'w_in0', 'w_in1', 'w_in2', 'w_in3', 'w_in4', 'w_in5', 'w_in6', 'h_in0', 'h_in1', 'h_in2', 'h_in3', 'h_in4', 'h_in5',
                                'total_out', 'w_out0', 'w_out1', 'w_out2', 'w_out3', 'w_out4', 'w_out5', 'w_out6', 'h_out0', 'h_out1', 'h_out2', 'h_out3', 'h_out4', 'h_out5']])

    for i in range(0,1024):
        data[i,0]*=0.3
        data[i,1]*=0.3

    n=7
    km = KMeans(n_clusters=n, random_state= 0).fit(data)
    label = km.labels_
    outPut = pd.concat((df,pd.DataFrame(label,columns=["label"])),
                       axis=1)
    print(outPut[["label"]])
    outPut.to_csv("../Data/output.csv",index=False)