from Base_Connectanator import Base_Connectanator
import numpy as np

class Connecty_Collin(Base_Connectanator):
    def __init__(self, connect_num):
        super().__init__(connect_num=connect_num)
        self.player_num = None

    def make_move(self, board)->int:
        self.set_board(board)
        best_connecs = [0,0,0,0]
        best_move = None

        for i in range(self.slots):
            board = self.get_board()
            
            board, spot = self.place_counter(board, i)
            connecs = self.find_connected(board, spot)
            
            for n,m in zip(sorted(connecs, reverse=True), sorted(best_connecs, reverse=True)):
                if n > m:
                    best_connecs = connecs
                    best_move = i
                elif n == m:
                    continue
                else:
                    break
        
        if best_move == None:
            best_move = np.random.randint(0, self.slots)
        return best_move