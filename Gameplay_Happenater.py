import pygame as pg
from Base_Connectanator import Base_Connectanator

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
                self.set_running(False)
                
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


    def display(self):
        self.screen.fill((0,0,150))
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
        pg.display.flip()
        self.clock.tick(self.frame_rate) 


    def game_loop(self):
        self.set_running(True)
        while self.running:
            # try:
            self.display()
            move = self.handle_inputs()
            player = self.players[self.get_player()-1]

            # for bot players, overwrites whatever the handle_inputs has done
            if player is not None:
                move = player.make_move(self.get_board())

            any_win, player_turn = self.game_turn(move)

            if any_win:
                print(f'Player {player_turn} Wins!!!')
                print(self.get_board())
                break

            # except Exception as e:
            #     pg.quit()
            #     raise e
        pg.quit()

    def get_turn(self):
        return self.turn
    
    def get_player(self):
        # redefining compared to the bot one cause this is nicer and works for this class
        return self.turn % 2 + 1

    def set_running(self, val:bool):
        self.running = val
    
    def set_board(self, board):
        self.board = board