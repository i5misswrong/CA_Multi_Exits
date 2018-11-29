
class Block():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.type = True
        self.initial_flag = True
        self.after_direction = 5

        self.clock_wise = True # True=clockwise  False=counterclockwise


        self.isInWallNear = False
        self.isInWallNear_double = False

        self.isInExitNear = False
        self.WhichExitNear = 0

        self.income_inertia = 0
        self.income_wall = 0
        self.income_exit = 0
        self.income_all = 0