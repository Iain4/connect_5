from Gameplay_Happenater import Gameplay_Happenater
import pygame as pg
from pygame_extras import Button

class Stateizer(Gameplay_Happenater):
    def __init__(
            self,
            connect_num:int,
            players:tuple=(None, None),
            res=(1280,720),
            frame_rate=60,
        ):
        super().__init__(connect_num, players)

        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(res)
        self.res = res
        self.frame_rate = frame_rate

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


    def run(self):
        # self.set_running(True)
        self.set_state("start_menu")
        while True:    
            state = self.get_state()
            match state:
                case "start_menu":
                    self.start_menu()
                case "gaming":
                    self.game_display(self.players[0] == None or self.players[1] == None)
                    self.gaming()
                case "paused":
                    self.pause()
                case "win":
                    self.win_screen(self.get_board(), True)
                case "won":
                    self.win_screen(self.get_board())
                case "close":
                    # self.set_running(False)
                    break
                case _:
                    raise ValueError(f"The state <{state}> does not exist.")
        pg.quit()

    def render(self):
        pg.display.flip()
        self.clock.tick(self.frame_rate)


    ### gaming state ###
    def draw_game_board(self, board, show_player=False):
        # background
        self.screen.fill((0,0,150))
        # player slot indecator
        if show_player:
            rect_left = int(self.grid[self.curr_slot*self.rows][0] - 0.5*self.slot_px)
            self.screen.fill(
                color="Orange",
                rect=(rect_left, 0, self.slot_px, self.res[1])
            )
        # counters and holes
        colors = ["Black", "Red", "Yellow"]
        for n, point in enumerate(self.grid):
            c = colors[board.flatten('F')[n]]
            pg.draw.circle(
                surface=self.screen,
                color=c,
                center=point,
                radius=self.cir_rad
            )
        # text_surf = self.pg_text.render(f'Slot={self.curr_slot}', False, (0,0,0))
        # self.screen.blit(text_surf, (1,1))

    def game_display(self, show_player=False):
        self.draw_game_board(self.get_board(), show_player)
        self.render()


    ### win / won state ###
    # TODO: Fix edge case for drawing line where two different line are completed at once
    def win_screen(self, board, new_win=False):
        # no point repeating but feel like theres a better way of doing this
        # finds the winning line of counters
        if new_win:
            w_spots = []
            for i in range(self.rows):
                for j in range(self.slots):
                    if self.win_check(board, (i,j)):
                        w_spots += [(i,j)]
            
            self.set_state("won") # only does once
            self.win_display(board, w_spots)
        
        self.handle_inputs()
    
    def win_display(self, board, win_spots):
        self.draw_game_board(board)

        for n, start in enumerate(win_spots[:-1]):
            end = win_spots[n+1]

            def p_to_px(p):
                x=int(p[1]*self.slot_px + 0.5*self.slot_px)
                y=int(p[0]*self.row_px + 0.5*self.row_px)
                return (x,y)
            
            pg.draw.line(
                surface=self.screen,
                color="orange",
                start_pos=p_to_px(start),
                end_pos=p_to_px(end),
                width=int(self.cir_rad / 2)
            )
        self.render()

    
    ### start_menu state ###
    def start_menu(self):
        self.draw_game_board(self.get_board())
        pose = (int(self.res[0]/2), int(self.res[1]/2)) 
        dim = (int(0.33*self.res[0]), int(0.2*self.res[1]))

        start_button = Button(
            pose,
            dim,
            text="START"
        )
        start_button.draw(self.screen)
        self.handle_inputs()
        # self.set_state("gaming")
        self.render()
    

    ### paused state ###
    def pause(self):
        self.handle_inputs()




