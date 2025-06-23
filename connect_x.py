from Gameplay_Happenater import Gameplay_Happenater
from Randy_The_Izer import Randomator

CONNECT_NUM = 3
randy = Randomator(CONNECT_NUM)

def main():
    game = Gameplay_Happenater(
        connect_num=CONNECT_NUM,
        players=(None, randy)
    )
    game.game_loop()

if __name__ == "__main__":
    main()