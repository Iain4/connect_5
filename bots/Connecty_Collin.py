from Base_Connectanator import Base_Connectanator
import numpy as np

class Connecty_Collin(Base_Connectanator):
    def __init__(self, connect_num):
        super().__init__(connect_num=connect_num)
        self.player_num = None

    def make_move(self, board)->int:
        self.set_board(board.copy())
        print(self.board, self.get_player()) 
        
        self.player_num = self.get_player()
    
    
        longest_connected = 0
        best_spot = None

        for i in range(self.slots):
            self.set_board(board.copy())

            
            move = self.check_move(i)
            if move == None:
                continue
            
            move = self.place_counter(move)
            val = self.num_connected(move)
            print(self.board) 
            print(f"for i={i} max_connected={val}")
            # if val == True: # will make any instantly winning moves
            #     print(f'winning move in slot {i}')
            #     return i

            if val > longest_connected:
                longest_connected = val
                best_spot = i

        if best_spot == None:
            best_spot = np.random.randint(0, self.slots)
        
        print(f"connected {longest_connected}, move {best_spot}")
        return int(best_spot)
    

    def num_connected(self, move):
        # slightly modded any_winners func
        o = self.player_num
        row, col = move

        max_connected = 0
        # checking rows
        connected = 0
        for i in range(self.rows):
            if self.board[i, col] == o:
                connected += 1
            else: 
                if connected > max_connected:
                    max_connected = connected
                connected = 0

        # checking cols
        connected = 0
        for i in range(self.slots):
            if self.board[row, i] == o:
                connected += 1
            else: 
                if connected > max_connected:
                    max_connected = connected
                connected = 0

        # checking down-sloppiong diagonal
        connected = 0
        if col > row:
            c = col - row
            r = 0
        else:
            r = row - col
            c = 0
        for i in range(self.rows):
            if self.board[r, c] == o:
                connected += 1
            else:
                if connected > max_connected:
                    max_connected = connected
                connected = 0

            r += 1; c += 1
            if r == self.rows or c == self.slots:
                break

        # checking upwards diagonals 
        connected = 0
        R = self.rows - 1
        if col + row > R:
            r = R
            c = col - (R - row)
        else:
            c = 0
            r = row + col
        for i in range(self.rows):
            if self.board[r, c] == o:
                connected += 1
            else:
                if connected > max_connected:
                    max_connected = connected
                connected = 0

            r -= 1; c += 1
            if r == -1 or c == self.slots:
                break

        return max_connected