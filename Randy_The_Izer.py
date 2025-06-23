import numpy as np
from Base_Connectanator import Base_Connectanator

class Randy_The_Izer(Base_Connectanator):
    def __init__(self, connect_num):
        super().__init__(connect_num=connect_num)


    def make_move(self, board)->int:
        self.set_board(board)

        while True:
            move = np.random.randint(0, self.slots)
            move = self.check_move(move)
            if move is not None:
                return move

        