import numpy as np
import matplotlib.pyplot as plt
import DrawFirst,Block,InCome,Rule,InitialPedestrian, Data

def run_view():
    plt.figure(figsize=(6, 6))
    evacuation_time = 0  # 疏散时间步 计时器
    time_after_step = -5 # 获取行人前5个时间步的方向
    allPeople = InitialPedestrian.creatPeople()
    # allPeople = InitialPedestrian.creatAppointPeo()  # 初始化行人--初始化指定行人 便于调试
    DrawFirst.draw_main(allPeople)  # 绘制行人和地图
    while Data.FLAG:  # 循环标识符
        for p in allPeople:  # 遍历每个行人
            Rule.chickInExit(p,allPeople)
            direcetion = InCome.addAllIncome(p,allPeople)  # 计算每个行人的移动方向
            p.after_direction = direcetion

            Rule.PeopleMove(p, allPeople, direcetion)  # 行人移动
            p.position_dic.append([p.x, p.y])  # 将行人所有位置存入列表
            if time_after_step > 0:
                p.position_dic.pop(0)
        DrawFirst.draw_main(allPeople)  # 更新图像

        '''程序终止检测'''
        if len(allPeople) == 0:  # 如果行人都出去了
            Data.FLAG = False  # 更改循环标识符
        # if evacuation_time > 5:
        #     Data.FLAG = False
        evacuation_time += 1  # 疏散时间步 计时器+1
        time_after_step += 1
        # print('当前时间步:', evacuation_time)  # 输出信息
    # plt.close()
    print(evacuation_time)

if __name__ == '__main__':
    '''程序入口方法'''
    run_view()
