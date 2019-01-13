import Data

d_1_2 = Data.ROOM_M * 0.5
d_1_4 = Data.ROOM_M * 0.25
d_3_4 = Data.ROOM_M * 0.75
d_m = Data.ROOM_M
d_n = Data.ROOM_N

def getExitConfig(index):
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
        exits.append(([d_1_4, d_m], [d_3_4, d_m], [0, d_1_4], [0, d_3_4], [d_m, d_1_4], [d_m, d_3_4], [d_1_4, d_m],
                      [d_3_4, d_m]))

    return exits

# def case_0(exits):
#     exits.append(([d_1_2, d_m]))
#     pass
# def case_1(exits):
#     exits.append(([d_1_2,d_m],[d_1_2,0]))
#     pass
#
# def case_2(exits):
#     exits.append(([d_m,d_1_4],[d_m,d_3_4]))
#     pass
#
# def case_3(exits):
#     exits.append(([d_1_2,d_m],[d_1_2,0],[0,d_1_2]))
#     pass
#
# def case_4(exits):
#     exits.append(([0,d_1_2],[d_m,d_1_4],[d_m,d_3_4]))
#     pass
#
# def case_5(exits):
#     exits.append(([d_1_4,d_m],[d_m,d_1_4],[d_m,d_3_4]))
#     pass
#
# def case_6(exits):
#     exits.append(([d_1_2,d_m],[d_1_2,0],[0,d_1_2],[d_m,d_1_2]))
#     pass
#
# def case_7(exits):
#     exits.append(([0,d_1_4],[0,d_3_4],[d_m,d_1_4],[d_m,d_3_4]))
#     pass
#
# def case_8(exits):
#     exits.append(([d_1_4,d_m],[d_3_4,d_m],[0,d_1_4],[0,d_3_4],[d_m,d_1_4],[d_m,d_3_4],[d_1_4,d_m],[d_3_4,d_m]))
#     pass


