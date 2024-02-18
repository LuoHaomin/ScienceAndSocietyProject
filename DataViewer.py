import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import seaborn as sb

def get_id(x, y):
    return x*32+y

def readData(uri='../Beijing/T_DRIVE_SMALL/T_DRIVE_SMALL.grid'):
    with open(uri, 'r') as f:
        print(f.readline())
        lastID=-1
        while f.readline()!="":
            strs = f.readline().split(",")
            id = get_id(int(strs[3]),int(strs[4]))
            if lastID==-1 :
                set = {}
                lastID=0
            if(id!=lastID):
                if lastID==0 :
                    df = pd.DataFrame(set)
                    print(set)
                else:
                    df = pd.concat((df,pd.DataFrame(set)),ignore_index=True)
                set = {}
            set[strs[2]] = [float(strs[5]),float(strs[6])]
            lastID=id
        #df.loc[len(df),len(df)+1] = set
        df = pd.concat((df,pd.DataFrame(set)),ignore_index=True)
    f.close()
    return df

def feature(dataframe):
    timestr = dataframe.columns.tolist()
    times = [time.strptime(ts, "%Y-%m-%dT%H:%M:%SZ") for ts in timestr]
    print(times)


    for i in range(0, len(dataframe)):

        # 计算特征：周平均流量，周流量分布，时段流量分布。
        if i % 2 == 0:
            w_in = [0.] * 7
            h_in = [0.] * 6
            total_in = 0.
            for j in range(0, len(timestr)):
                var = dataframe.loc[i, timestr[j]]
                w_in[times[j].tm_wday] += var
                h_in[(times[j].tm_hour // 4)] += var
                total_in += var
        else:
            w_out = [0.] * 7
            h_out = [0.] * 6
            total_out = 0.
            for j in range(0, len(timestr)):
                var = dataframe.loc[i, timestr[j]]
                w_out[times[j].tm_wday] += var
                h_out[(times[j].tm_hour // 4)] += var
                total_out += var
            if i == 1:
                featured = pd.DataFrame({"row": i // 64, "column": (i // 2) % 32,
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
                featured.loc[len(featured)] = {"row": i // 64, "column": (i // 2) % 32,
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

def heat_image(df,str):
    grid = np.zeros([32, 32])
    for i in range(0, 1024):
        grid[31 - df.loc[i, "row"], df.loc[i, "column"]] = df.loc[i, str]
    sb.set()
    sb.heatmap(grid)
    plt.show()

if __name__ == '__main__':
    heat_image(pd.read_csv("../Data/output.csv"),"label")
    # data = pd.read_csv("output.csv")
    # print(data["label"].to_string())
    # data["label"].plot(kind = "hist")
    # plt.show()