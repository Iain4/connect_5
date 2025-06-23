import numpy as np
from Base_Connectanator import Base_Connectanator

class Randomator(Base_Connectanator):
    def make_move(self)->int:
        while True:
            move = np.random.randint(0, self.slots)
            move = self.check_move(move)
            if move is not None:
                return move

        