import random
import numpy as np
import Data, Block
import matplotlib.pyplot as plt

def creatPeople():
    '''
    产生随机行人
    :return:行人列表
    '''
    allBlock = []  # 用于存放格子
    allPeople = []  # 用于存放行人
    '''将所有格子全部存入列表'''
    for i in range(1, Data.ROOM_M):
        for j in range(1, Data.ROOM_N):
            b = Block.Block()
            b.x = i
            b.y = j
            if random.random() > 0.5:
                b.clock_wise = True
            else:
                b.clock_wise = False
            # b.clock_wise = False
            b.income_inertia = np.zeros(9)
            b.income_wall = np.zeros(9)
            b.income_exit = np.zeros(9)
            b.income_all = np.zeros(9)
            allBlock.append(b)
    '''随机排序'''
    random.shuffle(allBlock)
    '''取前N个'''
    '''可有效防止无限产生随机数'''
    allPeople = allBlock[:Data.PEOPLE_NUMBER]
    return allPeople


def creatAppointPeo():
    '''
    产生指定行人
    :return: 行人列表
    '''
    allPeople = []
    b3 = Block.Block()
    b3.x = 30
    b3.y = 30
    b3.type = False
    b3.clock_wise = True
    b3.income_inertia = np.zeros(9)
    b3.income_wall = np.zeros(9)
    b3.income_exit = np.zeros(9)
    b3.income_all = np.zeros(9)
    allPeople.append(b3)



    return allPeople
