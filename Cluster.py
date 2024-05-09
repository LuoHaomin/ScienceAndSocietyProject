#-- coding UTF-8--
import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import seaborn as sb
import time

def Feature(filename="Gtaxi_18.csv"):
    df = pd.read_csv(filename)
    describe=df.describe()
    maxID = describe.loc["max","ID"]
    #print(maxID)
    for i  in range(1,int(maxID)+1):
        w_in = [0.] * 7
        h_in = [0.] * 6
        total_in = 1.
        total_out = 1.
        w_out = [0.] * 7
        h_out = [0.] * 6

        pergrid = df.loc[df["ID"] == i, :]
        for index, row in pergrid.iterrows():
            # print(row)
            timestr = row["time"]
            times = time.strptime(timestr, "%Y-%m-%d %H:%M:%S")
            w_in[times.tm_wday] += row["inflow"]
            h_in[(times.tm_hour // 4)] += row["inflow"]
            total_in += row["inflow"]

            w_out[times.tm_wday] += row["outflow"]
            h_out[(times.tm_hour // 4)] += row["outflow"]
            total_out += row["outflow"]
        if i == 1:
            featured = pd.DataFrame({"ID":i,
                                     "total_in": total_in, "w_in0": w_in[0] / total_in, "w_in1": w_in[1] / total_in,
                                     "w_in2": w_in[2] / total_in, "w_in3": w_in[3] / total_in,
                                     "w_in4": w_in[4] / total_in, "w_in5": w_in[5] / total_in,
                                     "w_in6": w_in[6] / total_in
                                        , "h_in0": h_in[0] / total_in, "h_in1": h_in[1] / total_in,
                                     "h_in2": h_in[2] / total_in, "h_in3": h_in[3] / total_in,
                                     "h_in4": h_in[4] / total_in, "h_in5": h_in[5] / total_in,
                                     "total_out": total_out, "w_out0": w_out[0] / total_out,
                                     "w_out1": w_out[1] / total_out, "w_out2": w_out[2] / total_out,
                                     "w_out3": w_out[3] / total_out, "w_out4": w_out[4] / total_out,
                                     "w_out5": w_out[5] / total_out, "w_out6": w_out[6] / total_out
                                        , "h_out0": h_out[0] / total_out, "h_out1": h_out[1] / total_out,
                                     "h_out2": h_out[2] / total_out, "h_out3": h_out[3] / total_out,
                                     "h_out4": h_out[4] / total_out, "h_out5": h_out[5] / total_out}, index=[0])
        else:
            featured.loc[len(featured)] = {"ID":i,
                                           "total_in": total_in, "w_in0": w_in[0] / total_in,
                                           "w_in1": w_in[1] / total_in, "w_in2": w_in[2] / total_in,
                                           "w_in3": w_in[3] / total_in, "w_in4": w_in[4] / total_in,
                                           "w_in5": w_in[5] / total_in, "w_in6": w_in[6] / total_in
                , "h_in0": h_in[0] / total_in, "h_in1": h_in[1] / total_in, "h_in2": h_in[2] / total_in,
                                           "h_in3": h_in[3] / total_in, "h_in4": h_in[4] / total_in,
                                           "h_in5": h_in[5] / total_in,
                                           "total_out": total_out, "w_out0": w_out[0] / total_out,
                                           "w_out1": w_out[1] / total_out, "w_out2": w_out[2] / total_out,
                                           "w_out3": w_out[3] / total_out, "w_out4": w_out[4] / total_out,
                                           "w_out5": w_out[5] / total_out, "w_out6": w_out[6] / total_out
                , "h_out0": h_out[0] / total_out, "h_out1": h_out[1] / total_out, "h_out2": h_out[2] / total_out,
                                           "h_out3": h_out[3] / total_out, "h_out4": h_out[4] / total_out,
                                           "h_out5": h_out[5] / total_out}
    return featured




def KMeansCluster(name = "../NYC/Featured_16.csv",output ="../NYC/output.csv"):
    df = pd.read_csv(name)
    print(df.columns.tolist())
    scaler = StandardScaler()
    scaler.fit(df[["total_in", 'w_in0', 'w_in1', 'w_in2', 'w_in3', 'w_in4', 'w_in5', 'w_in6', 'h_in0',
                   'h_in1', 'h_in2', 'h_in3', 'h_in4', 'h_in5',
                   'total_out', 'w_out0', 'w_out1', 'w_out2', 'w_out3', 'w_out4', 'w_out5', 'w_out6', 'h_out0',
                   'h_out1', 'h_out2', 'h_out3', 'h_out4', 'h_out5']])
    data = scaler.transform(df[["total_in", 'w_in0', 'w_in1', 'w_in2', 'w_in3', 'w_in4', 'w_in5',
                                'w_in6', 'h_in0', 'h_in1', 'h_in2', 'h_in3', 'h_in4', 'h_in5',
                                'total_out', 'w_out0', 'w_out1', 'w_out2', 'w_out3', 'w_out4', 'w_out5', 'w_out6',
                                'h_out0', 'h_out1', 'h_out2', 'h_out3', 'h_out4', 'h_out5']])



    n = 8
    km = KMeans(n_clusters=n, random_state=0).fit(data)
    label = km.labels_
    outPut = pd.concat((df, pd.DataFrame(label, columns=["label"])),
                       axis=1)
    print(outPut[["label"]])
    outPut.to_csv(output, index=False)



if __name__ == '__main__':
    Feature("YGtaxi_18_half (1).csv").to_csv("YGtaxi_18_half_feature.csv",index=False)
    KMeansCluster("YGtaxi_18_half_feature.csv","../NYC/YG_half_ans.csv")