import time
import numpy as np
import tqdm
import pymysql
import matplotlib.pyplot as plt
import DrawFirst,Block,InCome,Rule,InitialPedestrian, Data, DataCon

def run_view():
    e_index = 5
    Data.PEOPLE_DENSITY = 0.4
    Data.PEOPLE_NUMBER = int(Data.ROOM_M * Data.ROOM_N * Data.PEOPLE_DENSITY)
    Data.VISIBLE_R = 3
    Data.INFORMATION_R = 11
    Data.EXIT_WIGTH = 6
    Data.MEMORY_ANGLE = 90
    plt.figure(figsize=(6, 6))
    evacuation_time = 0  # 疏散时间步 计时器
    time_after_step = -5 # 获取行人前5个时间步的方向
    allPeople = InitialPedestrian.creatPeople()
    # allPeople = InitialPedestrian.creatAppointPeo()  # 初始化行人--初始化指定行人 便于调试
    DrawFirst.draw_main(allPeople, e_index)  # 绘制行人和地图
    while Data.FLAG:  # 循环标识符
        for p in allPeople:  # 遍历每个行人
            Rule.chickInExit(p,allPeople)
            direcetion = InCome.addAllIncome(p,allPeople, e_index)  # 计算每个行人的移动方向
            p.after_direction = direcetion
            Rule.PeopleMove(p, allPeople, direcetion)  # 行人移动
            p.position_dic.append([p.x, p.y])  # 将行人所有位置存入列表
            if time_after_step > 0:
                p.position_dic.pop(0)
        DrawFirst.draw_main(allPeople, e_index)  # 更新图像

        '''程序终止检测'''
        if len(allPeople) < Data.PEOPLE_NUMBER * 0.05:  # 如果行人都出去了
            Data.FLAG = False  # 更改循环标识符
        # if evacuation_time > 0:
        #     # Data.FLAG = False
        #     time.sleep(100)
        evacuation_time += 1  # 疏散时间步 计时器+1
        time_after_step += 1
        if evacuation_time == 8:
            plt.savefig('flag.eps')
        print('当前时间步:', evacuation_time, '剩余行人', len(allPeople))  # 输出信息
    # plt.close()
    print(evacuation_time)

def run_insert(l_c, l_d, l_r_v, l_r_i, l_w, l_a):
    Data.FLAG = True
    e_index = l_c

    Data.PEOPLE_DENSITY = l_d
    Data.PEOPLE_NUMBER = int(Data.ROOM_M * Data.ROOM_N * l_d)

    Data.VISIBLE_R = l_r_v
    Data.INFORMATION_R = l_r_i

    Data.EXIT_WIGTH = l_w

    Data.MEMORY_ANGLE = l_a

    evacuation_time = 0  # 疏散时间步 计时器
    time_after_step = -5 # 获取行人前5个时间步的方向
    allPeople = InitialPedestrian.creatPeople()
    while Data.FLAG:  # 循环标识符
        for p in allPeople:  # 遍历每个行人
            Rule.chickInExit(p,allPeople)
            direcetion = InCome.addAllIncome(p,allPeople, e_index)  # 计算每个行人的移动方向
            p.after_direction = direcetion
            Rule.PeopleMove(p, allPeople, direcetion)  # 行人移动
            p.position_dic.append([p.x, p.y])  # 将行人所有位置存入列表
            if time_after_step > 0:
                p.position_dic.pop(0)
        '''程序终止检测'''
        if len(allPeople) < Data.PEOPLE_NUMBER * 0.05:  # 如果行人都出去了
            Data.FLAG = False  # 更改循环标识符
        evacuation_time += 1  # 疏散时间步 计时器+1
        time_after_step += 1
        # print('当前时间步:', evacuation_time, '剩余行人', len(allPeople))  # 输出信息
    return evacuation_time

def insert_db():
    connect = pymysql.connect(host='localhost', user = 'root', password = '334455', db = 'multi_exit')

    list_case = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # list_density = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
    list_density = [0.4]

    # list_r_vision = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    list_r_vision = [3]

    list_r_information = [6]
    # list_r_information = [20, 30]

    # list_width = [3, 4, 5, 6, 7, 8]
    list_width = [6]

    list_angle = [0,30,60,120,150,180]
    # list_angle = [90]

    list_steps = range(3)
    # list_case = [0, 1]
    # list_density = [0.1]
    # list_r_vision = [5, 10]
    # list_r_information = [20, 30]
    # list_width = [6]
    # list_angle = [90]
    # list_steps = range(2)
    try:
        with connect.cursor() as cursor:
            total_list = len(list_case) * len(list_density) * len(list_r_vision) * len(list_r_information) * len(list_width) * len(list_angle) * len(list_steps)
            with tqdm.tqdm(total=total_list) as pbar:
                for l_c in list_case:
                    for l_d in list_density:
                        for l_r_v in list_r_vision:
                            for l_r_i in list_r_information:
                                for l_w in list_width:
                                    for l_a in list_angle:
                                        for l_s in list_steps:
                                            if l_r_v > l_r_i:
                                                pass
                                            else:
                                                evacuation_time = run_insert(l_c, l_d, l_r_v, l_r_i, l_w, l_a)
                                                sql = "insert into multi_exit.test (exit_case, exit_width, exit_force, density, v_vision, v_information, memory_angle, steps, times) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                                cursor.execute(sql,[l_c, l_w, 10, l_d, l_r_v, l_r_i, l_a, l_s, evacuation_time])
                                                connect.commit()
                                                print('case=', l_c, '---density=', l_d, '---r_vision=', l_r_v, '---r_information=', l_r_i, '---width=', l_w, '---angle=', l_a, '---steps=', l_s, '---times=', evacuation_time)
                                                pbar.update(1)
    finally:
        connect.close()

if __name__ == '__main__':
    '''程序入口方法'''
    run_view()
    # insert_db()
