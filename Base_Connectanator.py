import numpy as np

class Base_Connectanator():
    # this class does the gameplay rules
    def __init__(self, connect_num:int=4):
        self.connect_num = connect_num
        self.slots = 2 * connect_num -1
        self.rows = self.slots - 1
        self.moves = range(self.slots)
        self.players = ("Player 1", "Player 2") # ("Red", "Yellow")
        self.board = np.zeros((self.rows, self.slots), dtype=int)
        self.turn = 0


    def check_move(self, move, board=None):
        if board is None:
            board = self.board
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
        

    def place_counter(self, board, move, counter):
        col = self.board[:, move]
        for i, val in enumerate(col):
            if val != 0:
                placement = (i-1, move)
                break
            elif i == self.rows-1:
                placement = (i, move)

        board[placement] = counter
        return board, placement


    def find_connected(self, board, spot, counter):
        if board[spot] != counter:
            return [0,0,0,0]
        
        direcs = [(1,0), (0,1), (1,1), (-1,1)]
        signs = (1,-1)
        # connecteds is a list of the number of the same counters conected to the spot in the four directions:
        # column, row, downwards diag, upwards diag
        connecteds = []
        for d in direcs:
            connected = 0
            for sign in signs:
                test_spot = spot
                while True:
                    test_spot = (test_spot[0]+d[0]*sign, test_spot[1]+d[1]*sign)
                    try:
                        if test_spot[0] < 0 or test_spot[1] < 0:
                            break
                        elif board[test_spot] == counter:
                            connected += 1
                        else:
                             break
                    except IndexError:
                        break
            connecteds += [connected]
        return connecteds
                

    def win_check(self, board, spot):
        connecteds = self.find_connected(board, spot, self.get_player())
        if max(connecteds) >= self.connect_num-1:
            return True
        return False

    def get_player_name(self):
        return self.players[self.get_player()-1]
    
    def get_player(self):
        # done like this so it works for the bots which don't have a turn count
        tot = np.sum(self.board)
        if tot == 1:
            return 2
        return int(tot % 3) + 1
    
    def get_board(self):
        return self.board.copy()
    
    def set_board(self, board):
        self.board = board.copy()

    def make_move(self, board)->int:
        """To be implemented for any connect bots. The bot will get the current board from the Game_Happenator and can runs its logic off of that. The function should begin with a self.set_board(board).

        Parameters
        ----------
        board : numpy.ndarray
            The current connect-n board state.

        Returns
        -------
        int
            The move the bot wants to make. Need to be in range(self.slots).

        Raises
        ------
        NotImplementedError
            _description_
        """
        raise NotImplementedError("The make_move function has not been implemented in the current connect-x bot.")
        