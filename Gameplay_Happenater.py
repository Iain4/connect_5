import numpy as np
import pygame as pg
from Base_Connectanator import Base_Connectanator

# TODO:  
# - start menu and end of game screen buttons
# - draw detection / maximum number of peices
# - make a not shit bot

class Gameplay_Happenater(Base_Connectanator):
    # does the gameplay interaction for the players
    def __init__(
            self,
            connect_num:int,
            players:tuple=(None, None)
        ):
        super().__init__(connect_num)
        pg.init()
        pg.key.set_repeat()
        # pg.font.init()
        # self.pg_text = pg.font.SysFont(pg.font.get_default_font(), 12)
        
        self.state = None
        self.connect_num = connect_num
        self.players = (players[0], players[1])
        # self.running = False
    

    # will need to make handle inputs state depedant
    # or write a new one for each state once i make menus
    def handle_inputs(self):
        # returns the players move
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.set_state("close")
                
            elif event.type == pg.KEYDOWN:
                match event.key:
                    # escape needs to pause / play etc. so gets its own match case
                    case pg.K_ESCAPE:
                        match self.get_state():
                            case "gaming":
                                self.set_state("paused")
                            case "won":
                                self.set_state("close")
                            case "paused":
                                self.set_state("gaming")
                    case pg.K_q:
                        self.set_state("close")
                    case pg.K_LEFT:
                        self.curr_slot = int((self.curr_slot - 1) % self.slots)
                    case pg.K_RIGHT:
                        self.curr_slot = int((self.curr_slot + 1) % self.slots)
                    case pg.K_RETURN | pg.K_SPACE:
                        return self.curr_slot
        return None


    def game_turn(self, players_move=None):
        move = self.check_move(players_move)
        if move == None:
            return False
        
        self.board, placement = self.place_counter(self.board, move, self.get_player())
        winner = self.win_check(self.board, placement)
        if winner:
            # lets me find the winning move more easily
            self.board[placement]
        else:
            # no winner so increment turn
            self.turn += 1
        return winner
    

    def gaming(self):
        # self.game_display(self.players[0] == None or self.players[1] == None)

        move = self.handle_inputs()
        player = self.players[self.get_player()-1]

        # for bot players, overwrites whatever the handle_inputs has done
        if player is not None:
            move = player.make_move(self.get_board())

        any_win = self.game_turn(move)
        if any_win:
            self.set_state("win")


    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_turn(self):
        return self.turn
    
    def get_player(self):
        # redefining compared to the bot one cause this is nicer and works for this class
        return int(self.turn % 2 + 1)

    # def set_running(self, val:bool):
    #     self.running = val
    
    def set_board(self, board:np.ndarray):
        if board.shape != self.board.shape:
            raise ValueError(f"Shape of new board <{board.shape}> is not the same as the original <{self.board}>.")
        self.board = board