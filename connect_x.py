from Gameplay_Happenater import Gameplay_Happenater
from bots.Randy_The_Izer import Randy_The_Izer
from bots.Connecty_Collin import Connecty_Collin

CONNECT_NUM = 4
Randy = Randy_The_Izer(CONNECT_NUM)
Collin = Connecty_Collin(CONNECT_NUM)

def main():
    game = Gameplay_Happenater(
        connect_num=CONNECT_NUM,
        players=(Randy, Collin),
        frame_rate=6
    )
    game.game_loop()

if __name__ == "__main__":
    main()