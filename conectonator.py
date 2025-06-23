class connectanator:
    def __init__(self, connect_num:int=4):
        self.connect_num = connect_num
        self.slots = 2 * connect_num -1
        self.rows = self.slots - 1
        self.moves = range(1, self.slots+1)
        self.players = ("Player 1", "Player 2") # ("Red", "Yellow")
        self.board = np.zeros((self.rows, self.slots), dtype=int)
        self.turn = 0

    def players_move(self, case:str="default"):
        # this is taking text input from a prompt and making the move so ill probs change it to work with a mouse in a whiley
        # will defo need reworked
        players_turn = self.get_player_name()
        while True:
            match case:
                case "default":
                    move = input(f"The {players_turn} player puts their counter in slot...")
                case "bad_input":
                    move = input(f"The {players_turn} player didn't realise they had to put their counter in slot 1-{self.slots}. (Type 'exit' to close the game.)")
                case "full":
                    move = input(f"The {players_turn} player tried to put their counter in the full slot {full_col}, however they get to try again...(Type 'exit' to close the game.)")
                case "all_g":
                    self.move = checked_move-1
                    break

            if move == 'exit':
                raise Exception
            
            try: 
                move = int(move)
            except ValueError:
                case = "bad_input"; continue
            
            if move not in self.moves:
                case = "bad_input"
            elif self.board[0, move-1] != 0:
                full_col = move; case = "full"
            else: 
                checked_move = move; case = "all_g"
            

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


    def game_turn(self):
        self.players_move()
        placement = self.place_counter()
        winner = self.any_winners(placement)
        if winner:
            print(f"{self.get_player_name()} Wins!!!")
            print(self.board)
            raise Exception
        self.turn += 1


    def any_winners(self, placement):
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