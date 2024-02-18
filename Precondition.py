import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


def ReadTrack(uri='../Beijing/T_Drive/011'):
    files = os.listdir(uri)
    for file in files:
        with open(uri+"/"+file, 'r') as f:
            tag = False
            while f.readline()!="":
                strs = f.readline().split(",")
                if strs[0] != "":
                    set = {"id":[int(strs[0])],"time":[strs[1]],"Lo":[float(strs[2])],"La":[float(strs[3])]}
                    if not tag:
                        df = pd.DataFrame(set)
                        tag=True
                    else:
                        df = pd.concat((df, pd.DataFrame(set)), ignore_index=True)
                # print(strs)

        f.close()
    return df

if __name__ == '__main__':
    # df1 =ReadTrack('../Beijing/T_Drive/011')
    # df1.to_csv("../Beijing/T_Drive/Data/011.csv")
    # df2 =ReadTrack('../Beijing/T_Drive/012')
    # df2.to_csv("../Beijing/T_Drive/Data/012.csv")
    # df3 =ReadTrack('../Beijing/T_Drive/013')
    # df3.to_csv("../Beijing/T_Drive/Data/013.csv")
    # df4 =ReadTrack('../Beijing/T_Drive/014')
    # df4.to_csv("../Beijing/T_Drive/Data/014.csv")


    df = pd.concat((df1,df2,df3,df4), ignore_index=True)
    df.plot.scatter(x="Lo",y="La")
    plt.show()