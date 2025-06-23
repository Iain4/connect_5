import numpy as np

class Base_Connectanator():
    def __init__(self, connect_num:int=4):
        self.connect_num = connect_num
        self.slots = 2 * connect_num -1
        self.rows = self.slots - 1
        self.moves = range(self.slots)
        self.players = ("Player 1", "Player 2") # ("Red", "Yellow")
        self.board = np.zeros((self.rows, self.slots), dtype=int)
        self.turn = 0

    def check_move(self, move):
        if move is None:
            return None
        try: 
            move = int(move)

            if move not in self.moves:
                return None
            elif self.board[0, move] != 0:
                return None
            else: 
                return move
            
        except ValueError:
            return None
        


    def place_counter(self):
        col = self.board[:, self.move]
        for i, val in enumerate(col):
            if val != 0:
                placement = (i-1, self.move)
                break
            elif i == self.rows-1:
                placement = (i, self.move)

        self.board[placement] = self.get_player()
        return placement


    def game_turn(self, players_move=None):
        move = self.check_move(players_move)
        
        if move == None:
            return False, self.get_player()
        
        self.set_move(move)
        placement = self.place_counter()
        winner = self.any_winners(placement)
        if not winner:
            self.turn += 1
        return winner, self.get_player()
        

    def any_winners(self, placement):
        # think there might be a better way to return the value of this 
        # and defo need to rewite the detection cause 'tis fugly
        o = self.get_player()
        row, col = placement

        # checking rows
        connected = 0
        for i in range(self.rows):
            if self.board[i, col] == o:
                connected += 1
                if connected == self.connect_num:
                    return True
            else: 
                connected = 0

        # checking cols
        connected = 0
        for i in range(self.slots):
            if self.board[row, i] == o:
                connected += 1
                if connected == self.connect_num:
                    return True
            else: 
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
                if connected == self.connect_num:
                    return True
            else:
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
                if connected == self.connect_num:
                    return True
            else:
                connected = 0

            r -= 1; c += 1
            if r == -1 or c == self.slots:
                break
        return False

    def get_player_name(self):
        return self.players[self.get_player()-1]
    
    def get_turn(self):
        return self.turn
    
    def get_player(self):
        return self.turn % 2 + 1
    
    def get_board(self):
        return self.board
    
    def set_move(self, move):
        self.move = move