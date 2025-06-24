from Base_Connectanator import Base_Connectanator
import numpy as np

class Blocky_Bob(Base_Connectanator):
    def __init__(self, connect_num):
        super().__init__(connect_num)

    def get_player(self):
        # faking that bob is the other player, so it will find their best move and play it instead
        return int(super().get_player() % 2) + 1
    
    def make_move(self, board):
        self.set_board(board)

        best_connecs = [0,0,0,0]
        best_move = None

        for i in range(self.slots):
            board = self.get_board()
            
            move = self.check_move(i)
            if move == None:
                continue
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