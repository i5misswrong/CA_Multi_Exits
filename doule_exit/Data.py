FLAG = True
ROOM_M = 40 # 房间长度
ROOM_N = 40 # 房间高度
EXIT_X = 20 # 出口x坐标
EXIT_Y = 40 # 出口y坐标
EXIT_WIGTH = 6 # 出口宽度

PEOPLE_DENSITY = 0.1 # 行人密度
PEOPLE_NUMBER = int(ROOM_M * ROOM_N * PEOPLE_DENSITY) # 行人数量
# PEOPLE_NUMBER = 3
VISIBLE_R = 10 # 行人视野半径
INFORMATION_R = 20 # 信息传播范围
MEMORY_ANGLE = 30




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

EXIT_INDEX = getExitConfig(8) # 出口列表