import numpy as np
from Base_Connectanator import Base_Connectanator
from Gameplay_Happenater import Gameplay_Happenater
import pygame as pg

CONNECT_NUM = 5


def main():
    fe = Gameplay_Happenater(CONNECT_NUM, res=(1920,1080))
    be = Base_Connectanator(CONNECT_NUM)

    fe.set_running(True)
    while fe.running:
        try:
            board = be.get_board()
            move = fe.game_runner(board)
            any_win, player_turn = be.game_turn(move)
            if any_win:
                print(f'Player {player_turn} Wins!!!')
                print(be.get_board())
                break

        except Exception as e:
            pg.quit()
            raise e
    pg.quit()


if __name__ == "__main__":
    main()