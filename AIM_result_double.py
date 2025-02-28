import pandas as pd
from AIM_plot import *
from AIM_tolls import *
import os


# plist = [0.3, 0.5, 0.4, 0.3, 0.6, 0.5, 0.4, 0.3]
# time = 40
# car_information = make_car_information(plist, time)
# df = pd.DataFrame(car_information)
# print(df)
# df.to_csv("car_information_new1.csv")
# df1 = pd.read_csv("car_information_new1.csv")
# car_list = read_car_table_new(df1)
# print(car_list)
# print(len(car_list))
# print(int(72/16))
# a=[1,2,3,4,5]
# for i in range(72,72):
#     print(i+1)
# slight, elight = make_traffic_light_table(80, 32)
# print(slight)
# print(elight)


def batch_operation(folder_path):
    # 获取目录下的所有文件和文件夹的名称
    mode_name_list = ["无信号不考虑公平", "信号不考虑公平(c=16)", "信号不考虑公平(c=24)"]
    r1 = 1
    # r2 = 3
    experiment_name_list = []
    for i in range(1, 7):
        experiment_name_list.append("实验" + str(i))
    df = pd.DataFrame()
    MODE = []
    EXPERIMENT = []
    ROAD_DELAY_CAR = []
    TOTAL_DELAY_CAR = []
    ROAD_DELAY_BUS = []
    ROAD_DELAY_VEHICLE = []
    TOTAL_DELAY_BUS = []
    TOTAL_DELAY_VEHICLE = []
    CAR_TOTAL_TRAVEL_TIME = []
    BUS_TOTAL_TRAVEL_TIME = []
    VEHICLE_TOTAL_TRAVEL_TIME = []
    CAR_ROAD_TRAVEL_TIME = []
    BUS_ROAD_TRAVEL_TIME = []
    VEHICLE_ROAD_TRAVEL_TIME = []
    ROAD_CAR_NUM = []
    ROAD_BUS_NUM = []
    ROAD_VEHICLE_NUM = []
    TOTAL_CAR_NUM = []
    TOTAL_BUS_NUM = []
    TOTAL_VEHICLE_NUM = []
    AVERAGE_CAR_TRAVEL_TIME = []
    AVERAGE_BUS_TRAVEL_TIME = []
    AVERAGE_VEHICLE_TRAVEL_TIME = []
    AVERAGE_CAR_DELAY = []
    AVERAGE_BUS_DELAY = []
    AVERAGE_VEHICLE_DELAY = []
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
            car_total_travel_time = calculate_total_travel_time(car_travel_time)
            bus_total_travel_time = calculate_total_travel_time(bus_travel_time)
            vehicle_total_travel_time = calculate_total_travel_time(vehicle_travel_time)
            road_travel_time_car = sum(car_travel_time[r1 - 1])
            road_travel_time_bus = sum(bus_travel_time[r1 - 1])
            road_travel_time_vehicle = road_travel_time_bus + road_travel_time_car
            road_car_num = len(car_travel_time[r1 - 1])
            road_bus_num = len(bus_travel_time[r1 - 1])
            road_vehicle_num = road_car_num + road_bus_num
            total_car_num = 0
            for item in car_total_list:
                total_car_num += len(item)
            total_bus_num = 0
            for item in bus_total_list:
                total_bus_num += len(item)
            total_vehicle_num = 0
            for item in vehicle_total_list:
                total_vehicle_num += len(item)
            # 采集每项试验的结果

            MODE.append(mode)
            EXPERIMENT.append(experiment)

            TOTAL_CAR_NUM.append(total_car_num)
            TOTAL_BUS_NUM.append(total_bus_num)
            TOTAL_VEHICLE_NUM.append(total_vehicle_num)

            ROAD_CAR_NUM.append(road_car_num)
            ROAD_BUS_NUM.append(road_bus_num)
            ROAD_VEHICLE_NUM.append(road_vehicle_num)

            CAR_TOTAL_TRAVEL_TIME.append(car_total_travel_time)
            BUS_TOTAL_TRAVEL_TIME.append(bus_total_travel_time)
            VEHICLE_TOTAL_TRAVEL_TIME.append(vehicle_total_travel_time)

            CAR_ROAD_TRAVEL_TIME.append(road_travel_time_car)
            BUS_ROAD_TRAVEL_TIME.append(road_travel_time_bus)
            VEHICLE_ROAD_TRAVEL_TIME.append(road_travel_time_vehicle)

            TOTAL_DELAY_CAR.append(total_delay_car)
            TOTAL_DELAY_BUS.append(total_delay_bus)
            TOTAL_DELAY_VEHICLE.append(total_delay_vehicle)

            ROAD_DELAY_CAR.append(road_delay_car[r1 - 1])
            ROAD_DELAY_BUS.append(road_delay_bus[r1 - 1])
            ROAD_DELAY_VEHICLE.append(road_delay_car[r1 - 1] + road_delay_bus[r1 - 1])

            AVERAGE_CAR_TRAVEL_TIME.append(car_total_travel_time / total_car_num)
            AVERAGE_BUS_TRAVEL_TIME.append(bus_total_travel_time / total_bus_num)
            AVERAGE_VEHICLE_TRAVEL_TIME.append(vehicle_total_travel_time / total_vehicle_num)

            AVERAGE_CAR_DELAY.append(total_delay_car / total_car_num)
            AVERAGE_BUS_DELAY.append(total_delay_bus / total_bus_num)
            AVERAGE_VEHICLE_DELAY.append(total_delay_vehicle / total_vehicle_num)
            # print(total_delay_vehicle, total_travel_time)
            # print(total_travel_time - total_delay_vehicle)
            """fig = draw_travel_time(bus_travel_time)
            # fig.savefig('/Users/fyc/PycharmProjects/AIM/数据/' + lab_name + '/' + lab_num + '/' + 'Travel Time' + str(bus_mode) + '.svg', format='svg')
            fig.savefig(folder_path + mode + "/" + experiment + "/" + "公交车行驶时间.svg", format='svg')
            fig.show()
            x, y1_car, y1_bus, y2_car, y2_bus = get_trajectory(r1=r1, r2=r2, vehicle_total_list=vehicle_total_list,
                                                               position_address=vehicle_position_address)
            fig1 = draw_trajectory(x, y1_car, y1_bus, y2_car, y2_bus, r1=r1, r2=r2, mode=signal_mode)
            # fig.savefig('/Users/fyc/PycharmProjects/AIM/数据/' + lab_name + '/' +  lab_num + '/' + 'Trajectory' + str(bus_mode) + '.svg', format='svg')
            fig1.savefig(folder_path + mode + "/" + experiment + "/" + "车辆轨迹.svg", format='svg')
            fig.show()"""
    df['mode'] = MODE
    df['experiment'] = EXPERIMENT

    df['total car num'] = TOTAL_CAR_NUM
    df['total bus num'] = TOTAL_BUS_NUM
    df['total vehicle num'] = TOTAL_VEHICLE_NUM

    df['road car num[' + str(r1) + ']'] = ROAD_CAR_NUM
    df['road bus num[' + str(r1) + ']'] = ROAD_BUS_NUM
    df['road vehicle num[' + str(r1) + ']'] = ROAD_VEHICLE_NUM

    df['total travel time car'] = CAR_TOTAL_TRAVEL_TIME
    df['total travel time bus'] = BUS_TOTAL_TRAVEL_TIME
    df['total travel time vehicle'] = VEHICLE_TOTAL_TRAVEL_TIME

    df['road travel time car[' + str(r1) + ']'] = CAR_ROAD_TRAVEL_TIME
    df['road travel time bus[' + str(r1) + ']'] = BUS_ROAD_TRAVEL_TIME
    df['road travel time vehicle[' + str(r1) + ']'] = VEHICLE_ROAD_TRAVEL_TIME

    df['total delay car'] = TOTAL_DELAY_CAR
    df['total delay bus'] = TOTAL_DELAY_BUS
    df['total delay vehicle'] = TOTAL_DELAY_VEHICLE

    df['road delay car[' + str(r1) + ']'] = ROAD_DELAY_CAR
    df['road delay bus[' + str(r1) + ']'] = ROAD_DELAY_BUS
    df['road delay vehicle[' + str(r1) + ']'] = ROAD_DELAY_VEHICLE

    df['average car travel time'] = AVERAGE_CAR_TRAVEL_TIME
    df['average bus travel time'] = AVERAGE_BUS_TRAVEL_TIME
    df['average vehicle travel time'] = AVERAGE_VEHICLE_TRAVEL_TIME

    df['average car delay'] = AVERAGE_CAR_DELAY
    df['average bus delay'] = AVERAGE_BUS_DELAY
    df['average vehicle delay'] = AVERAGE_VEHICLE_DELAY

    df.to_csv(folder_path + "result.csv")


def main():
    # 指定要遍历的目录
    folder_path = '/Users/fyc/PycharmProjects/AIM/数据/车流密度变化1/测试4结果/'
    batch_operation(folder_path)


if __name__ == "__main__":
    main()
