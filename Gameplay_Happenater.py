import pygame as pg
import numpy as np

class Gameplay_Happenater():
    def __init__(
            self,
            connect_num:int,
            res=(1280,720),
            frame_rate=60,
        ):
        pg.init()
        pg.key.set_repeat(10)
        self.connect_num = connect_num
        self.res = res
        self.screen = pg.display.set_mode(res)
        self.frame_rate = frame_rate
        self.clock = pg.time.Clock()
        self.running = False

        self.slots = 2 * connect_num - 1
        self.rows = self.slots - 1
        self.slot_px = int(res[0] / self.slots)
        self.row_px = int(res[1] / self.rows)
        # making grid of circle centers:
        self.grid = [
            (self.slot_px*(i+0.5), self.row_px*(j+0.5)) 
                for i in range(self.slots) 
                for j in range(self.rows)
        ]
        self.cir_rad = int(min([self.row_px, self.slot_px])/2 - 5)
        self.board = np.zeros((self.rows, self.slots), dtype=int)
        self.curr_slot = 0


    def game_runner(self, board):
        self.set_board(board)
        move = self.handle_inputs()
        self.display_func()
        return move


    def handle_inputs(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.set_running(False)
        
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self.set_running(False)
        if True: #keys[pg.K_LEFT]:
            self.curr_slot = int((self.curr_slot - 1) % self.slots)
        if keys[pg.K_RIGHT]:
            self.curr_slot = int((self.curr_slot + 1) % self.slots)
        if keys[pg.K_RETURN]:
            return self.curr_slot
        return None


    def display_func(self):
        self.screen.fill((0,0,150))
        rect_left = int(self.grid[self.curr_slot][0] - 0.5*self.slot_px)
        self.screen.fill(
            color="Yellow",
            rect=(rect_left, 0, 2*self.cir_rad, self.res[1])
        )
        colors = ["Black", "Red", "Yellow"]
        for n, point in enumerate(self.grid):
            c = colors[self.board.flatten()[n]]
            pg.draw.circle(
                surface=self.screen,
                color=c,
                center=point,
                radius=self.cir_rad
            )
        pg.display.flip()
        self.clock.tick(self.frame_rate)
    

    def set_running(self, val:bool):
        self.running = val
    
    def set_board(self, board):
        self.board = board
    