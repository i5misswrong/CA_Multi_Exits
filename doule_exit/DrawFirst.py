import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import Data, Block, InitialPedestrian, DataCon

# EXIT_INDEX = DataCon.getExitConfig(DataCon.exit_case)  # 出口列表

room_m = Data.ROOM_M
room_n = Data.ROOM_N
exit_width = Data.EXIT_WIGTH
exit_center = 20
people_number = Data.PEOPLE_NUMBER
# exits = Data.EXIT_INDEX
# exits = EXIT_INDEX
def draw_main(Peoples, e_index):
    plt.clf()
    draw_boundary()
    draw_wall()
    draw_exit(e_index)
    # draw_pedestrian()
    drawPeople(Peoples)
    if Data.FLAG == False:
        plt.close()
    else:
        plt.pause(0.2)


def count_exit_axis_horizontal():
    e_x_1 = exit_center - exit_width / 2
    e_x_2 = exit_center + exit_width / 2
    e_y = room_n
    x_list = []
    x_list.append(e_x_1)
    x_list.append(e_x_2)
    y_list = []
    y_list.append(e_y)
    y_list.append(e_y)
    result = []
    result.append(x_list)
    result.append(y_list)
    return result


def draw_wall():
    exit_axis = count_exit_axis_horizontal()
    plt.plot([0, room_m], [0, 0], 'k-')  # bottom,
    plt.plot([0,room_m],[room_m,room_m],'k-')
    # plt.plot([0, exit_axis[0][0]], [room_n, room_n], 'k-')  # upper left
    # plt.plot([exit_axis[0][1], room_m], [room_n, room_n], 'k-')  # upper right
    plt.plot([0, 0], [0, room_n], 'k-')  # left
    plt.plot([room_m, room_m], [0, room_n], 'k-')  # right

    # plt.plot([exit_center - exit_width / 2, exit_center + exit_width / 2], [room_n, room_n])
    # plt.plot([exit_axis[0][0], exit_axis[0][1]], [exit_axis[1][0], exit_axis[1][1]], 'g-', linewidth=6)
    # plt.plot([exit_axis[0][0], exit_axis[0][1]], [exit_axis[1][0], exit_axis[1][1]], 'w-',linewidth=0.1)
    # plt.Rectangle((room_m - exit_width, room_n),exit_width * 2,3)


def draw_boundary():
    '''
    绘制外框，如果不加框，行人从出口出去会造成图像震荡
    框距离墙壁为 3
    :return:
    '''
    plt.plot([-3, room_m + 3], [-3, -3], 'k-')  # bottom
    plt.plot([-3, -3], [-3, room_n + 3], 'k-')  # left
    plt.plot([room_m + 3, room_m + 3], [-3, room_n + 3], 'k-')  # right
    plt.plot([-3, room_m + 3], [room_n + 3, room_n + 3], 'k-')  # upper


def draw_exit(e_index):
    EXIT_INDEX = DataCon.getExitConfig(e_index)  # 出口列表
    exits = EXIT_INDEX
    if len(exits[0]) == 1:
        print(exits[0][0])
        plt.plot([exits[0][0] - Data.EXIT_WIGTH/2,exits[0][0] + Data.EXIT_WIGTH/2],[exits[0][1],exits[0][1]],'w-',linewidth = 2)
    else:

        for e in exits[0]:
            exit_list = []
            if type(e) == float or type(e) == int:
                e_x_0 = exits[0][0] - Data.EXIT_WIGTH / 2
                e_x_1 = exits[0][0] + Data.EXIT_WIGTH / 2
                exit_list.append(([e_x_0,exits[0][1]]))
                exit_list.append(([e_x_1,exits[0][1]]))
            else:
                if int(e[0]) != 0 and e[0] != Data.ROOM_M:
                    e_x_0 = e[0] - Data.EXIT_WIGTH / 2
                    e_x_1 = e[0] + Data.EXIT_WIGTH / 2
                    exit_list.append(([e_x_0,e[1]]))
                    exit_list.append(([e_x_1,e[1]]))
                if e[1] != 0.0 and e[1] != Data.ROOM_M:
                    e_y_0 = e[1] - Data.EXIT_WIGTH / 2
                    e_y_1 = e[1] + Data.EXIT_WIGTH / 2
                    exit_list.append(([e[0],e_y_0]))
                    exit_list.append(([e[0],e_y_1]))

            plt.plot([exit_list[0][0],exit_list[1][0]],[exit_list[0][1],exit_list[1][1]],'w-',linewidth=6)

def draw_pedestrian():
    pass


def drawPeople(P):
    # plt.clf()  # 清除数据
    P_x_clock = []  # 存放所有行人x坐标
    P_y_clock = []  # 存放所有行人y坐标
    P_x_clock_conter = []
    P_y_clock_conter = []
    for p in P:  # 遍历行人
        if p.clock_wise:
            P_x_clock.append(p.x)  # 分别添加坐标
            P_y_clock.append(p.y)
        else:
            P_x_clock_conter.append(p.x)
            P_y_clock_conter.append(p.y)
    plt.scatter(P_x_clock, P_y_clock, c='r', marker='o')  # 顺时针行人
    plt.scatter(P_x_clock_conter, P_y_clock_conter, c='b', marker='o') # 逆时针行人
    '''由于无法右上角关闭 加了个关闭按钮'''
    closeFig = plt.axes([0.8, 0.025, 0.1, 0.04])  # 关闭按钮
    closeFigbutton = Button(closeFig, 'close', hovercolor='0.5')  # 按钮样式
    closeFigbutton.on_clicked(closeFigure)  # 按钮按下去的动作

    # plt.savefig("%d.png" %step) #保存图片用
    # while Data.pause_flag:
    #     plt.pause(1)  # 暂停1s
    # plt.pause(0.3)  # 暂停1s


def closeFigure(event):
    print('onclick')
    plt.close()
    Data.FLAG = False


if __name__ == '__main__':
    draw_main()
