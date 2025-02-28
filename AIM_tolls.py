import numpy as np
import pandas as pd
import gurobipy
import re
from AIM_tolls import *


def read_car_table():
    df = pd.read_excel('C:\\Users\\15470\PycharmProjects\IntersectionControl\AIM\数据\car_information.xlsx')
    car_information = []
    for item in df.values:
        item = list(item)
        car_information.append(item)
    # print(car_information)
    car_list = []
    for item in car_information:
        for num in range(1, len(item)):
            if str(item[num]) != "nan":
                car = [int(item[0]), int(item[num]), num]
                # print(car)
                car_list.append(car)
    '''for i in range(len(car_list)):
        if car_list[i][2] == 2:
            print(i+1)
    for i in range(len(car_list)):
        if car_list[i][2] == 5:
            print(i + 1)'''
    return car_list


def read_car_table_new(df):
    """读取发车时刻表的df，并提取有效的车辆，返回车辆信息表，里面的每个元素代表一个车辆的发车信息，按照道路顺序和时间排列
    第一个元素是发车时刻，第二个元素是车辆种类id（0为小汽车1为公交车），第三个元素是车辆所在道路"""
    car_information = []
    for item in df.values:
        item = list(item)
        car_information.append(item)
    car_list = []
    for i in range(1, len(car_information[0])):
        for j in range(len(car_information)):
            if str(car_information[j][i]) != "nan":
                car = [int(i - 1) * 2, int(car_information[j][i]), int(car_information[j][0]) + 1]
                car_list.append(car)
    return car_list


def make_traffic_light_table(total_time, cycle_time):
    """设计信号灯控制，根据总控制时间和循环周期时长来制作红灯时段表，返回两个列表，分别是每条道路的红灯起始时间和结束时间
    要求total_time和 cycle_time必须是4的倍数，且total_time模cycle_time(余数）不能超过（不大于）cycle_time的0.5
    倍，否则会存在某条路上开始时刻的红灯没被记录上"""
    slight = []
    elight = []
    for i in range(8):
        slight.append([])
        elight.append([])
        J = int(total_time / cycle_time) + 1
    for i in range(J):
        for j in range(len(slight)):
            if i * cycle_time + (j % 4) * (cycle_time / 4) < total_time:
                slight[j].append(int(i * cycle_time + (j % 4) * (cycle_time / 4)))
                elight[j].append(int(min(slight[j][i] + 3 / 4 * cycle_time, total_time)))
            elif slight[j][0] - cycle_time / 4 > 0:
                slight[j].append(0)
                elight[j].append(int(slight[j][0] - cycle_time / 4))
            else:
                slight[j].append(slight[j][0])
                elight[j].append(elight[j][0])
    return slight, elight


def make_traffic_light_table2(total_time, cycle_time):
    """设计信号灯控制，根据总控制时间和循环周期时长来制作红灯时段表，返回两个列表，分别是每条道路的红灯起始时间和结束时间
    要求total_time和 cycle_time必须是4的倍数，且total_time模cycle_time(余数）不能超过（不大于）cycle_time的0.5
    倍，否则会存在某条路上开始时刻的红灯没被记录上"""
    slight = []
    elight = []
    J = int(total_time / cycle_time) + 1
    for i in range(12):
        slight.append([])
        elight.append([])
    for i in range(J):
        for j in range(len(slight)):
            if i * cycle_time + (j % 4) * (cycle_time / 4) < total_time:
                slight[j].append(int(i * cycle_time + (j % 4) * (cycle_time / 4)))
                elight[j].append(int(min(slight[j][i] + 3 / 4 * cycle_time, total_time)))
            elif slight[j][0] - cycle_time / 4 > 0:
                slight[j].append(0)
                elight[j].append(int(slight[j][0] - cycle_time / 4))
            else:
                slight[j].append(slight[j][0])
                elight[j].append(elight[j][0])
    return slight, elight


def lp_model_analysis(MODEL, precision=3):
    if MODEL.status == gurobipy.GRB.Status.OPTIMAL:
        pd.set_option('display.precision', precision)  # 设置精度
        print("\nGlobal optimal solution found.")
        print(f"Objective Sense: {'MINIMIZE' if MODEL.ModelSense is 1 else 'MAXIMIZE'}")
        print(f"Objective Value = {MODEL.ObjVal}")
        try:
            print(pd.DataFrame([[var.X, var.RC] for var in MODEL.getVars()],
                               index=[var.Varname for var in MODEL.getVars()], columns=["Value", "Reduced Cost"]))
            print(pd.DataFrame([[Constr.Slack, Constr.pi] for Constr in MODEL.getConstrs()],
                               index=[Constr.constrName for Constr in MODEL.getConstrs()],
                               columns=["Slack or Surplus", "Dual Price"]))
            print("\nRanges in which the basis is unchanged: ")
            print(pd.DataFrame([[var.Obj, var.SAObjLow, var.SAObjUp] for var in MODEL.getVars()],
                               index=[var.Varname for var in MODEL.getVars()],
                               columns=["Cofficient", "Allowable Minimize", "Allowable Maximize"]))
            print("Righthand Side Ranges:")
            print(pd.DataFrame([[Constr.RHS, Constr.SARHSLow, Constr.SARHSUp] for Constr in MODEL.getConstrs()],
                               index=[Constr.constrName for Constr in MODEL.getConstrs()],
                               columns=["RHS", "Allowable Minimize", "Allowable Maximize"]))
        except:
            print(pd.DataFrame([var.X for var in MODEL.getVars()],
                               index=[var.Varname for var in MODEL.getVars()],
                               columns=["Value"]))
            print(pd.DataFrame([Constr.Slack for Constr in MODEL.getConstrs()],
                               index=[Constr.constrName for Constr in MODEL.getConstrs()],
                               columns=["Slack or Surplus"]))


def store_result_local(test_name, test_num, mode, model, car, total_time):
    car_position = []
    car_speed = []
    car_time = []
    for i in range(car):
        position = []
        speed = []
        time = []
        for j in range(total_time):
            for var in model.getVars():
                if var.Varname == "x" + "[" + str(i) + "," + str(j) + "]":
                    position.append(round(var.X, 3))
                    # print(f"{var.varName}: {round(var.X, 3)}")
                elif var.Varname == "v" + "[" + str(i) + "," + str(j) + "]":
                    speed.append(round(var.X, 3))
                    # print(f"{var.varName}: {round(var.X, 3)}")
                elif var.Varname == "w" + "[" + str(i) + "," + str(j) + "]":
                    time.append(round(var.X, 3))
                    # print(f"{var.varName}: {round(var.X, 3)}")
        car_position.append(position)
        car_speed.append(speed)
        car_time.append(time)
    df1 = pd.DataFrame(car_position)
    df2 = pd.DataFrame(car_speed)
    df3 = pd.DataFrame(car_time)
    df1.to_csv('C:\\Users\\15470\PycharmProjects\IntersectionControl\AIM\数据\\' + str(test_name) + '\\' + str(test_num) + '\\car_position' + str(
        mode) + '.csv')
    df2.to_csv('C:\\Users\\15470\PycharmProjects\IntersectionControl\AIM\数据\\' + str(test_name) + '\\' + str(test_num) + '\\car_speed' + str(
        mode) + '.csv')
    df3.to_csv('C:\\Users\\15470\PycharmProjects\IntersectionControl\AIM\数据\\' + str(test_name) + '\\' + str(test_num) + '\\car_time' + str(
        mode) + '.csv')
    # print(route_result)


def generate_car_flows(p, t):
    """按照伯努利分布生成一条道路上的车流"""
    flows = np.random.binomial(n=1, p=p, size=int(t / 2 + 1))
    return flows


def add_bus_flows(flows, start_time, gap):
    """对生成的车流列表里添加公交车，按照固定的发车间隔和起始的时间来生成。遍历列表，如果该值所处时间点不属于添加bus的话，
    判断：如果为0则将其变为空值，如果为1则将其变为0"""
    flows = list(flows)
    for i in range(len(flows)):
        if i < start_time / 2:
            if flows[i] == 0:
                flows[i] = None
            elif flows[i] == 1:
                flows[i] = 0
        else:
            if (i - start_time / 2) % (gap / 2) == 0:
                flows[i] = 1
            elif flows[i] == 0:
                flows[i] = None
            elif flows[i] == 1:
                flows[i] = 0
    return flows


def make_car_information(p_list, time):
    """生成发车信息表，其中p_list代表每一条道路上的车辆到达率（车流密度），time代表总发车时间"""
    # if len(p_list) != 8 or len(p_list) != 12:
    #     print("道路数量不正确！")
    # else:
    car_information_list = []
    for i in range(len(p_list)):
        flow = generate_car_flows(p_list[i], time)
        flow = list(flow)
        flow = add_bus_flows(flow, 2 * (i % 4), 8)
        car_information_list.append(flow)
    for i in range(len(p_list)):
        flow = add_bus_flows(flow, 2 * (i % 4), 8)
    return car_information_list


def store_result(local_address, model):
    car_position_i = []
    car_position_t = []
    car_position_x = []
    car_speed_i = []
    car_speed_t = []
    car_speed_x = []
    car_time_i = []
    car_time_t = []
    car_time_x = []
    for var in model.getVars():
        ptn = r'\d+'
        temp = re.findall(ptn, var.Varname)
        if var.Varname[0] == 'x':
            i = int(temp[0])
            t = int(temp[1])
            x = var.X
            car_position_i.append(i)
            car_position_t.append(t)
            car_position_x.append(x)
        elif var.Varname[0] == 'v':
            i = int(temp[0])
            t = int(temp[1])
            x = var.X
            car_speed_i.append(i)
            car_speed_t.append(t)
            car_speed_x.append(x)
        elif var.Varname[0] == 'w':
            i = int(temp[0])
            t = int(temp[1])
            x = var.X
            car_time_i.append(i)
            car_time_t.append(t)
            car_time_x.append(x)
        else:
            break
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    df1['idx'] = car_position_i
    df1['time'] = car_position_t
    df1['data'] = car_position_x
    df2['idx'] = car_speed_i
    df2['time'] = car_speed_t
    df2['data'] = car_speed_x
    df3['idx'] = car_time_i
    df3['time'] = car_time_t
    df3['data'] = car_time_x
    df1 = transform_to_origin_file(df1)
    df2 = transform_to_origin_file(df2)
    df3 = transform_to_origin_file(df3)
    df1.to_csv(local_address + "\\" + "position.csv")
    df2.to_csv(local_address + "\\" + "speed.csv")
    df3.to_csv(local_address + "\\" + "time.csv")
    # print(route_result)


def transform_to_origin_file(df):
    x = []
    X = []
    row0 = int(df['idx'][0])
    for index, row in df.iterrows():
        if row['idx'] == row0:
            x.append(float(row['data']))
        else:
            X.append(x)
            row0 = row['idx']
            x = [float(row['data'])]
    X.append(x)
    df = pd.DataFrame(X)
    return df


def main():
    read_car_table()


if __name__ == "__main__":
    main()
