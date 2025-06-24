import numpy as np
import pygame as pg
from Base_Connectanator import Base_Connectanator

# TODO:  
# - start menu and end of game screen
# - draw detection / maximum number of peices

class Gameplay_Happenater(Base_Connectanator):
    def __init__(
            self,
            connect_num:int,
            players:tuple=(None, None),
            res=(1280,720),
            frame_rate=60,
        ):
        super().__init__(connect_num)
        pg.init()
        pg.key.set_repeat()
        pg.font.init()
        self.pg_text = pg.font.SysFont(pg.font.get_default_font(), 12)
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(res)

        self.state = None
        self.connect_num = connect_num
        self.players = (players[0], players[1])
        self.res = res
        self.frame_rate = frame_rate
        self.running = False
        
        self.slot_px = int(res[0] / self.slots)
        self.row_px = int(res[1] / self.rows)
        # making grid of circle centers:
        self.grid = [
            (self.slot_px*(i+0.5), self.row_px*(j+0.5)) 
                for i in range(self.slots) 
                for j in range(self.rows)
        ]
        self.cir_rad = int(min([self.row_px, self.slot_px])/2 - 5)
        self.curr_slot = 0


    def handle_inputs(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.set_state("close")
                
            elif event.type == pg.KEYDOWN:    
                if event.key == pg.K_ESCAPE:
                    self.set_running(False)
                elif event.key == pg.K_LEFT:
                    self.curr_slot = int((self.curr_slot - 1) % self.slots)
                elif event.key == pg.K_RIGHT:
                    self.curr_slot = int((self.curr_slot + 1) % self.slots)
                elif event.key in (pg.K_RETURN, pg.K_SPACE):
                    return self.curr_slot
        return None


    def game_turn(self, players_move=None):
        move = self.check_move(players_move)
        if move == None:
            return False
        
        self.board, placement = self.place_counter(self.board, move)
        winner = self.win_check(self.board, placement)
        if winner:
            # lets me find the winning move more easily
            self.board[placement]
        else:
            # no winner so increment turn
            self.turn += 1
        return winner
    

    def draw_game_board(self, show_player=False):
        self.screen.fill((0,0,150))
        if show_player:
            rect_left = int(self.grid[self.curr_slot*self.rows][0] - 0.5*self.slot_px)
            self.screen.fill(
                color="Orange",
                rect=(rect_left, 0, self.slot_px, self.res[1])
            )
        colors = ["Black", "Red", "Yellow"]
        for n, point in enumerate(self.grid):
            c = colors[self.board.flatten('F')[n]]
            pg.draw.circle(
                surface=self.screen,
                color=c,
                center=point,
                radius=self.cir_rad
            )
        text_surf = self.pg_text.render(f'Slot={self.curr_slot}', False, (0,0,0))
        self.screen.blit(text_surf, (1,1))

    def game_display(self, show_player=False):
        self.draw_game_board(show_player)
        pg.display.flip()
        self.clock.tick(self.frame_rate)

    def gaming(self):
        self.game_display(self.players[0] == None or self.players[1] == None)

        move = self.handle_inputs()
        player = self.players[self.get_player()-1]

        # for bot players, overwrites whatever the handle_inputs has done
        if player is not None:
            move = player.make_move(self.get_board())

        any_win = self.game_turn(move)
        if any_win:
            self.set_state("win")


    def start_menu(self):
        self.set_state("gaming")
    

    def pause(self):
        ...
    

    def win_display(self, win_spots):
        self.draw_game_board()

        for n, start in enumerate(win_spots[:-1]):
            end = win_spots[n+1]

            def p_to_px(p):
                x=int(p[1]*self.slot_px + 0.5*self.slot_px)
                y=int(p[0]*self.row_px + 0.5*self.row_px)
                return (x,y)
            
            pg.draw.line(
                surface=self.screen,
                color="gold",
                start_pos=p_to_px(start),
                end_pos=p_to_px(end),
                width=int(self.cir_rad / 2)
            )
        pg.display.flip()
        self.clock.tick(self.frame_rate)


    def win_screen(self, new_win=False):
        if new_win:
            winner = self.get_player()
            print(f'Player {winner} Wins!!!')
            w_spots = []
            for i in range(self.rows):
                for j in range(self.slots):
                    if self.win_check(self.get_board(), (i,j)):
                        w_spots += [(i,j)]
            self.set_state("won")
            self.win_display(w_spots)
        
        self.handle_inputs()


    def run(self):
        self.set_running(True)
        self.set_state("start_menu")
        while self.running:    
            state = self.get_state()
            match state:
                case "start_menu":
                    self.start_menu()
                case "gaming":
                    self.gaming()
                case "paused":
                    self.pause()
                case "win":
                    self.win_screen(True)
                case "won":
                    self.win_screen()
                case "close":
                    self.set_running(False)
                    break
                case _:
                    raise ValueError(f"The state <{state}> does not exist.")
        pg.quit()
                
    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_turn(self):
        return self.turn
    
    def get_player(self):
        # redefining compared to the bot one cause this is nicer and works for this class
        return int(self.turn % 2 + 1)

    def set_running(self, val:bool):
        self.running = val
    
    def set_board(self, board):
        self.board = board