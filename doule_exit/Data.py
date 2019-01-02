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
MEMORY_ANGLE = 30