import Data


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
    if p.x >= Data.EXIT_X - Data.EXIT_WIGTH and p.x <= Data.EXIT_X + Data.EXIT_WIGTH and p.y == Data.ROOM_N:
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
    if n_x >= Data.EXIT_X - Data.EXIT_WIGTH and n_x <= Data.EXIT_X + Data.EXIT_WIGTH and n_y == Data.ROOM_N:
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