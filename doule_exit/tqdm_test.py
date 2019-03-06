# from tqdm import tqdm
import tqdm
import time
#
# text = ""
# for char in tqdm(["a", "b", "c", "d"]):
#     time.sleep(0.25)
#     text = text + char


list_case = [0, 1, 2, 3, 4, 5, 6, 7, 8]
list_density = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
# list_density = [0.1]
list_r_vision = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
list_r_information = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
list_width = [3, 4, 5, 6, 7, 8]
list_angle = [0, 30, 60, 90, 120, 150, 180]
list_steps = range(10)
text = ''
i=0
# for l_c in tqdm.trange(100):
#     for l_d in list_density:
#         for l_r in list_r_vision:
#             i += 1
#             # print(i)
#             time.sleep(0.1)
with tqdm.tqdm(total=(len(list_case) * len(list_density))) as pbar:
    for l_c in list_case:
        for l_d in list_density:
            time.sleep(0.1)
            i += 1
            # print(i)
            tqdm.tqdm.write(str(i))

            pbar.update(1)
#
# for l_d in tqdm(range(300)):
#     # for lr in tqdm(list_r_vision):
#     # i += 1
#     # tqdm.write(text + str(l_d))
#     tqdm.write( 's', file=None, end='\n', nolock=False)
#     time.sleep(0.01)


        # text = text+str(l_d)
# for l_c in list_case:
#     for l_d in list_density:
#         for l_r_v in list_r_vision:
#             for l_r_i in list_r_information:
#                 for l_w in list_width:
#                     for l_a in list_angle:
#                         for l_s in list_steps: