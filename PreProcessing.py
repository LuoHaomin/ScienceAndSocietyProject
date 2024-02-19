import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

TAXI_NUM = 10357
LAT_MIN = 39.83
LAT_MAX = 40.12
LON_MIN = 116.25
LON_MAX = 116.64
MIN_TIME = '2008-02-02 00:00:00'
MAX_TIME = '2008-02-09 00:00:00'
old_time_format = '%Y-%m-%d %H:%M:%S'
new_time_format = '%Y-%m-%d %H:%M'
MIN_TIMESTAMP = float(
    datetime.timestamp(
        pd.to_datetime(MIN_TIME, utc=True, format=old_time_format)))
MAX_TIMESTAMP = float(
    datetime.timestamp(
        pd.to_datetime(MAX_TIME, utc=True, format=old_time_format)))

# 数据读取
def ReadTrack(uri='./input/bjtaxi'):
    all_data = []
    files = os.listdir(uri)
    for file in files:
        with open(os.path.join(uri, file), 'r') as f:
            for line in f:
                if line.strip():
                    data = line.strip().split(",")
                    all_data.append({
                        'id': int(data[0]),
                        'time': data[1],
                        'lo': float(data[2]),
                        'la': float(data[3])
                    })

    return pd.DataFrame(all_data)


# 判断id
def judge_id(value, dividing_points):
    min_v = dividing_points[0]
    interval = dividing_points[1] - dividing_points[0]
    idx = int((value - min_v) / interval)
    max_id = len(dividing_points) - 2
    return min(max_id, idx)

# 划分网格
def partition_to_grid(data, row_num, col_num, interval):
    """
    :param data: ['id', 'time', 'lo', 'la']
    :param row_num: # of rows
    :param col_num: # of columns
    :return data: ['id','time','row_id','column_id']
    """
    # 以纬度划分行
    lat_diff = LAT_MAX - LAT_MIN
    lat_dividing_points = \
        [round(LAT_MIN + lat_diff / row_num * i, 3)
         for i in range(row_num + 1)]
    data['row_id'] = data.apply(
        lambda x: judge_id(x['la'], lat_dividing_points),
        axis=1
    )

    # 以经度划分列
    lon_diff = LON_MAX - LON_MIN
    lon_dividing_points = \
        [round(LON_MIN + lon_diff / col_num * i, 3)
         for i in range(col_num + 1)]
    data['column_id'] = data.apply(
        lambda x: judge_id(x['lo'], lon_dividing_points),
        axis=1
    )

    return data[
        ['id','time','row_id','column_id']
    ]

def convert_time(data, interval):
    time_dividing_point = \
    list(np.arange(MIN_TIMESTAMP, MAX_TIMESTAMP, interval))

    data['timestamp'] = data.apply(
        lambda x: float(datetime.timestamp(
            pd.to_datetime(x['time'], utc=True, format=old_time_format)
        )),
        axis=1
    )

    data['time_id'] = data.apply(
        lambda x: judge_id(x['timestamp'], time_dividing_point),
        axis=1
    )

    return data

def add_previous_rc_id(tra):
    tra = tra.sort_values(by='time')
    tra['prev_row_id'] = tra['row_id'].shift(1)
    tra['prev_column_id']= tra['column_id'].shift(1)
    return tra[1:]

def timestamp2str(timestamp):
    return pd.to_datetime(timestamp, unit='s').strftime(new_time_format)

def gen_flow_data(trajectory, time_dividing_point):
    trajectory = trajectory[
        (trajectory.prev_row_id != trajectory.row_id) |
        (trajectory.prev_column_id != trajectory.column_id)]
    tra_groups = trajectory.groupby(by='time_id')
    for tra_group in tra_groups:
        tra_group = tra_group[1]
        # print(tra_group)
        t = time_dividing_point[tra_group.iloc[0].loc['time_id']]
        flow_in = tra_group.groupby(
            by=[
                'row_id',
                'column_id']
        )[['id']].count().sort_index()
        flow_in.columns = ['inflow']
        flow_out = tra_group.groupby(
            by=[
                'prev_row_id',
                'prev_column_id']
        )[['id']].count().sort_index()
        flow_out.index.names = ['row_id', 'column_id']
        flow_out.columns = ['outflow']
        flow = flow_in.join(flow_out, how='outer', on=['row_id', 'column_id'])
        flow = flow.reset_index()
        flow['time'] = timestamp2str(t)
        yield flow

def fill_empty_flow(flow_data, time_dividing_point, row_num, col_num):
    # 主要通过生成一个全数据的data frame 与flow_data合并实现
    row_ids = list(range(0, row_num))
    col_ids = list(range(0, col_num))
    time_ids = list(map(timestamp2str, time_dividing_point))

    ids = [(x, y, z) for x in row_ids for y in col_ids for z in time_ids]
    flow_keep = pd.DataFrame(ids, columns=['row_id', 'column_id', 'time'])
    flow_keep = pd.merge(flow_keep, flow_data, how='outer')

    flow_keep = flow_keep.fillna(value={'inflow': 0, 'outflow': 0})
    return flow_keep

def calculate_flow(trajectory,row_num,col_num) :
    trajectory = trajectory.groupby(by='id')

    trajectory = pd.concat(
        map(lambda x: add_previous_rc_id(x[1]), trajectory)
    )
    trajectory['prev_row_id'] = \
        trajectory['prev_row_id'].astype("int64")
    trajectory['prev_column_id'] = \
        trajectory['prev_column_id'].astype("int64")

    # 只保留发生区域变化的time
    trajectory = trajectory[
        ~((trajectory['row_id'] == trajectory['prev_row_id']) & (
                trajectory['column_id'] ==
                trajectory['prev_column_id']))]
    
    # time -> time_id
    trajectory = convert_time(trajectory,interval)

    time_dividing_point = \
    list(np.arange(MIN_TIMESTAMP, MAX_TIMESTAMP, interval))
    
    flow_data_part = gen_flow_data(trajectory, time_dividing_point)
    flow_data = pd.concat(flow_data_part)

    flow_data = fill_empty_flow(
        flow_data, time_dividing_point, row_num, col_num
    )

    flow_data = flow_data.fillna(0)

    flow_data['id'] = flow_data.apply(
        lambda x: x['row_id']*column_num + x['column_id'],
        axis=1
    )
    
    return flow_data[
        ['id', 'row_id', 'column_id', 'time', 'inflow', 'outflow']
    ]

if __name__ == '__main__':
    data =ReadTrack()
    # 过滤超出北京范围的数据
    data = data.loc[
        data['lo'].apply(lambda x:(LON_MIN <= x <= LON_MAX))
    ]
    data = data.loc[
        data['la'].apply(lambda x:(LAT_MIN <= x <= LAT_MAX))
    ]
    # 行数
    row_num = 64
    # 列数
    column_num = 64
    # 时间间隔 1h
    interval = 3600
    # 输出文件夹名称
    output_dir_flow = 'output/T_DRIVE'
    # 创建输出文件夹
    if not os.path.exists(output_dir_flow):
        os.makedirs(output_dir_flow)

    trajectory = partition_to_grid(data, row_num, column_num, interval)
    
    flow = calculate_flow(trajectory, row_num, column_num)

    flow.to_csv(output_dir_flow+'/bjtaxi_64.csv', index = False)