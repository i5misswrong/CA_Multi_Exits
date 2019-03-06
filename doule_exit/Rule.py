import Data, DataCon


def PeopleMove(p, allPeople, direction):
    '''
    行人移动方法
    :param p: 单个行人
    :param direction: 移动方向
    :return: None
    '''
    flag = chickNextCanMove(p,allPeople,direction)
    if flag: # 如果下一点能移动
        if direction == 0:
            p.x = p.x - 1
            p.y = p.y + 1
        elif direction == 1:
            p.y = p.y + 1
        elif direction == 2:
            p.x = p.x + 1
            p.y = p.y + 1
        elif direction == 3:
            p.x = p.x - 1
        elif direction == 4:
            p.y = p.y
            p.x = p.x
        elif direction == 5:
            p.x = p.x + 1
        elif direction == 6:
            p.x = p.x - 1
            p.y = p.y - 1
        elif direction == 7:
            p.y = p.y - 1
        elif direction == 8:
            p.x = p.x + 1
            p.y = p.y - 1
    else:
        p.y = p.y
        p.x = p.x


def chickInExit(p, allPeople):
    '''
    检测行人是否到达出口
    :param p: 单个行人
    :param allPeople: 所有行人
    :return: None
    '''
    # if p.x >= Data.EXIT_X - Data.EXIT_WIGTH and p.x <= Data.EXIT_X + Data.EXIT_WIGTH and p.y == Data.ROOM_N:
    #     allPeople.remove(p)

    flag = False
    w = Data.EXIT_WIGTH / 2
    for i in p.exitNearList:
        e_x, e_y = DataCon.getExitPosition(i)
        if i == 0 or i == 1 or i == 2: # upper
            if p.x >= e_x - w and p.x <= e_x + w and p.y == Data.ROOM_M - 1:
                flag = True
        elif i == 3 or i == 4 or i == 5: # left
            if p.y >= e_y - w and p.y <= e_y + w and p.x == 1:
                flag = True
        elif i == 6 or i == 7 or i == 8: # right
            if p.y >= e_y - w and p.y <= e_y + w and p.x == Data.ROOM_M - 1:
                flag = True
        elif i == 9 or i == 10 or i == 11: # bottom
            if p.x >= e_x - w and p.x <= e_x + w and p.y == 1:
                flag = True
    if flag:
        allPeople.remove(p)
def chickNextCanMove(p,allPeople,direction):
    '''
    检查行人下一点能否移动
    :param p:
    :param allPeople:
    :param direction:
    :return:
    '''
    flag = True
    exit_flag = False
    n_x = p.x
    n_y = p.y
    if direction == 0:
        n_x = p.x - 1
        n_y = p.y + 1
    elif direction == 1:
        n_y = p.y + 1
    elif direction == 2:
        n_x = p.x + 1
        n_y = p.y + 1
    elif direction == 3:
        n_x = p.x - 1
    elif direction == 4:
        n_x = p.x
        n_y = p.y
    elif direction == 5:
        n_x = p.x + 1
    elif direction == 6:
        n_x = p.x - 1
        n_y = p.y - 1
    elif direction == 7:
        n_y = p.y - 1
    elif direction == 8:
        n_x = p.x + 1
        n_y = p.y - 1

    w = Data.EXIT_WIGTH / 2
    for i in p.exitNearList:
        e_x, e_y = DataCon.getExitPosition(i)
        if i == 0 or i == 1 or i == 2:  # upper
            if p.x >= e_x - w and p.x <= e_x + w and p.y == Data.ROOM_M - 1:
                exit_flag = True
        elif i == 3 or i == 4 or i == 5:  # left
            if p.y >= e_y - w and p.y <= e_y + w and p.x == 1:
                exit_flag = True
        elif i == 6 or i == 7 or i == 8:  # right
            if p.y >= e_y - w and p.y <= e_y + w and p.x == Data.ROOM_M - 1:
                exit_flag = True
        elif i == 9 or i == 10 or i == 11:  # bottom
            if p.x >= e_x - w and p.x <= e_x + w and p.y == 1:
                exit_flag = True
    if exit_flag:
        flag = True
    else:
        if n_x <= 0 or n_x >= Data.ROOM_M or n_y <= 0 or n_y >= Data.ROOM_N:
            flag = False
    for p_i in allPeople:
        if p_i.x == p.x and p_i.y ==p.y:
            pass
        else:
            if n_x == p_i.x and n_y == p_i.y:
                flag = False
    return flag
