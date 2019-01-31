FLAG = True
ROOM_M = 40 # 房间长度
ROOM_N = 40 # 房间高度
EXIT_X = 20 # 出口x坐标
EXIT_Y = 40 # 出口y坐标
EXIT_WIGTH = 6 # 出口宽度
EXIT_CASE = 4

PEOPLE_DENSITY = 0.01 # 行人密度
PEOPLE_NUMBER = int(ROOM_M * ROOM_N * PEOPLE_DENSITY) # 行人数量
print(PEOPLE_NUMBER)
# PEOPLE_NUMBER = 3
VISIBLE_R = 100 # 行人视野半径
INFORMATION_R = 100 # 信息传播范围
MEMORY_ANGLE = 30

EXIT_FORCE = 10




def getExitConfig(index):
    d_1_2 = ROOM_M * 0.5
    d_1_4 = ROOM_M * 0.25
    d_3_4 = ROOM_M * 0.75
    d_m = ROOM_M
    d_n = ROOM_N
    exits = []
    if index == 0:
        exits.append(([d_1_2, d_m]))
    elif index == 1:
        exits.append(([d_1_2, d_m], [d_1_2, 0]))
    elif index == 2:
        exits.append(([d_m, d_1_4], [d_m, d_3_4]))
    elif index == 3:
        exits.append(([d_1_2, d_m], [d_1_2, 0], [0, d_1_2]))
    elif index == 4:
        exits.append(([0, d_1_2], [d_m, d_1_4], [d_m, d_3_4]))
    elif index == 5:
        exits.append(([d_1_4, d_m], [d_m, d_1_4], [d_m, d_3_4]))
    elif index == 6:
        exits.append(([d_1_2, d_m], [d_1_2, 0], [0, d_1_2], [d_m, d_1_2]))
    elif index == 7:
        exits.append(([0, d_1_4], [0, d_3_4], [d_m, d_1_4], [d_m, d_3_4]))
    elif index == 8:
        exits.append(([d_1_4, d_m], [d_3_4, d_m], [0, d_1_4], [0, d_3_4], [d_m, d_1_4], [d_m, d_3_4], [d_1_4, 0],
                      [d_3_4, 0]))
    return exits
def getExitIndex(e_x,e_y):
    d_1_2 = ROOM_M * 0.5
    d_1_4 = ROOM_M * 0.25
    d_3_4 = ROOM_M * 0.75
    d_m = ROOM_M
    d_n = ROOM_N
    exit_index = 0
    if e_y == d_m:
        if e_x == d_1_4:
            exit_index = 0
        elif e_x == d_1_2:
            exit_index = 1
        elif e_x == d_3_4:
            exit_index = 2
    if e_y == 0:
        if e_x == d_1_4:
            exit_index = 9
        elif e_x == d_1_2:
            exit_index = 10
        elif e_x == d_3_4:
            exit_index = 11
    if e_x == 0:
        if e_y == d_3_4:
            exit_index = 3
        elif e_y == d_1_2:
            exit_index = 4
        elif e_y == d_1_4:
            exit_index = 5
    if e_x == d_m:
        if e_y == d_3_4:
            exit_index = 6
        elif e_y == d_1_2:
            exit_index = 7
        elif e_y == d_1_4:
            exit_index = 8

    return exit_index
def getExitPosition(index):
    d_1_2 = ROOM_M * 0.5
    d_1_4 = ROOM_M * 0.25
    d_3_4 = ROOM_M * 0.75
    d_m = ROOM_M
    d_n = ROOM_N
    e_x = 0
    e_y = 0
    if index == 0:
        e_x = d_1_4
        e_y = d_m
    elif index == 1:
        e_x = d_1_2
        e_y = d_m
    elif index == 2:
        e_x = d_3_4
        e_y = d_m
    elif index == 3:
        e_x = 0
        e_y = d_3_4
    elif index == 4:
        e_x = 0
        e_y = d_1_2
    elif index == 5:
        e_x = 0
        e_y = d_1_4
    elif index == 6:
        e_x = d_m
        e_y = d_3_4
    elif index == 7:
        e_x = d_m
        e_y = d_1_2
    elif index == 8:
        e_x = d_m
        e_y = d_1_4
    elif index == 9:
        e_x = d_1_4
        e_y = 0
    elif index == 10:
        e_x = d_1_2
        e_y = 0
    elif index == 11:
        e_x = d_3_4
        e_y = 0
    return e_x,e_y

EXIT_INDEX = getExitConfig(EXIT_CASE) # 出口列表