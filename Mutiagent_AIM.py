import gurobipy
from gurobipy import Model
from AIM import AIM_tolls
import math

# 创建参数信息
car_list = AIM_tolls.read_car_table()  # 列表顺序即车辆顺序，子元素中第一个元素是发车时间，第二是车辆类型，第三个是车辆道路
l_c = 3
l_b = 8
l_buffer = 25
v_min = 0
v_max = 12
v_bus_min = 0
v_bus_max = 10
a_min = -3
a_max = 3
a_bus_min = -2
a_bus_max = 2
v0 = 6
reaction_time = 0.3
bus_reaction_time = 0.6
car = 95
cost_car = 1
cost_bus = 1
total_time = 72
intersection_conflict_num = 4
M = 1000000
e = 0.2
C = 16
J = int(total_time / C) + 1
# 创建数据结构信息
road = [1, 2, 3, 4, 5, 6, 7, 8]
car_type = []
for item in car_list:
    car_type.append(item[1])
'''car_type = [1, 0, 0, 1, 0, 0, 0, 1,
            0, 0, 1, 0, 0, 1, 0, 0,
            0, 0, 0, 0, 0, 0, 1, 0,
            0, 1, 0, 0, 1, 0, 0, 0,
            1, 0, 0, 1, 0, 0, 0, 1,
            0, 0, 1, 0, 0, 1, 0, 0,
            0, 0, 0, 0, 0, 0, 1, 0,
            0, 1, 0, 0, 1, 0, 0, 0]'''
car_route = []
for item in car_list:
    car_route.append(item[2])
initial_time = []
for item in car_list:
    initial_time.append(item[0])
road_length = [154, 145, 154, 145, 154, 145, 154, 145]
intersection_lowerbound = [50, 49.75, 50, 49.75, 50, 49.75, 50, 49.75]
slight = [
    [0, 16, 32, 48, 64],
    [4, 20, 36, 52, 68],
    [0, 8, 24, 40, 56],
    [0, 12, 28, 44, 60],
    [0, 16, 32, 48, 64],
    [4, 20, 36, 52, 68],
    [0, 8, 24, 40, 56],
    [0, 12, 28, 44, 60]
]
elight = [
    [12, 28, 44, 60, 72],
    [16, 32, 48, 64, 72],
    [4, 20, 36, 52, 68],
    [8, 24, 40, 56, 72],
    [12, 28, 44, 60, 72],
    [16, 32, 48, 64, 72],
    [4, 20, 36, 52, 68],
    [8, 24, 40, 56, 72]
]
slight2 = [
    [0, 24, 48, 72],
    [6, 30, 54, 72],
    [0, 12, 36, 60],
    [0, 18, 42, 66],
    [0, 24, 48, 72],
    [6, 30, 54, 72],
    [0, 12, 36, 60],
    [0, 18, 42, 66]
]
elight2 = [
    [18, 42, 66, 72],
    [24, 48, 72, 72],
    [6, 30, 54, 72],
    [12, 36, 60, 72],
    [18, 42, 66, 72],
    [24, 48, 72, 72],
    [6, 30, 54, 72],
    [12, 36, 60, 72]
]

'''slight = [
    [0, 32, 64],
    [8, 40, 72],
    [0, 16, 48],
    [0, 24, 56],
    [0, 32, 64],
    [8, 40, 72],
    [0, 16, 48],
    [0, 24, 56]
]
elight = [
    [24, 56, 72],
    [32, 64, 72],
    [8, 40, 72],
    [16, 48, 72],
    [24, 56, 72],
    [32, 64, 72],
    [8, 40, 72],
    [16, 48, 72]
]'''
intersection_conflict = [
    [[1, 8, 61.81, 73.83], [1, 3, 70.00, 73.50], [1, 7, 80.50, 84.00], [1, 6, 80.16, 92.18]],
    [[2, 8, 55.93, 64.85], [2, 5, 63.43, 75.00], [2, 3, 70.04, 81.60], [2, 4, 80.20, 89.11]],
    [[3, 2, 60.81, 73.83], [3, 5, 70.00, 73.50], [3, 1, 80.50, 84.00], [3, 8, 80.16, 92.18]],
    [[4, 2, 55.93, 64.85], [4, 7, 63.43, 75.00], [4, 5, 70.04, 81.60], [4, 6, 80.20, 89.11]],
    [[5, 4, 61.81, 73.83], [5, 7, 70.00, 73.50], [5, 3, 80.50, 84.00], [5, 2, 80.16, 92.18]],
    [[6, 4, 55.93, 64.85], [6, 1, 63.43, 75.00], [6, 7, 70.04, 81.60], [6, 8, 80.20, 89.11]],
    [[7, 6, 60.81, 73.83], [7, 1, 70.00, 73.50], [7, 5, 80.50, 84.00], [7, 4, 80.16, 92.18]],
    [[8, 6, 55.93, 64.85], [8, 3, 63.43, 75.00], [8, 1, 70.04, 81.60], [8, 2, 80.20, 89.11]]
]
car_intersection_conflict = []
for cars in range(car):  # 给每辆车
    c_road_list = []
    for i in range(intersection_conflict_num):
        c_road_list.append(intersection_conflict[car_route[cars] - 1][i])
    car_intersection_conflict.append(c_road_list)


def AIM_problem(mode, consider):
    # 创建模型
    MODEL: Model = gurobipy.Model()
    MODEL.Params.NonConvex = 2

    # 创建变量
    x = MODEL.addVars(car, total_time, name='x')  # 车辆c在t时刻的位置
    v = MODEL.addVars(car, total_time, name='v')  # 车辆c在t时刻速率
    w = MODEL.addVars(car, total_time, vtype=gurobipy.GRB.BINARY, name='w')  # 车辆c在t时刻是否在有效区域内
    theta = MODEL.addVars(car, total_time, vtype=gurobipy.GRB.BINARY, name='theta')  # 车辆c在t时刻是否在有进入初始点
    y_in = MODEL.addVars(intersection_conflict_num, car, total_time, vtype=gurobipy.GRB.BINARY, name='y_in')
    y_out = MODEL.addVars(intersection_conflict_num, car, total_time, vtype=gurobipy.GRB.BINARY, name='y_out')
    p = MODEL.addVars(car, J, vtype=gurobipy.GRB.BINARY, name='p')

    # 更新变量环境
    MODEL.update()

    # 创建目标函数
    # MODEL.setObjective(sum(car[i + 1] * Cost[i] for i in range(6)), sense=gurobipy.GRB.MAXIMIZE)
    MODEL.setObjective(gurobipy.quicksum(cost_car * ((1-car_type[c]) * w[c, t]) + cost_bus * (car_type[c] * w[c, t])
                                         for c in range(car) for t in range(total_time)), sense=gurobipy.GRB.MINIMIZE)

    # 创建约束条件

    # 初始速度约束
    MODEL.addConstrs(v[c, initial_time[c]] == v0 for c in range(car))

    # Constraints 1
    #  MODEL.addConstrs(theta[c, t] == 1 for c in range(car) for t in range(initial_time[c], total_time))
    MODEL.addConstrs(w[c, t] == 0 for c in range(car) for t in range(initial_time[c]))
    MODEL.addConstrs(w[c, t] <= theta[c, t] for c in range(car) for t in range(total_time))

    # Constraints 2
    MODEL.addConstrs((theta[c, t] - 1) * M <= x[c, t] for c in range(car) for t in range(total_time))
    MODEL.addConstrs(theta[c, t] * M >= x[c, t] for c in range(car) for t in range(total_time))
    MODEL.addConstrs((w[c, t] - theta[c, t]) * M <= road_length[car_route[c] - 1] - x[c, t]
                     for c in range(car) for t in range(total_time))
    MODEL.addConstrs((w[c, t] - theta[c, t] + 1) * M >= road_length[car_route[c] - 1] - x[c, t]
                     for c in range(car) for t in range(total_time))

    # Constraints 7
    MODEL.addConstrs(w[c, initial_time[c]] == 1 for c in range(car))
    MODEL.addConstrs(x[c, initial_time[c]] == 0 for c in range(car))
    MODEL.addConstrs((x[c, t] - x[c, t1] <= 0 for c in range(car)
                      for t in range(total_time) for t1 in range(t, total_time)))

    # Constraints 8
    MODEL.addConstrs(x[c, total_time - 1] >= road_length[car_route[c] - 1] for c in range(car))

    # Constraints 9A
    MODEL.addConstrs(x[c, t] == x[c, t - 1] + 1 / 2 * (v[c, t - 1] + v[c, t])
                     for c in range(car) for t in range(initial_time[c] + 1, total_time))

    # Constraints 9B
    MODEL.addConstrs((v[c, t] - v_min) * (1 - car_type[c]) >= 0 for c in range(car)
                     for t in range(initial_time[c], total_time))
    MODEL.addConstrs((v[c, t] - v_bus_min) * car_type[c] >= 0 for c in range(car)
                     for t in range(initial_time[c], total_time))
    MODEL.addConstrs(v[c, t] * (1 - car_type[c]) <= v_max for c in range(car)
                     for t in range(initial_time[c], total_time))
    MODEL.addConstrs(v[c, t] * car_type[c] <= v_bus_max for c in range(car)
                     for t in range(initial_time[c], total_time))

    # Constraints 9C
    MODEL.addConstrs((v[c, t] - v[c, t - 1]) * (1 - car_type[c]) >= a_min
                     for c in range(car) for t in range(initial_time[c] + 1, total_time))
    MODEL.addConstrs((v[c, t] - v[c, t - 1]) * car_type[c] >= a_bus_min
                     for c in range(car) for t in range(initial_time[c] + 1, total_time))
    MODEL.addConstrs((v[c, t] - v[c, t - 1]) * (1 - car_type[c]) <= a_max
                     for c in range(car) for t in range(initial_time[c] + 1, total_time))
    MODEL.addConstrs((v[c, t] - v[c, t - 1]) * car_type[c] <= a_bus_max
                     for c in range(car) for t in range(initial_time[c] + 1, total_time))

    # Constraints 10
    MODEL.addConstrs(w[c, t] * (x[c, t] - x[c1, t]) >= w[c, t] * (((l_c * (1-car_type[c]) + l_b * car_type[c]) + reaction_time * v[c1, t]) * (1 - car_type[c1]) +
                                                                  ((l_c * (1-car_type[c]) + l_b * car_type[c]) + bus_reaction_time * v[c1, t]) * car_type[c1])
                     for c in range(car) for c1 in range(c + 1, car) for t in range(total_time)
                     if t >= initial_time[c1] and car_route[c] == car_route[c1])
    if int(mode) == 0:
        # Constraints 11
        MODEL.addConstrs(y_in[b, c, t] * M >= x[c, t] - car_intersection_conflict[c][b][2]
                         for c in range(car) for t in range(total_time) for b in range(intersection_conflict_num))
        MODEL.addConstrs((y_in[b, c, t] - 1) * M <= x[c, t] - car_intersection_conflict[c][b][2]
                         for c in range(car) for t in range(total_time) for b in range(intersection_conflict_num))
        MODEL.addConstrs(y_out[b, c, t] * M >= car_intersection_conflict[c][b][3] - x[c, t]
                         for c in range(car) for t in range(total_time) for b in range(intersection_conflict_num))
        MODEL.addConstrs((y_out[b, c, t] - 1) * M <= car_intersection_conflict[c][b][3] - x[c, t]
                         for c in range(car) for t in range(total_time) for b in range(intersection_conflict_num))

        # Constraints 12
        MODEL.addConstrs(y_in[b, c, t] + y_out[b, c, t] + y_in[b1, c1, t] + y_out[b1, c1, t] <= 3
                         for c in range(car) for c1 in range(car) for t in range(total_time)
                         for b in range(intersection_conflict_num) for b1 in range(intersection_conflict_num)
                         if car_route[c] != car_route[c1]
                         and car_intersection_conflict[c][b][1] == car_route[c1]
                         and car_intersection_conflict[c1][b1][1] == car_route[c])

    if int(consider) == 1:
        # Constraints 13 AIM considering Equity
        MODEL.addConstrs(car_type[c] * gurobipy.quicksum(w[c, t] for t in range(total_time)) >=
                         (1 - e) * car_type[c] * gurobipy.quicksum(w[c1, t] for t in range(total_time))
                         for c in range(car) for c1 in range(car) if c != c1 and car_type[c1] == 1)
        MODEL.addConstrs(car_type[c] * gurobipy.quicksum(w[c, t] for t in range(total_time)) <=
                         (1 + e) * car_type[c] * gurobipy.quicksum(w[c1, t] for t in range(total_time))
                         for c in range(car) for c1 in range(car) if c != c1 and car_type[c1] == 1)
    # 边界约束
    MODEL.addConstrs((x[c, t] - road_length[car_route[c] - 1] + 0.1) * w[c, t] <= 0.00000001
                     for c in range(car) for t in range(initial_time[c], total_time))

    if int(mode) == 1:
        # Constraints 14 Signal-based strategy
        MODEL.addConstrs(intersection_lowerbound[car_route[c] - 1] - x[c, slight[car_route[c] - 1][j]] >=
                         (p[c, j] - 1) * M for c in range(car) for j in range(J))
        MODEL.addConstrs(intersection_lowerbound[car_route[c] - 1] - x[c, slight[car_route[c] - 1][j]] <=
                         p[c, j] * M for c in range(car) for j in range(J))
        MODEL.addConstrs(intersection_lowerbound[car_route[c] - 1] - x[c, t] >=
                         (w[c, t] + p[c, j] - 2) * M for c in range(car) for j in range(J)
                         for t in range(slight[car_route[c] - 1][j], elight[car_route[c] - 1][j]))

    # 执行线性规划模型
    MODEL.optimize()
    return MODEL

# Routes = gurobipy.tuplelist(x)

# 输出模型结果


def main():
    test_name = str(input("请输入实验名称："))
    test_num = str(input("请输入实验编号："))
    mode = str(input("请输入控制模式：")) # 0为无信号，1为信号
    consider = str(input("请输入车辆模式："))
    model = AIM_problem(mode, consider)
    AIM_tolls.lp_model_analysis(model)
    AIM_tolls.store_result(test_name, test_num, mode, model, car, total_time)


if __name__ == "__main__":
    main()
