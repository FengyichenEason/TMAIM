import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import csv
import seaborn as sns
import os
from copy import deepcopy
from Mutiagent_AIM_TEST import road_length, intersection_lowerbound, intersection_conflict, slight, elight
font_dirs = ["fonts"]
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
for font_file in font_files:
    font_manager.fontManager.addfont(font_file)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fs_car_short = 14  # 短直行道小汽车自由流旅行时间
fl_car_short = 13  # 短左转道小汽车自由流旅行时间
fs_bus_short = 16  # 短直行道大巴车自由流旅行时间
fl_bus_short = 15  # 短左转道大巴车自由流旅行时间
fs_car_long = 30  # 长直行道小汽车自由流旅行时间
fl_car_long = 30  # 短左转道小汽车自由流旅行时间
fs_bus_long = 36  # 短直行道大巴车自由流旅行时间
fl_bus_long = 35  # 短左转道大巴车自由流旅行时间


def get_vehicle_type_local(information_address):
    df = pd.read_excel(information_address)
    df_vehicle_information = pd.read_excel(information_address)
    vehicle_id = 0
    vehicle_total_list = []
    car_total_list = []
    bus_total_list = []
    for i in range(8):
        vehicle_total_list.append([])
        car_total_list.append([])
        bus_total_list.append([])
    for index, row in df_vehicle_information.iterrows():
        for road in range(1, len(row)):
            if row[road] == 0:
                car_total_list[road - 1].append([vehicle_id, int(row[0])])
                vehicle_total_list[road - 1].append([vehicle_id, int(row[0]), int(row[road])])  # 添加车辆编号，发车时间和车辆种类
                vehicle_id += 1
            elif row[road] == 1:
                bus_total_list[road - 1].append([vehicle_id, int(row[0])])
                vehicle_total_list[road - 1].append([vehicle_id, int(row[0]), int(row[road])])  # 添加车辆编号，发车时间和车辆种类
                vehicle_id += 1
            else:
                continue
    return vehicle_total_list, car_total_list, bus_total_list


def get_vehicle_type(information_address):
    df_vehicle_information = pd.read_csv(information_address)
    # print(df_vehicle_information)
    df_T = pd.DataFrame(df_vehicle_information.values.T)
    # print(df_T)
    vehicle_id = 0
    vehicle_total_list = []
    car_total_list = []
    bus_total_list = []
    for i in range(8):
        vehicle_total_list.append([])
        car_total_list.append([])
        bus_total_list.append([])
    for index, row in df_T.iterrows():
        for road in range(1, len(row)):
            if row[road] == 0:
                car_total_list[road - 1].append([vehicle_id, int(row[0])])
                vehicle_total_list[road - 1].append([vehicle_id, int(row[0]), int(row[road])])  # 添加车辆编号，发车时间和车辆种类
                vehicle_id += 1
            elif row[road] == 1:
                bus_total_list[road - 1].append([vehicle_id, int(row[0])])
                vehicle_total_list[road - 1].append([vehicle_id, int(row[0]), int(row[road])])  # 添加车辆编号，发车时间和车辆种类
                vehicle_id += 1
            else:
                continue
    return vehicle_total_list, car_total_list, bus_total_list


def get_vehicle_type_new(information_address):
    df_vehicle_information = pd.read_csv(information_address)
    # print(df_vehicle_information)
    df_T = pd.DataFrame(df_vehicle_information.values.T)
    # print(df_T)
    vehicle_id = 0
    vehicle_total_list = []
    car_total_list = []
    bus_total_list = []
    for i in range(12):
        vehicle_total_list.append([])
        car_total_list.append([])
        bus_total_list.append([])
    for index, row in df_T.iterrows():
        if int(index) > 0:
            for road in range(len(row)):
                # print(row[road])
                if row[road] == 0:
                    car_total_list[road].append([vehicle_id, (int(index)-1)*2])
                    vehicle_total_list[road].append([vehicle_id, (int(index)-1)*2, int(row[road])])  # 添加车辆编号，发车时间和车辆种类
                    vehicle_id += 1
                elif row[road] == 1:
                    bus_total_list[road].append([vehicle_id, (int(index)-1)*2])
                    vehicle_total_list[road].append([vehicle_id, (int(index)-1)*2, int(row[road])])  # 添加车辆编号，发车时间和车辆种类
                    vehicle_id += 1
                else:
                    continue
    return vehicle_total_list, car_total_list, bus_total_list


def calculate_travel_time(vehicle_total_list, time_table_address):
    df_vehicle_time_table = pd.read_csv(time_table_address)
    vehicle_total_travel_time = []
    for index, row in df_vehicle_time_table.iterrows():
        # print(index)
        # print(row)
        travel_time = 0
        for w in range(1, len(row)):
            travel_time += row[w]
        vehicle_total_travel_time.append(travel_time)
    # print(vehicle_total_travel_time)
    vehicle_travel_time = []
    bus_travel_time = []
    car_travel_time = []
    for road in vehicle_total_list:
        vehicle_road_travel_time_list = []
        car_road_travel_time_list = []
        bus_road_travel_time_list = []
        for vehicle in road:
            vehicle_road_travel_time_list.append(vehicle_total_travel_time[vehicle[0]])
            if vehicle[2] == 0:
                car_road_travel_time_list.append(vehicle_total_travel_time[vehicle[0]])
            elif vehicle[2] == 1:
                bus_road_travel_time_list.append(vehicle_total_travel_time[vehicle[0]])
        vehicle_travel_time.append(vehicle_road_travel_time_list)
        car_travel_time.append(car_road_travel_time_list)
        bus_travel_time.append(bus_road_travel_time_list)
    return vehicle_travel_time, car_travel_time, bus_travel_time


def calculate_total_travel_time(vehicle_travel_time):
    total_travel_time = 0
    for vehicle in vehicle_travel_time:
        if vehicle:
            total_travel_time += sum(vehicle)
    return total_travel_time


def calculate_delay_double(travel_time_list, vehicle_type=1):
    vehicle_delay = deepcopy(travel_time_list)
    if vehicle_type == 1:
        for i in range(len(vehicle_delay)):
            if i+1 == 3 or i+1 == 5 or i+1 == 9 or i+1 == 11:  # 短直行道
                for j in range(len(vehicle_delay[i])):
                    vehicle_delay[i][j] = vehicle_delay[i][j] - fs_bus_short
            elif i+1 == 2 or i+1 == 6 or i+1 == 8 or i+1 == 12:  # 短左转道
                for j in range(len(vehicle_delay[i])):
                    vehicle_delay[i][j] = vehicle_delay[i][j] - fl_bus_short
            elif i+1 == 1 or i+1 == 7:  # 长直行道
                for j in range(len(vehicle_delay[i])):
                    vehicle_delay[i][j] = vehicle_delay[i][j] - fs_bus_long
            elif i+1 == 4 or i+1 == 10:  # 长左转道
                for j in range(len(vehicle_delay[i])):
                    vehicle_delay[i][j] = vehicle_delay[i][j] - fl_bus_long
    elif vehicle_type == 0:
        for i in range(len(vehicle_delay)):
            if i+1 == 3 or i+1 == 5 or i+1 == 9 or i+1 == 11:  # 短直行道
                for j in range(len(vehicle_delay[i])):
                    vehicle_delay[i][j] = vehicle_delay[i][j] - fs_car_short
            elif i+1 == 2 or i+1 == 6 or i+1 == 8 or i+1 == 12:  # 短左转道
                for j in range(len(vehicle_delay[i])):
                    vehicle_delay[i][j] = vehicle_delay[i][j] - fl_car_short
            elif i+1 == 1 or i+1 == 7:  # 长直行道
                for j in range(len(vehicle_delay[i])):
                    vehicle_delay[i][j] = vehicle_delay[i][j] - fs_car_long
            elif i+1 == 4 or i+1 == 10:  # 长左转道
                for j in range(len(vehicle_delay[i])):
                    vehicle_delay[i][j] = vehicle_delay[i][j] - fl_car_long
    road_delay = []
    for item in vehicle_delay:
        if not item:
            road_delay.append(0)
        else:
            road_delay.append(sum(item))
    total_delay = sum(road_delay)
    return vehicle_delay, road_delay, total_delay


def calculate_delay(travel_time_list, vehicle_type=1):
    vehicle_delay = deepcopy(travel_time_list)
    if vehicle_type == 1:
        for i in range(len(vehicle_delay)):
            if i % 2 == 0:  # 直行道
                for j in range(len(vehicle_delay[i])):
                    vehicle_delay[i][j] = vehicle_delay[i][j] - fs_bus_short
            else:  # 左转道
                for j in range(len(vehicle_delay[i])):
                    vehicle_delay[i][j] = vehicle_delay[i][j] - fl_bus_short
    elif vehicle_type == 0:
        for i in range(len(vehicle_delay)):
            if i % 2 == 0:  # 直行道
                for j in range(len(vehicle_delay[i])):
                    vehicle_delay[i][j] = vehicle_delay[i][j] - fs_car_short
            else:  # 左转道
                for j in range(len(vehicle_delay[i])):
                    vehicle_delay[i][j] = vehicle_delay[i][j] - fl_car_short
    road_delay = []
    for item in vehicle_delay:
        if not item:
            road_delay.append(0)
        else:
            road_delay.append(sum(item))
    total_delay = sum(road_delay)
    return vehicle_delay, road_delay, total_delay


def draw_travel_time(bus_travel_time):
    y = []
    x = []
    h = []
    order = 0
    for i in range(len(bus_travel_time)):
        if bus_travel_time[i]:
            for j in range(len(bus_travel_time[i])):
                order += 1
                # x.append(order)
                x.append(order)
                h.append("第"+str(i+1)+"路")
                y.append(bus_travel_time[i][j])
    X = np.array(x)
    Y = np.array(y)
    H = np.array(h)
    # print(X)
    # print(Y)
    sns.barplot(x=X, y=Y, hue=H, dodge=False)
    plt.ylim(0, 1.8 * max(Y))
    # 坐标轴标签
    plt.xlabel('公交车序列',
               rotation=0,  # 旋转角度
               )
    plt.ylabel('旅行时间(单位:s)',
               rotation=90,  # 旋转角度
               horizontalalignment='right',  # 水平对齐方式
               )
    plt.title("公交车旅行时间分布图", fontsize=16)
    ax = plt.gca()
    ax.axes.xaxis.set_ticks([])
    return plt


def get_trajectory(r1, r2, vehicle_total_list, position_address):
    vehicle_position_csv = open(position_address)
    reader = csv.reader(vehicle_position_csv)
    data = list(reader)
    length_h = len(data)  # 车辆数+1
    length_l = len(data[0])  # 总时间步长+1
    x = []
    y1_car = []
    y1_bus = []
    y2_car = []
    y2_bus = []
    for time_step in range(1, length_l):
        x.append(int(data[0][time_step]))
    for vehicle in vehicle_total_list[r1-1]:
        car_list = []
        bus_list = []
        if vehicle[2] == 0:
            for time_step in range(1, length_l):
                car_list.append(float(data[vehicle[0]+1][time_step]))
            y1_car.append(car_list)
        elif vehicle[2] == 1:
            for time_step in range(1, length_l):
                bus_list.append(float(data[vehicle[0]+1][time_step]))
            y1_bus.append(bus_list)
    for vehicle in vehicle_total_list[r2-1]:
        car_list = []
        bus_list = []
        if vehicle[2] == 0:
            for time_step in range(1, length_l):
                car_list.append(road_length[r2-1] - float(data[vehicle[0]+1][time_step]))
            y2_car.append(car_list)
        elif vehicle[2] == 1:
            for time_step in range(1, length_l):
                bus_list.append(road_length[r2-1] - float(data[vehicle[0]+1][time_step]))
            y2_bus.append(bus_list)
    return x, y1_car, y1_bus, y2_car, y2_bus


def data_clean_r1(vehicle_trajectory_list, r1):
    road_len = road_length[r1-1]
    for vehicle in vehicle_trajectory_list:
        i = 0
        j = len(vehicle) - 1
        while vehicle[i] == 0:
            if vehicle[i+1] == vehicle[i]:
                vehicle[i] = None
            i += 1
        while vehicle[j] >= road_len:
            if not vehicle[j-1] < road_len:
                vehicle[j] = None
            j += -1
    return vehicle_trajectory_list


def data_clean_r2(vehicle_trajectory_list, r2):
    road_len = road_length[r2-1]
    for vehicle in vehicle_trajectory_list:
        i = 0
        j = len(vehicle) - 1
        while vehicle[i] == road_len:
            if vehicle[i + 1] == vehicle[i]:
                vehicle[i] = None
            i += 1
        while vehicle[j] <= 0:
            if not vehicle[j - 1] > 0:
                vehicle[j] = None
            j += -1
    return vehicle_trajectory_list


def draw_trajectory(x, y1_car, y1_bus, y2_car, y2_bus, r1, r2, mode):
    global conflict_out_r1, conflict_in_r1, conflict_in_r2, conflict_out_r2
    X = np.array(x)
    y1_car = data_clean_r1(y1_car, r1)
    y1_bus = data_clean_r1(y1_bus, r1)
    y2_car = data_clean_r2(y2_car, r2)
    y2_bus = data_clean_r2(y2_bus, r2)
    for i in range(len(y1_car)):
        Y1_car = np.array(y1_car[i])
        if i == 0:
            plt.plot(X, Y1_car, marker='o', ms=0.5, mfc='black', color='black', linewidth=0.7, linestyle='-', label="第"+str(r1)+"路小汽车轨迹图")
        else:
            plt.plot(X, Y1_car, marker='o', ms=0.5, mfc='black', color='black', linewidth=0.7, linestyle='-')
    for i in range(len(y1_bus)):
        Y1_bus = np.array(y1_bus[i])
        if i == 0:
            plt.plot(X, Y1_bus, marker='o', ms=0.5, mfc='black', color='black', linewidth=1.2, linestyle='-', label="第"+str(r1)+"路公交车轨迹图")
        else:
            plt.plot(X, Y1_bus, marker='o', ms=0.5, mfc='black', color='black', linewidth=1.2, linestyle='-')
    for i in range(len(y2_car)):
        Y2_car = np.array(y2_car[i])
        if i == 0:
            plt.plot(X, Y2_car, marker='o', ms=0.5, mfc='blue', color='blue', linewidth=0.7, linestyle='-', label="第"+str(r2)+"路小汽车轨迹图")
        else:
            plt.plot(X, Y2_car, marker='o', ms=0.5, mfc='blue', color='blue', linewidth=0.7, linestyle='-')
    for i in range(len(y2_bus)):
        Y2_bus = np.array(y2_bus[i])
        if i == 0:
            plt.plot(X, Y2_bus, marker='o', ms=0.5, mfc='blue', color='blue', linewidth=1.2, linestyle='-', label="第"+str(r2)+"路公交车轨迹图")
        else:
            plt.plot(X, Y2_bus, marker='o', ms=0.5, mfc='blue', color='blue', linewidth=1.2, linestyle='-')
    plt.ylim(0, max(road_length[r1-1], road_length[r2-1]))
    plt.xlim(0, len(X))
    if mode == 0:
        count = 0
        for road in intersection_conflict:
            for conflict_point in road:
                count += 1
                if int(conflict_point[0]) == r1 and int(conflict_point[1] == r2):
                    conflict_in_r1 = conflict_point[2]
                    conflict_out_r1 = conflict_point[3]
                    order_r1 = count
                elif int(conflict_point[0]) == r2 and int(conflict_point[1] == r1):
                    conflict_in_r2 = road_length[r2-1] - conflict_point[2]
                    conflict_out_r2 = road_length[r2-1] - conflict_point[3]
                    order_r2 = count
            # 画辅助线
        plt.axhline(y=conflict_in_r1,  # 线高
                    xmin=X[0],  # 线起始位置
                    xmax=X[-1],  # 线结束位置
                    color="green",
                    label=r"$\mu_{"+str(order_r1)+","+str(r1)+"}^{in}$",
                    linestyle='--',  # 线型
                    linewidth=0.5,  # 线宽
                    # marker='*',#线两端marker
                    markerfacecolor='w',
                    markersize=10,  # marker大小
                    )
        plt.axhline(y=conflict_out_r1,  # 线高
                    xmin=X[0],  # 线起始位置
                    xmax=X[-1],  # 线结束位置
                    color="green",
                    label=r"$\mu_{"+str(order_r1)+","+str(r1)+"}^{out}$",
                    linestyle='-.',  # 线型
                    linewidth=0.5,  # 线宽
                    # marker='*',#线两端marker
                    markerfacecolor='w',
                    markersize=10,  # marker大小
                    )
        plt.axhline(y=conflict_in_r2,  # 线高
                    xmin=X[0],  # 线起始位置
                    xmax=X[-1],  # 线结束位置
                    color="red",
                    label=r"$\mu_{"+str(order_r2)+","+str(r2)+"}^{in}$",
                    linestyle='--',  # 线型
                    linewidth=0.5,  # 线宽
                    # marker='*',#线两端marker
                    markerfacecolor='w',
                    markersize=10,  # marker大小
                    )
        plt.axhline(y=conflict_out_r2,  # 线高
                    xmin=X[0],  # 线起始位置
                    xmax=X[-1],  # 线结束位置
                    color="red",
                    label=r"$\mu_{"+str(order_r2)+","+str(r2)+"}^{out}$",
                    linestyle='-.',  # 线型
                    linewidth=0.5,  # 线宽
                    # marker='*',#线两端marker
                    markerfacecolor='w',
                    markersize=10,  # marker大小
                    )
    elif mode == 1:
        b1 = intersection_lowerbound[r1-1]
        b2 = road_length[r2-1] - intersection_lowerbound[r2-1]
        for i in range(len(slight[0])):
            if elight[r1-1][i] < len(X):
                plt.axhline(y=b1,  # 线高
                            xmin=slight[r1-1][i]/len(X),  # 线起始位置
                            xmax=(elight[r1-1][i] - 1)/len(X),  # 线结束位置
                            color="red",
                            linestyle='-',  # 线型
                            linewidth=1,  # 线宽
                            # marker='*',#线两端marker
                            markerfacecolor='w',
                            markersize=10,  # marker大小
                            )
            if elight[r2-1][i] < len(X):
                plt.axhline(y=b2,  # 线高
                            xmin=slight[r2 - 1][i] / len(X),  # 线起始位置
                            xmax=(elight[r2 - 1][i] - 1) / len(X),  # 线结束位置
                            color="red",
                            linestyle='-',  # 线型
                            linewidth=1,  # 线宽
                            # marker='*',#线两端marker
                            markerfacecolor='w',
                            markersize=10,  # marker大小
                            )
            if not elight[r1-1][i] < len(X):
                plt.axhline(y=b1,  # 线高
                            xmin=slight[r1-1][i] / len(X),  # 线起始位置
                            xmax=(elight[r1-1][i]) / len(X),  # 线结束位置
                            color="red",
                            linestyle='-',  # 线型
                            linewidth=1,  # 线宽
                            # marker='*',#线两端marker
                            markerfacecolor='w',
                            markersize=10,  # marker大小
                            )
            if not elight[r2-1][i] < len(X):
                plt.axhline(y=b2,  # 线高
                            xmin=slight[r2-1][i] / len(X),  # 线起始位置
                            xmax=(elight[r2-1][i]) / len(X),  # 线结束位置
                            color="red",
                            linestyle='-',  # 线型
                            linewidth=1,  # 线宽
                            # marker='*',#线两端marker
                            markerfacecolor='w',
                            markersize=10,  # marker大小
                            )
        plt.axhline(y=b1,  # 线高
                    xmin=0,  # 线起始位置
                    xmax=1,  # 线结束位置
                    color="green",
                    linestyle='--',  # 线型
                    linewidth=0.5,  # 线宽
                    # marker='*',#线两端marker
                    markerfacecolor='w',
                    markersize=10,  # marker大小
                    )
        plt.axhline(y=b2,  # 线高
                    xmin=0,  # 线起始位置
                    xmax=1,  # 线结束位置
                    color="green",
                    linestyle='--',  # 线型
                    linewidth=0.5,  # 线宽
                    # marker='*',#线两端marker
                    markerfacecolor='w',
                    markersize=10,  # marker大小
                    )
    plt.legend(loc="lower right", fontsize=7,title='图例', title_fontsize=7)
    plt.xlabel('时间(单位:s)',
               rotation=0,  # 旋转角度
               )
    plt.ylabel('位移(单位:m)',
               rotation=90,  # 旋转角度
               horizontalalignment='right',  # 水平对齐方式
               )
    plt.title(str(r1)+"路-"+str(r2)+"路轨迹图", fontsize=16)
    fig = plt.figure(num=1, figsize=(1000, 40), dpi=300)
    return fig


def test():
    while True:
        lab_name = str(input("请输入实验名称："))
        lab_num = str(input("请输入实验编号："))
        signal_mode = int(input("请输入信号控制模式（无信号控制为0，信号控制为1）："))
        bus_mode = int(input("请输入车辆控制模式（不考虑公平效益控制为1，考虑公平效益为2）："))
        r1 = int(input("请输入需要绘制轨迹的道路r1编号："))
        r2 = int(input("请输入需要绘制轨迹的道路r2编号："))
        '''vehicle_information_address = "/Users/fyc/PycharmProjects/AIM/数据/car_information" + str(lab_num) + ".xlsx"
        vehicle_time_table_address = "/Users/fyc/PycharmProjects/AIM/数据/" + lab_name + '/' + lab_num + '/' + "/car_time" + str(bus_mode) + ".csv"
        vehicle_position_address = "/Users/fyc/PycharmProjects/AIM/数据/" + lab_name + '/' + lab_num + '/' + "/car_position" + str(bus_mode) + ".csv"'''
        vehicle_information_address = "car_information_new.csv"
        vehicle_time_table_address = "test6.csv"
        vehicle_position_address = "test4.csv"
        vehicle_total_list, car_total_list, bus_total_list = get_vehicle_type_new(vehicle_information_address)
        vehicle_travel_time, car_travel_time, bus_travel_time = calculate_travel_time(vehicle_total_list, vehicle_time_table_address)
        # print(vehicle_travel_time)
        # print(car_travel_time)
        # print(bus_travel_time)
        vehicle_delay_car, road_delay_car, total_delay_car = calculate_delay(car_travel_time, 0)
        vehicle_delay_bus, road_delay_bus, total_delay_bus = calculate_delay(bus_travel_time, 1)
        total_delay_vehicle = total_delay_car + total_delay_bus
        total_travel_time = calculate_total_travel_time(vehicle_travel_time)
        print(total_delay_vehicle, total_travel_time)
        print(total_travel_time-total_delay_vehicle)
        fig = draw_travel_time(bus_travel_time)
        # fig.savefig('/Users/fyc/PycharmProjects/AIM/数据/' + lab_name + '/' + lab_num + '/' + 'Travel Time' + str(bus_mode) + '.svg', format='svg')
        fig.savefig('/Users/fyc/PycharmProjects/AIM/数据/test1.svg', format='svg')
        fig.show()
        x, y1_car, y1_bus, y2_car, y2_bus = get_trajectory(r1, r2, vehicle_total_list, vehicle_position_address)
        fig = draw_trajectory(x, y1_car, y1_bus, y2_car, y2_bus, r1, r2, mode=signal_mode)
        # fig.savefig('/Users/fyc/PycharmProjects/AIM/数据/' + lab_name + '/' +  lab_num + '/' + 'Trajectory' + str(bus_mode) + '.svg', format='svg')
        fig.savefig('/Users/fyc/PycharmProjects/AIM/数据/test2.svg', format='svg')
        fig.show()


def main():
    # 指定要遍历的目录
    folder_path = '/Users/fyc/PycharmProjects/AIM/数据/车流密度变化/'

    # 获取目录下的所有文件和文件夹的名称
    mode_name_list = ["无信号不考虑公平", "无信号考虑公平", "信号不考虑公平", "信号考虑公平"]
    experiment_name_list = []
    for i in range(1, 7):
        experiment_name_list.append("实验" + str(i))
    df = pd.DataFrame()
    MODE = []
    EXPERIMENT = []
    ROAD_DELAY_CAR = []
    TOTAL_DELAY_CAR = []
    ROAD_DELAY_BUS = []
    TOTAL_DELAY_BUS = []
    TOTAL_DELAY_VEHICLE = []
    TOTAL_TRAVEL_TIME = []
    for mode in mode_name_list:
        if mode == "无信号不考虑公平" or mode == "无信号考虑公平":
            signal_mode = 0
        else:
            signal_mode = 1
        for experiment in experiment_name_list:
            vehicle_information_address = folder_path + experiment + ".csv"  # 发车信息表
            file_names = os.listdir(folder_path + mode + "/" + experiment)  # 每个模式下一项实验中的全部文件名称
            for file_name in file_names:
                if file_name == "position.csv":
                    vehicle_position_address = os.path.join(folder_path + mode + "/" + experiment, file_name)
                if file_name == "time.csv":
                    vehicle_time_table_address = os.path.join(folder_path + mode + "/" + experiment, file_name)
            vehicle_total_list, car_total_list, bus_total_list = get_vehicle_type_new(vehicle_information_address)
            vehicle_travel_time, car_travel_time, bus_travel_time = calculate_travel_time(vehicle_total_list,
                                                                                          vehicle_time_table_address)
            # print(vehicle_travel_time)
            # print(car_travel_time)
            # print(bus_travel_time)
            vehicle_delay_car, road_delay_car, total_delay_car = calculate_delay(car_travel_time, 0)
            vehicle_delay_bus, road_delay_bus, total_delay_bus = calculate_delay(bus_travel_time, 1)
            total_delay_vehicle = total_delay_car + total_delay_bus
            total_travel_time = calculate_total_travel_time(vehicle_travel_time)
            MODE.append(mode)
            EXPERIMENT.append(experiment)
            TOTAL_TRAVEL_TIME.append(total_travel_time)
            TOTAL_DELAY_VEHICLE.append(total_delay_vehicle)
            ROAD_DELAY_CAR.append(road_delay_car[1])
            TOTAL_DELAY_CAR.append(total_delay_car)
            ROAD_DELAY_BUS.append(road_delay_bus[1])
            TOTAL_DELAY_BUS.append(total_delay_bus)
            # print(total_delay_vehicle, total_travel_time)
            # print(total_travel_time - total_delay_vehicle)
            fig = draw_travel_time(bus_travel_time)
            # fig.savefig('/Users/fyc/PycharmProjects/AIM/数据/' + lab_name + '/' + lab_num + '/' + 'Travel Time' + str(bus_mode) + '.svg', format='svg')
            fig.savefig(folder_path + mode + "/" + experiment + "/" + "公交车行驶时间.svg", format='svg')
            fig.show()
            x, y1_car, y1_bus, y2_car, y2_bus = get_trajectory(r1=2, r2=5, vehicle_total_list=vehicle_total_list, position_address=vehicle_position_address)
            fig1 = draw_trajectory(x, y1_car, y1_bus, y2_car, y2_bus, r1=2, r2=5, mode=signal_mode)
            # fig.savefig('/Users/fyc/PycharmProjects/AIM/数据/' + lab_name + '/' +  lab_num + '/' + 'Trajectory' + str(bus_mode) + '.svg', format='svg')
            fig1.savefig(folder_path + mode + "/" + experiment + "/" + "车辆轨迹.svg", format='svg')
            fig.show()
    """df['mode'] = MODE
    df["experiment"] = EXPERIMENT
    df["total travel time"] = TOTAL_TRAVEL_TIME
    df["total delay vehicle"] = TOTAL_DELAY_VEHICLE
    df["road delay car[2]"] = ROAD_DELAY_CAR
    df["total delay car"] = TOTAL_DELAY_CAR
    df["road delay bus[2]"] = ROAD_DELAY_BUS
    df["total delay bus"] = TOTAL_DELAY_BUS
    df.to_csv(folder_path + "result.csv")"""


if __name__ == "__main__":
    main()
