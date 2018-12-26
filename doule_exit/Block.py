
class Block():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.initial_flag = True # 行人是否初始移动
        self.after_direction = 5 # 行人上一步移动方向

        self.clock_wise = True # 行人转向偏好 True=clockwise  False=counterclockwise


        self.isInWallNear = False # 行人是否在墙壁附近
        self.isInWallNear_double = False # 行人是否位于墙壁拐角

        self.isInExitNear = False # 行人是否位于出口附近
        self.WhichExitNear = 0 # 行人位于哪个出口附近

        self.income_inertia = 0 # 惯性收益
        self.income_wall = 0 # 墙壁收益
        self.income_exit = 0 # 出口收益
        self.income_all = 0 # 总收益