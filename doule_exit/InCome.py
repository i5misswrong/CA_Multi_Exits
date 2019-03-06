import math
import numpy as np
import Data, Rule, DataCon

# EXIT_INDEX = DataCon.getExitConfig(DataCon.exit_case)  # 出口列表
def addAllIncome(p, allPeople, e_index):
    '''
    计算总收益，，返回方向，runmain方法调用
    :param p:
    :param allPeople:
    :return: 行人移动最终方向
    '''
    # EXIT_INDEX = DataCon.getExitConfig(DataCon.exit_case)  # 出口列表
    # p.income_inertia = np.zeros(9)
    # p.income_wall = np.zeros(9)
    # p.income_exit = np.zeros(9)
    # p.income_memory = np.zeros(9)
    p.income_all = np.zeros(9)

    judgeCanGetInf(p, e_index)  # 判断行人是否位于获取信息范围内
    countDistenceWithExits(p, e_index)  # 判断你信任是否位于出口范围内
    countWhichWallNear(p)  # 判断行人是否位于墙壁附近
    judgePedStay(p)
    # if p.isStaty:
    countBlackIncome(p,allPeople)



    countDirection(p)  # 计算惯性收益
    if p.isInWallNear:
        countWallIncome(p)  # 计算墙壁收益
        # judgeClock(p)  # 计算行人的顺逆时针偏好方向
    if p.isInExitNear:
        countExitIncome(p)  # 计算出口收益
    if p.isInMemoryArea:
        countMemoryIncome(p)  # 计算记忆角收益
    judgeClock(p)


    if p.isInExitNear:  # 如果行人位于出口附近
        p.income_all = np.sum([p.income_exit], axis=0)
    elif p.isInWallNear:
        if p.isStaty:
            p.income_all = np.sum([p.income_memory, p.income_wall, p.income_inertia], axis=0)
        else:
            p.income_all = np.sum([p.income_inertia],axis=0)
    else:
        p.income_all = np.sum([p.income_memory, p.income_inertia],axis=0)
    # direction = np.argmax(p.income_all)
    time_flag = 0
    income = p.income_all
    while Rule.chickNextCanMove(p, allPeople, np.argmax(p.income_all)) != True:
        # p.income_all[np.argmax(p.income_all)] = 0
        income[np.argmax(p.income_all)] = 0
        time_flag += 1
        if time_flag > 9:
            return 4
        # if time_flag > 4:
        #     # p.income_all[4] = 100
        #     income[4] = 100

    # return np.argmax(p.income_all)
    return np.argmax(income)
    # if Rule.chickNextCanMove(p, allPeople, np.argmax(p.income_all)):
    #     return np.argmax(income)
    # else:
    #     return 4


# ---------------------------------------------------------------------------------
# -----------------------------------判断行人顺逆时针方向-----------------------------------
def judgeClock(p):
    income = np.zeros(9)
    income = np.sum([p.income_inertia, p.income_memory], axis=0)
    clock = True
    if p.clock_change_by_income < 10:
        if p.after_direction == 1:
            if np.argmax(income) in [0, 3, 7]:
                clock = False
            elif np.argmax(income) in [2, 5, 9]:
                clock = True
            else:
                clock = getRamdonSec()
        elif p.after_direction == 3:
            if np.argmax(income) in [7, 8, 9]:
                clock = False
            elif np.argmax(income) in [0, 1, 2]:
                clock = True
            else:
                clock = getRamdonSec()
        elif p.after_direction == 5:
            if np.argmax(income) in [0, 1, 2]:
                clock = False
            elif np.argmax(income) in [7, 8, 9]:
                clock = True
            else:
                clock = getRamdonSec()
        elif p.after_direction == 8:
            if np.argmax(income) in [2, 5, 9]:
                clock = False
            elif np.argmax(income) in [0, 3, 7]:
                clock = True
            else:
                clock = getRamdonSec()
        elif p.after_direction == 0:
            if np.argmax(income) in [3, 7, 8]:
                clock = False
            elif np.argmax(income) in [1, 2, 5]:
                clock = True
            else:
                clock = getRamdonSec()
        elif p.after_direction == 2:
            if np.argmax(income) in [0, 1, 3]:
                clock = False
            elif np.argmax(income) in [5, 8, 9]:
                clock = True
            else:
                clock = getRamdonSec()
        elif p.after_direction == 7:
            if np.argmax(income) in [5, 8, 9]:
                clock = False
            elif np.argmax(income) in [0, 1, 3]:
                clock = True
            else:
                clock = getRamdonSec()
        elif p.after_direction == 9:
            if np.argmax(income) in [1, 2, 5]:
                clock = False
            elif np.argmax(income) in [3, 7, 8]:
                clock = True
            else:
                clock = getRamdonSec()
        p.clock_wise = clock
        p.clock_change_by_income += 1
def getRamdonSec():
    flag = False
    if np.random.random() > 0.5:
        flag = True
    return flag
# ----------------------------------判断顺逆时针方向结束-----------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ---------------------------------------惯性收益-----------------------------------
def countDirection(p):
    '''
    惯性收益
        初始时刻，行人随机运动
        其他时刻，调用inertiaIncome 计算惯性收益具体指
    :param p:
    :return:
    '''
    if p.initial_flag:
        p.income_inertia = np.random.rand(9)
        # p.income_inertia[1] = 50
        # direction = randomDirection()
        p.initial_flag = False
    else:
        p.income_inertia = np.zeros(9)
        inertiaIncome(p)
    p.income_inertia = p.income_inertia * 0.1


def inertiaIncome(p):
    '''
    计算惯性收益：获取上一步方向
    :param p:
    :return:
    '''
    old_direction = p.after_direction
    p.income_inertia[old_direction] = 0.7 + np.random.random() * 0.01
    if old_direction == 0:
        p.income_inertia[1] = 0.3 + np.random.random() * 0.01
        p.income_inertia[3] = 0.3 + np.random.random() * 0.01
    elif old_direction == 1:
        p.income_inertia[0] = 0.3 + np.random.random() * 0.01
        p.income_inertia[2] = 0.3 + np.random.random() * 0.01
    elif old_direction == 2:
        p.income_inertia[1] = 0.3 + np.random.random() * 0.01
        p.income_inertia[5] = 0.3 + np.random.random() * 0.01
    elif old_direction == 3:
        p.income_inertia[0] = 0.3 + np.random.random() * 0.01
        p.income_inertia[6] = 0.3 + np.random.random() * 0.01
    elif old_direction == 4:
        for i in range(len(p.income_inertia)):
            p.income_inertia[i] = 0.1 + np.random.random() * 0.01
    elif old_direction == 5:
        p.income_inertia[2] = 0.3 + np.random.random() * 0.01
        p.income_inertia[8] = 0.3 + np.random.random() * 0.01
    elif old_direction == 6:
        p.income_inertia[3] = 0.3 + np.random.random() * 0.01
        p.income_inertia[7] = 0.3 + np.random.random() * 0.01
    elif old_direction == 7:
        p.income_inertia[6] = 0.3 + np.random.random() * 0.01
        p.income_inertia[8] = 0.3 + np.random.random() * 0.01
    elif old_direction == 8:
        p.income_inertia[5] = 0.3 + np.random.random() * 0.01
        p.income_inertia[7] = 0.3 + np.random.random() * 0.01


# ----------------------------------惯性收益-结束-----------------------------------
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# -----------------------------------空格收益---------------------------------------
def judgePedStay(p):
    if len(p.position_dic) < 1:
        pass
    else:
        after_x = p.position_dic[0][0]
        after_y = p.position_dic[0][1]
        if np.sqrt((after_x - p.x) ** 2 + (after_y - p.y) ** 2) < 2:
            p.isStaty = True

def countBlackIncome(p,allPeople):
    aroundPos = getPedestrianAround(p)
    block = 0
    block_income = []
    for peo in allPeople:
        if peo.x == p.x and peo.y == p.y:
            pass
        else:
            for j in aroundPos[0]:
                if j[0] == p.x and j[1] == p.y:
                    block = 0
                else:
                    block = 10
                block_income.append(block)  # 将计算的收益添加到列表
    p.block_income = block_income
# ----------------------------------空格收益-结束-----------------------------------
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
# -----------------------------------墙壁收益---------------------------------------
def countWallIncome(p):
    '''
    计算行人墙壁收益相关：沿墙行走，沿墙转弯
    :param p:
    :return:
    '''
    p.income_wall = np.zeros(9)
    min_distence, min_distence_2 = countWhichWallNear(p)
    if p.isInWallNear_double:
        countWallCornerTurn(p, min_distence, min_distence_2)
    else:
        countWallTurn(p, min_distence)


def countWhichWallNear(p):
    '''
    计算行人离那个墙壁最近
    :param p:
    :return: up:0 bottom:1 left:2 right:3
    '''
    # ------------- 计算行人离四周墙壁的距离--------
    d_top = np.abs(p.y - Data.ROOM_N)
    d_bottom = np.abs(p.y)
    d_left = np.abs(p.x)
    d_right = np.abs(p.x - Data.ROOM_M)
    # ----创建列表 计算列表中的最小值------------
    distence_wall = []
    distence_wall_copy = []
    distence_wall.append(d_top)
    distence_wall.append(d_bottom)
    distence_wall.append(d_left)
    distence_wall.append(d_right)

    distence_wall_copy = distence_wall[:]
    min_distence = np.argmin(distence_wall)
    distence_wall_copy[min_distence] = 50
    min_distence_double = np.argmin(distence_wall_copy)
    if distence_wall[min_distence] < Data.VISIBLE_R:  # 如果行人与墙壁距离小于R
        p.isInWallNear = True  # 将行人标记为 进入墙壁范围
        if distence_wall[min_distence_double] < Data.VISIBLE_R:
            p.isInWallNear_double = True
        else:
            p.isInWallNear_double = False
    else:
        p.isInWallNear = False
    return min_distence, min_distence_double


def countWallTurn(p, min_distence):
    '''
    计算行人沿着墙壁行走 的收益
    :param p:
    :param min_distence: 离那个墙壁最近 索引
    :return:
    '''
    old_direction = p.after_direction
    # turn left:
    if p.clock_wise:
        if min_distence == 0:
            # if old_direction == 0 or old_direction == 1 or old_direction == 2:
            p.income_wall[0] = 0.5 + np.random.random() * 0.01
            p.income_wall[1] = 0.5 + np.random.random() * 0.01
            p.income_wall[3] = 0.5 + np.random.random() * 0.1
        elif min_distence == 1:
            # if old_direction == 6 or old_direction == 7 or old_direction == 8:
            p.income_wall[5] = 0.5 + np.random.random() * 0.1
            p.income_wall[7] = 0.5 + np.random.random() * 0.01
            p.income_wall[8] = 0.5 + np.random.random() * 0.01
        elif min_distence == 2:
            # if old_direction == 0 or old_direction == 3 or old_direction == 6:
            p.income_wall[3] = 0.5 + np.random.random() * 0.01
            p.income_wall[6] = 0.5 + np.random.random() * 0.01
            p.income_wall[7] = 0.5 + np.random.random() * 0.1
        elif min_distence == 3:
            # if old_direction == 2 or old_direction == 3 or old_direction == 4:
            p.income_wall[1] = 0.5 + np.random.random() * 0.1
            p.income_wall[2] = 0.5 + np.random.random() * 0.01
            p.income_wall[3] = 0.5 + np.random.random() * 0.01

    # turn right
    else:
        if min_distence == 0:
            # if old_direction == 0 or old_direction == 1 or old_direction == 2:
            p.income_wall[1] = 0.5 + np.random.random() * 0.01
            p.income_wall[2] = 0.5 + np.random.random() * 0.01
            p.income_wall[5] = 0.5 + np.random.random() * 0.1
        elif min_distence == 1:
            # if old_direction == 6 or old_direction == 7 or old_direction == 8:
            p.income_wall[3] = 0.5 + np.random.random() * 0.1
            p.income_wall[6] = 0.5 + np.random.random() * 0.01
            p.income_wall[7] = 0.5 + np.random.random() * 0.01
        elif min_distence == 2:
            # if old_direction == 0 or old_direction == 3 or old_direction == 6:
            p.income_wall[0] = 0.5 + np.random.random() * 0.01
            p.income_wall[1] = 0.5 + np.random.random() * 0.1
            p.income_wall[3] = 0.5 + np.random.random() * 0.01
        elif min_distence == 3:
            # if old_direction == 2 or old_direction == 3 or old_direction == 4:
            p.income_wall[5] = 0.5 + np.random.random() * 0.01
            p.income_wall[7] = 0.5 + np.random.random() * 0.1
            p.income_wall[8] = 0.5 + np.random.random() * 0.01


def countWallCornerTurn(p, min_distence, min_distence_2):
    '''
    计算行人在沿着墙壁行走、转弯时候的方向
    :param p:
    :param min_distence: 距离行人最近的墙壁 索引
    :param min_distence_2: 距离行人第二近的墙壁 索引
    :return: null
    '''
    #  turn left
    if p.clock_wise:
        if p.isInWallNear_double:
            if (min_distence == 1 and min_distence_2 == 3) or (min_distence == 3 and min_distence_2 == 1):
                p.income_wall[0] = 0.5 + np.random.random() * 0.01
                p.income_wall[1] = 0.5 + np.random.random() * 0.1
                p.income_wall[2] = 0.5 + np.random.random() * 0.01
                p.income_wall[5] = 0.5 + np.random.random() * 0.01
            elif (min_distence == 0 and min_distence_2 == 3) or (min_distence == 3 and min_distence_2 == 0):
                p.income_wall[0] = 0.5 + np.random.random() * 0.01
                p.income_wall[1] = 0.5 + np.random.random() * 0.01
                p.income_wall[3] = 0.5 + np.random.random() * 0.1
                p.income_wall[6] = 0.5 + np.random.random() * 0.01
            elif (min_distence == 0 and min_distence_2 == 2) or (min_distence == 2 and min_distence_2 == 0):
                p.income_wall[3] = 0.5 + np.random.random() * 0.01
                p.income_wall[6] = 0.5 + np.random.random() * 0.01
                p.income_wall[7] = 0.5 + np.random.random() * 0.1
                p.income_wall[8] = 0.5 + np.random.random() * 0.01
            elif (min_distence == 1 and min_distence_2 == 2) or (min_distence == 2 and min_distence_2 == 1):
                p.income_wall[2] = 0.5 + np.random.random() * 0.01
                p.income_wall[5] = 0.5 + np.random.random() * 0.1
                p.income_wall[8] = 0.5 + np.random.random() * 0.01
                p.income_wall[7] = 0.5 + np.random.random() * 0.01
    # turn right
    else:
        if p.isInWallNear_double:
            if (min_distence == 1 and min_distence_2 == 3) or (min_distence == 3 and min_distence_2 == 1):
                p.income_wall[0] = 0.5 + np.random.random() * 0.01
                p.income_wall[3] = 0.5 + np.random.random() * 0.1
                p.income_wall[6] = 0.5 + np.random.random() * 0.01
                p.income_wall[7] = 0.5 + np.random.random() * 0.01
            elif (min_distence == 0 and min_distence_2 == 3) or (min_distence == 3 and min_distence_2 == 0):
                p.income_wall[5] = 0.5 + np.random.random() * 0.01
                p.income_wall[6] = 0.5 + np.random.random() * 0.01
                p.income_wall[7] = 0.5 + np.random.random() * 0.1
                p.income_wall[8] = 0.5 + np.random.random() * 0.01
            elif (min_distence == 0 and min_distence_2 == 2) or (min_distence == 2 and min_distence_2 == 0):
                p.income_wall[1] = 0.5 + np.random.random() * 0.01
                p.income_wall[2] = 0.5 + np.random.random() * 0.01
                p.income_wall[5] = 0.5 + np.random.random() * 0.1
                p.income_wall[8] = 0.5 + np.random.random() * 0.01
            elif (min_distence == 1 and min_distence_2 == 2) or (min_distence == 2 and min_distence_2 == 1):
                p.income_wall[0] = 0.5 + np.random.random() * 0.01
                p.income_wall[1] = 0.5 + np.random.random() * 0.1
                p.income_wall[2] = 0.5 + np.random.random() * 0.001
                p.income_wall[3] = 0.5 + np.random.random() * 0.01


# ---------------------------------------墙壁收益-结束------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ----------------------------------------出口收益----------------------------------
def countDistenceWithExits(p, e_index):
    '''
    计算行人离哪个出口近
    该方法在addallincome中引用 用于判断行人是否位于出口范围内
    :param p:
    :return:
    '''
    p.exitNearList = [] # 行人位于出口附近的列表 里面存放出口id 需要重置归零
    # exits = Data.EXIT_INDEX # 获取所有出口的xy坐标 ex ey
    exits = DataCon.getExitConfig(e_index)  # 出口列表
    for e in exits[0]: # e为[ex,ey]
        if type(e) == float or type(e) == int:
            d_e = np.sqrt((p.x - exits[0][0]) ** 2 + (p.y - exits[0][1]) ** 2)
        else:
            d_e = np.sqrt((p.x - e[0]) ** 2 + (p.y - e[1]) ** 2) # 计算当前出口与行人的距离
        # if d_e < Data.VISIBLE_R: # 如果位于视野范围内
        if d_e < Data.INFORMATION_R:  # 如果位于视野范围内
            if type(e) == float or type(e) == int:
                p.exitNearList.append(DataCon.getExitIndex(exits[0][0], exits[0][1]))
                pass
            else:
                p.exitNearList.append(DataCon.getExitIndex(e[0],e[1])) # 根据ex ey获取出口id 将出口id放入exitnearlist
    if len(p.exitNearList) > 0: # 当出口列表不为空时，表示行人位于某个出口内
        p.isInExitNear = True # 设置行人位于出口范围内

def countExitIncome(p):
    '''
    计算出口收益
    :param p:
    :return:
    '''
    around = getPedestrianAround(p)  # 计算行人周围坐标  返回一个列表 可以debug查看一下
    direction_income = []  # 行人收益存放列表
    dir_income = 0
    # if len(p.exitNearList) == 0: #如果行人不在出口范围内
    #     direction_income = np.zeros(9)
    #     pass
    # elif len(p.exitNearList) == 1: # 如果行人只能看到一个出口
    #     p.WhichExitNear = p.exitNearList[0]
    #     for i in around:  # 遍历around 需要循环2次  根据around结构具体调节循环次数 around在append时又新建了一个列表
    #         for j in i:
    #             try:  # 在程序终止时 除数为0  捕获异常 完成程序
    #                 dir_income = (1 / math.sqrt((j[0] - 20) ** 2 + (j[1] - 40) ** 2)) * 10  # 计算行人周围8个位置到出口的距离 的倒数
    #             except:
    #                 pass
    #             direction_income.append(dir_income)  # 将计算的收益添加到列表
    # else:
    #     exit_force_list = np.zeros(12) # 该列表表示 出口对行人的影响力 F/s 值越大 表示行人越会选择该出口 对应12个出口
    #     for i in p.exitNearList: # i为出口id
    #         e_x,e_y = Data.getExitPosition(i) # 根据出口id获取出口xy坐标 ex ey
    #         if np.sqrt((p.x - e_x) ** 2 + (p.y - e_y) ** 2) == 0:
    #             e_f = Data.EXIT_FORCE
    #         else:
    #             e_f = Data.EXIT_FORCE / np.sqrt((p.x - e_x) ** 2 + (p.y - e_y) ** 2)  # 计算F/S
    #         # try:
    #         #     e_f = Data.EXIT_FORCE / np.sqrt((p.x - e_x) ** 2 + (p.y - e_y) ** 2) # 计算F/S
    #         # except:
    #         #     pass
    #         exit_force_list[i] = e_f # 将出口影响力添加到列表
    #     exit_select = np.argmax(exit_force_list) # 获取出口影响力列表 的 最大值 的索引 即为行人最终选择的出口id
    #     p.WhichExitNear = exit_select
    #     ex,ey = Data.getExitPosition(exit_select) # 根据出口id获取出口xy坐标
    #     for i in around:  # 遍历around 需要循环2次  根据around结构具体调节循环次数 around在append时又新建了一个列表
    #         for j in i:
    #             try:  # 在程序终止时 除数为0  捕获异常 完成程序
    #                 dir_income = (1 / math.sqrt((j[0] - ex) ** 2 + (j[1] - ey) ** 2)) * 10  # 计算行人周围8个位置到出口的距离 的倒数
    #             except:
    #                 pass
    #             direction_income.append(dir_income)  # 将计算的收益添加到列表
    # p.income_exit = direction_income[:]

    ex, ey = DataCon.getExitPosition(p.WhichExitNear)
    for i in around:
        for j in i:
            try:
                dir_income = (1 / math.sqrt((j[0] - ex) ** 2 + (j[1] - ey) ** 2)) * 10  # 计算行人周围8个位置到出口的距离 的倒数
            except:
                pass
            direction_income.append(dir_income)
    p.income_exit = direction_income[:]

def countExitForce(p):

    pass
# def countExitIncome(p):
#     '''
#     计算行人的收益
#     :param p: 单个行人
#     :return: 方向 int
#     '''
#     around = getPedestrianAround(p)  # 计算行人周围坐标  返回一个列表 可以debug查看一下
#     direction_income = []  # 行人收益存放列表
#     dir_income = 0
#     for i in around:  # 遍历around 需要循环2次  根据around结构具体调节循环次数 around在append时又新建了一个列表
#         for j in i:
#             try:  # 在程序终止时 除数为0  捕获异常 完成程序
#                 dir_income = (1 / math.sqrt((j[0] - 20) ** 2 + (j[1] - 40) ** 2)) * 10  # 计算行人周围8个位置到出口的距离 的倒数
#             except:
#                 pass
#             direction_income.append(dir_income)  # 将计算的收益添加到列表
#     p.income_exit = direction_income[:]


def getPedestrianAround(p):
    '''
    获取行人周围8个点的坐标
    :param p: 单个行人
    :return: 返回值可以debug看一下结构
    '''
    around = []
    around.append(([p.x - 1, p.y + 1], [p.x, p.y + 1], [p.x + 1, p.y + 1], [p.x - 1, p.y], [p.x, p.y], [p.x + 1, p.y],
                   [p.x - 1, p.y - 1], [p.x, p.y - 1], [p.x + 1, p.y - 1]))
    return around



# ----------------------------------------出口收益-结束----------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ----------------------------------------记忆角收益----------------------------------
def judgeQuad(p):
    '''
    判断行人与出口位置 即出口位于行人的第几象限
    以行人为坐标原点
    :param p:
    :return: quad < 10 返回出口位于行人第几象限
             quad > 10 返回出口与行人成多少度（直角）
             quad = 360 = 0
    '''
    exit_index = p.whichExitNearInformation
    e_x, e_y = DataCon.getExitPosition(exit_index)  # 出口x
    # e_x = Data.EXIT_X  # 出口x
    # e_y = Data.EXIT_Y  # 出口y
    p_x = p.x  # 行人x
    p_y = p.y  # 行人y
    quad = 0  # 象限
    if e_y != p_y and e_x != p_x:  # 即行人位于象限内
        if e_y > p_y and e_x > p_x:  # 判断位置
            quad = 1
        elif e_y > p_y and e_x < p_x:
            quad = 2
        elif e_y < p_y and e_x < p_x:
            quad = 3
        elif e_y < p_y and e_x > p_x:
            quad = 4
    elif e_y == p_y and e_x == p_x:  # 即行人正好位于出口
        pass
    else:  # 行人位于坐标轴上
        if e_x == p_x:  # 出口位于x轴上
            if e_y > p_y:
                quad = 90
            else:
                quad = 270
        elif e_y == p_y:  # 出口位于y轴上
            if e_x > p_x:
                quad = 360
            else:
                quad = 180
    return quad


def countAngle(p):
    '''
    计算出口与行人所形成的角度
    :param p:
    :return: 角度
    '''
    exit_index = p.whichExitNearInformation
    e_x,e_y = DataCon.getExitPosition(exit_index)  # 出口x
    # e_x = Data.EXIT_X  # 出口x
    # e_y = Data.EXIT_Y  # 出口y
    p_x = p.x  # 行人x
    p_y = p.y  # 行人y
    try:
        ratio = np.abs(e_y - p_y) / (np.abs(e_x - p_x) + 0.1)  # 计算行人与出口所成角度的 tan
    except:
        print('divisor = 0')
    subAngle = np.degrees(np.arctan(ratio))  # 计算arctan 并返回以角度显示
    quad = judgeQuad(p)  # 判断角度所在象限
    angle = 0
    if quad < 10:  # 角度位于象限内
        if quad == 0:
            pass
        elif quad == 1:  # 第一象限
            angle = subAngle
        elif quad == 2:  # 第二象限
            angle = 180 - subAngle
        elif quad == 3:  # 第三象限
            angle = 180 + subAngle
        elif quad == 4:  # 第四象限
            angle = 360 - subAngle
    else:  # 位于坐标轴上
        if quad == 360:  # 360 = 0
            angle = 0
        else:
            angle = quad  # 等于指定坐标轴
    return angle  # 返回角度


def countMemoryAngle(p):
    '''
    计算所形成的记忆角的最小值和最大值
    :param p:
    :return: 最小记忆角 最大记忆角
    '''
    angle = countAngle(p)  # 获取出口与行人所形成的角度
    min_angle = angle - Data.MEMORY_ANGLE / 2  # 最小记忆角
    max_angle = angle + Data.MEMORY_ANGLE / 2  # 最大记忆角
    if min_angle < 0:  # 0与360处理
        min_angle = 360 + min_angle
    if max_angle > 360:
        max_angle = max_angle - 360
    # 正常结果 min_angle < max_angle
    # 在0°附近 可能 min_angle > max_angle
    return min_angle, max_angle


def countMemoryIncome(p):
    '''
    计算记忆角收益
    :param p:
    :return:
    '''
    # judgeCanGetInf(p)
    min_angle, max_angle = countMemoryAngle(p)  # 获取最小 最大记忆角
    standSec = [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5]  # 标准记忆角分割位置
    max_edge = 0  # 与最大记忆角相邻的分割位置
    min_edge = 0  # 与最小记忆角相邻的分割位置
    memoryIncome = np.zeros(9)  # 初始化记忆角收益
    #todo min=278 max=8
    # 不存在一个角使得standSec - max_angle < 45
    # 此处可以用指定max、min_edeg来表示
    if max_angle < min_angle:
        if judgeAngleArea(max_angle) == 5:
            max_edge = 337.5
    else:
        for i in standSec:  # max
            sub = i - max_angle
            if sub < 0:
                if np.abs(sub) / 45 < 1:
                    max_edge = i
    for j in standSec:  # min
        sub = min_angle - j
        if sub < 0:
            if np.abs(sub) / 45 < 1:
                min_edge = j
    if max_angle - min_angle > 0:
        if max_angle - min_angle < 45: # 如果记忆角之间没有横跨一个区间
            if judgeAngleArea(max_angle) == judgeAngleArea(min_angle):
                memoryIncome[judgeAngleArea(max_angle)] = (max_angle - min_angle) / 45
            else:
                memoryIncome[judgeAngleArea(max_angle)] = (max_angle - max_edge) / 45
                memoryIncome[judgeAngleArea(min_angle)] = (max_edge - min_angle) / 45
        elif (max_edge - min_edge) / 45 == 1:  # 如果记忆角之间隔了一个区间
            # memoryIncome[judgeAngleArea((max_edge + min_edge) / 2)] = 1  # 该区间收益值= 1
            memoryIncome[judgeAngleArea(max_angle)] = (max_angle - max_edge) / 45
            memoryIncome[judgeAngleArea(min_angle)] = (max_edge - min_angle) / 45
        elif (max_edge - min_edge) / 45 == 2:  # 如果记忆角之间隔了两个区间
            memoryIncome[judgeAngleArea(max_edge - 10)] = 1  # 该区间收益值 = 1
            memoryIncome[judgeAngleArea(min_edge + 10)] = 1
            memoryIncome[judgeAngleArea(max_angle)] = (max_angle - max_edge) / 45
            memoryIncome[judgeAngleArea(min_angle)] = (max_edge - min_angle) / 45
        elif (max_edge - min_edge) / 45 == 3:  # 如果记忆角之间隔了3个区间
            memoryIncome[judgeAngleArea(max_edge - 10)] = 1  # 相邻区间收益值 = 1
            memoryIncome[judgeAngleArea(min_edge + 10)] = 1
            memoryIncome[judgeAngleArea(((max_edge + min_edge) / 2))] = 1
            memoryIncome[judgeAngleArea(max_angle)] = (max_angle - max_edge) / 45
            memoryIncome[judgeAngleArea(min_angle)] = (max_edge - min_angle) / 45
    else:
        # if max_angle - min_angle < 45:  # 如果记忆角之间没有横跨一个区间
        #     if judgeAngleArea(max_angle) == judgeAngleArea(min_angle):
        #         memoryIncome[judgeAngleArea((max_angle + min_angle) / 2 + 180)] = (max_angle - min_angle + 360) / 45
        #     else:
        #         memoryIncome[judgeAngleArea(max_angle)] = (max_angle - max_edge) / 45
        #         memoryIncome[judgeAngleArea(min_angle)] = (max_edge - min_angle) / 45
        # -----------max_angle > min_angle 只在5方向中出现-------------------
        # -------------- 以下针对一些特殊案例做了处理---------------------
        if judgeAngleArea(max_angle) == judgeAngleArea(min_angle) == 5:
            if max_angle > 0 and min_angle > 337.5:
                memoryIncome[5] = (360 - min_angle + max_angle) / 45
        if judgeAngleArea(max_angle) == 2 and judgeAngleArea(min_angle) == 5:
            if min_angle > 337.5:
                memoryIncome[5] = (360 - min_angle + 22.5) / 45
                memoryIncome[2] = (max_angle - 22.5) / 45
        if judgeAngleArea(max_angle) == 5 and judgeAngleArea(min_angle) == 8:
            if max_angle < 22.5:
                memoryIncome[5] = (max_angle + 22.5) / 45
                memoryIncome[8] = (337.5 - min_angle) / 45
        if judgeAngleArea(max_angle) == 2 and judgeAngleArea(min_angle) == 8:
            memoryIncome[2] = (max_angle - 22.5) / 45
            memoryIncome[5] = 1
            memoryIncome[8] = (337.5 -min_angle) / 45
        if judgeAngleArea(max_angle) == 5 and judgeAngleArea(min_angle) == 7:
            memoryIncome[8] = 1
            if max_angle > 0:
                memoryIncome[5] = (max_angle + 22.5) / 45
            memoryIncome[7] = (292.5 - min_angle) / 45
        # if max_angle - min_angle < 45:  # 如果记忆角之间没有横跨一个区间
        #     # memoryIncome[max_angle] =
        #     if judgeAngleArea(max_angle) == judgeAngleArea(min_angle):
        #         memoryIncome[judgeAngleArea(max_angle)] = (360 - min_angle + max_angle) / 45
        #     if max_angle > 0 and max_angle < 22.5:
        #         pass
        # elif (max_edge - min_edge) / 45 == 3:  # 如果记忆角之间隔了3个区间
        #     memoryIncome[judgeAngleArea(max_edge - 10)] = 1  # 相邻区间收益值 = 1
        #     memoryIncome[judgeAngleArea(min_edge + 10)] = 1
        #     memoryIncome[judgeAngleArea(((max_edge + min_edge) / 2) + 180)] = 1

    if p.isInMemoryArea:  # 如果行人持续留在记忆角范围内
        p.income_memory = memoryIncome * 10  # 赋值
    # 该语句是为了行人离开记忆角范围后 记忆角收益能持续保留


def judgeAngleArea(angle):
    '''
    将记忆角与区间联系起来
    :param angle:
    :return: 返回记忆角所对应的区间
    '''
    area = 4  # 4位静止不同
    a = angle + np.random.uniform(-0.01, 0.01)  # 防止记忆角正好卡在区间边上
    if a > 112.5 and a < 157.5:
        area = 0
    elif a > 67.5 and a < 112.5:
        area = 1
    elif a > 22.5 and a < 67.5:
        area = 2
    elif a > 157.5 and a < 202.5:
        area = 3
    elif (a > 0 and a < 22.5) or (a > 337.5 and a < 360):
        area = 5
    elif a > 202.5 and a < 247.5:
        area = 6
    elif a > 247.5 and a < 292.5:
        area = 7
    elif a > 292.5 and a < 337.5:
        area = 8
    return area


def judgeCanGetInf(p, e_index):
    '''
    判断行人是否进入接受信息范围内
    :param p:
    :return:
    '''
    p.exitNearInformation = []
    # exits = Data.EXIT_INDEX
    exits = DataCon.getExitConfig(e_index)
    # e_x_0 = exits[0][0] - Data.EXIT_WIGTH / 2
    # e_x_1 = exits[0][0] - Data.EXIT_WIGTH / 2
    # exit_list.append(([e_x_0, exits[0][1]]))
    # exit_list.append(([e_x_1, exits[0][1]]))
    for e in exits[0]:
        if type(e) == float or type(e) == int:
            d_e = np.sqrt((p.x - exits[0][0]) ** 2 + (p.y - exits[0][1]) ** 2)
        else:
            d_e = np.sqrt((p.x - e[0]) ** 2 + (p.y - e[1]) ** 2)  # 计算当前出口与行人的距离
        if d_e < Data.INFORMATION_R:  # 如果位于视野范围内
            if type(e) == float or type(e) == int:
                p.exitNearInformation.append(DataCon.getExitIndex(exits[0][0], exits[0][1]))
            else:
                p.exitNearInformation.append(DataCon.getExitIndex(e[0], e[1]))  # 根据ex ey获取出口id 将出口id放入
            p.isInMemoryArea = True
    if len(p.exitNearInformation) == 0:
        pass
    elif len(p.exitNearInformation) == 1:
        p.whichExitNearInformation = p.exitNearInformation[0]
        p.WhichExitNear = p.whichExitNearInformation
    else:
        exit_force_list = np.zeros(12)
        for i in p.exitNearInformation:
            e_x, e_y = DataCon.getExitPosition(i)
            if np.sqrt((p.x - e_x) ** 2 + (p.y - e_y) ** 2) == 0:
                e_f = Data.EXIT_FORCE
            else:
                e_f = Data.EXIT_FORCE / np.sqrt((p.x - e_x) ** 2 + (p.y - e_y) ** 2)  # 计算F/S
            exit_force_list[i] = e_f
        exit_select = np.argmax(exit_force_list)
        p.whichExitNearInformation = exit_select
        p.WhichExitNear = exit_select
    # exit_index = p.WhichExitNear
    # e_x, e_y = Data.getExitPosition(exit_index)  # 出口x
    # if np.sqrt((p.x - e_x) ** 2 + (p.y - e_y) ** 2) < Data.INFORMATION_R:
    #     p.isInMemoryArea = True


# todo 记忆角收益中 让其他出口也发出疏散信息

# ----------------------------------------记忆角-结束----------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ----------------------------------------多出口影响力----------------------------------

# ----------------------------------------多出口影响力---------------------------------
# ---------------------------------------------------------------------------------
