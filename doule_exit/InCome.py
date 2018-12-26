import math
import numpy as np
import Data, Rule


def addAllIncome(p, allPeople):
    '''
    计算总收益，，返回方向，runmain方法调用
    :param p:
    :param allPeople:
    :return: 行人移动最终方向
    '''
    p.income_inertia = np.zeros(9)
    p.income_wall = np.zeros(9)
    p.income_exit = np.zeros(9)
    p.income_all = np.zeros(9)
    countWallIncome(p)
    countDirection(p)
    countExitIncome(p)
    countDistenceWithExits(p)
    if p.isInExitNear:
        p.income_all = np.sum([p.income_exit, p.income_inertia], axis=0)
    else:
        if p.isInWallNear:
            p.income_all = np.sum([p.income_inertia, p.income_wall], axis=0)
        else:
            p.income_all = np.sum([p.income_inertia], axis=0)
    # direction = np.argmax(p.income_all)
    time_flag = 0

    while Rule.chickNextCanMove(p, allPeople, np.argmax(p.income_all)) != True:
        p.income_all[np.argmax(p.income_all)] = 0
        time_flag += 1
        if time_flag > 2:
            p.income_all[4] = 100

    return np.argmax(p.income_all)


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
# -----------------------------------墙壁收益---------------------------------------
def countWallIncome(p):
    '''
    计算行人墙壁收益相关：沿墙行走，沿墙转弯
    :param p:
    :return:
    '''
    p.income_wall = np.zeros(9)
    min_distence, min_distence_2 = countWhichWallNear(p)
    countWallTurn(p, min_distence)
    if p.isInWallNear_double:
        countWallCornerTurn(p, min_distence, min_distence_2)


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
            if old_direction == 0 or old_direction == 1 or old_direction == 2:
                p.income_wall[0] = 0.5 + np.random.random() * 0.01
                p.income_wall[1] = 0.5 + np.random.random() * 0.01
                p.income_wall[3] = 0.5 + np.random.random() * 0.1
        elif min_distence == 1:
            if old_direction == 6 or old_direction == 7 or old_direction == 8:
                p.income_wall[5] = 0.5 + np.random.random() * 0.1
                p.income_wall[7] = 0.5 + np.random.random() * 0.01
                p.income_wall[8] = 0.5 + np.random.random() * 0.01
        elif min_distence == 2:
            if old_direction == 0 or old_direction == 3 or old_direction == 6:
                p.income_wall[3] = 0.5 + np.random.random() * 0.01
                p.income_wall[6] = 0.5 + np.random.random() * 0.01
                p.income_wall[7] = 0.5 + np.random.random() * 0.1
        elif min_distence == 3:
            if old_direction == 2 or old_direction == 3 or old_direction == 4:
                p.income_wall[1] = 0.5 + np.random.random() * 0.1
                p.income_wall[2] = 0.5 + np.random.random() * 0.01
                p.income_wall[3] = 0.5 + np.random.random() * 0.01

    # turn right
    else:
        if min_distence == 0:
            if old_direction == 0 or old_direction == 1 or old_direction == 2:
                p.income_wall[1] = 0.5 + np.random.random() * 0.01
                p.income_wall[2] = 0.5 + np.random.random() * 0.01
                p.income_wall[5] = 0.5 + np.random.random() * 0.1
        elif min_distence == 1:
            if old_direction == 6 or old_direction == 7 or old_direction == 8:
                p.income_wall[3] = 0.5 + np.random.random() * 0.1
                p.income_wall[6] = 0.5 + np.random.random() * 0.01
                p.income_wall[7] = 0.5 + np.random.random() * 0.01
        elif min_distence == 2:
            if old_direction == 0 or old_direction == 3 or old_direction == 6:
                p.income_wall[0] = 0.5 + np.random.random() * 0.01
                p.income_wall[1] = 0.5 + np.random.random() * 0.1
                p.income_wall[3] = 0.5 + np.random.random() * 0.01
        elif min_distence == 3:
            if old_direction == 2 or old_direction == 3 or old_direction == 4:
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
                # p.income_wall[0] = 0.5 + np.random.random() * 0.01
                p.income_wall[1] = 0.5 + np.random.random() * 0.1
                p.income_wall[2] = 0.5 + np.random.random() * 0.01
                p.income_wall[5] = 0.5 + np.random.random() * 0.01
            elif (min_distence == 0 and min_distence_2 == 3) or (min_distence == 3 and min_distence_2 == 0):
                p.income_wall[0] = 0.5 + np.random.random() * 0.01
                p.income_wall[1] = 0.5 + np.random.random() * 0.01
                p.income_wall[3] = 0.5 + np.random.random() * 0.1
                # p.income_wall[6] = 0.5 + np.random.random() * 0.01
            elif (min_distence == 0 and min_distence_2 == 2) or (min_distence == 2 and min_distence_2 == 0):
                p.income_wall[3] = 0.5 + np.random.random() * 0.01
                p.income_wall[6] = 0.5 + np.random.random() * 0.01
                p.income_wall[7] = 0.5 + np.random.random() * 0.1
                # p.income_wall[8] = 0.5 + np.random.random() * 0.01
            elif (min_distence == 1 and min_distence_2 == 2) or (min_distence == 2 and min_distence_2 == 1):
                # p.income_wall[2] = 0.5 + np.random.random() * 0.01
                p.income_wall[5] = 0.5 + np.random.random() * 0.1
                p.income_wall[8] = 0.5 + np.random.random() * 0.01
                p.income_wall[7] = 0.5 + np.random.random() * 0.01
    # turn right
    else:
        if p.isInWallNear_double:
            if (min_distence == 1 and min_distence_2 == 3) or (min_distence == 3 and min_distence_2 == 1):
                # p.income_wall[0] = 0.5 + np.random.random() * 0.01
                p.income_wall[3] = 0.5 + np.random.random() * 0.1
                p.income_wall[6] = 0.5 + np.random.random() * 0.01
                p.income_wall[7] = 0.5 + np.random.random() * 0.01
            elif (min_distence == 0 and min_distence_2 == 3) or (min_distence == 3 and min_distence_2 == 0):
                p.income_wall[5] = 0.5 + np.random.random() * 0.01
                # p.income_wall[6] = 0.5 + np.random.random() * 0.01
                p.income_wall[7] = 0.5 + np.random.random() * 0.1
                p.income_wall[8] = 0.5 + np.random.random() * 0.01
            elif (min_distence == 0 and min_distence_2 == 2) or (min_distence == 2 and min_distence_2 == 0):
                p.income_wall[1] = 0.5 + np.random.random() * 0.01
                p.income_wall[2] = 0.5 + np.random.random() * 0.01
                p.income_wall[5] = 0.5 + np.random.random() * 0.1
                # p.income_wall[8] = 0.5 + np.random.random() * 0.01
            elif (min_distence == 1 and min_distence_2 == 2) or (min_distence == 2 and min_distence_2 == 1):
                p.income_wall[0] = 0.5 + np.random.random() * 0.01
                p.income_wall[1] = 0.5 + np.random.random() * 0.1
                # p.income_wall[2] = 0.5 + np.random.random() * 0.001
                p.income_wall[3] = 0.5 + np.random.random() * 0.01


# ---------------------------------------墙壁收益-结束------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ----------------------------------------出口收益----------------------------------
def countDistenceWithExits(p):
    '''
    计算行人离哪个出口近
    :param p:
    :return:
    '''
    d_1 = np.sqrt((p.x - Data.EXIT_X) ** 2 + (p.y - Data.EXIT_Y) ** 2)
    if d_1 < Data.VISIBLE_R:
        p.isInExitNear = True


def countExitIncome(p):
    '''
    计算行人的收益
    :param p: 单个行人
    :return: 方向 int
    '''
    around = getPedestrianAround(p)  # 计算行人周围坐标  返回一个列表 可以debug查看一下
    direction_income = []  # 行人收益存放列表
    dir_income = 0
    for i in around:  # 遍历around 需要循环2次  根据around结构具体调节循环次数 around在append时又新建了一个列表
        for j in i:
            try:  # 在程序终止时 除数为0  捕获异常 完成程序
                dir_income = (1 / math.sqrt((j[0] - 20) ** 2 + (j[1] - 40) ** 2)) * 10  # 计算行人周围8个位置到出口的距离 的倒数
            except:
                pass
            direction_income.append(dir_income)  # 将计算的收益添加到列表
    p.income_exit = direction_income[:]


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
