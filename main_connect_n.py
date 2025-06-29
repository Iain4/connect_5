from Stateizer import Stateizer
from bots.Randy_The_Izer import Randy_The_Izer
from bots.Connecty_Collin import Connecty_Collin
from bots.Bob_BlocksLikesSteve_Branson import Blocky_Bob

CONNECT_NUM = 4
Randy = Randy_The_Izer(CONNECT_NUM)
Collin = Connecty_Collin(CONNECT_NUM)
Bob = Blocky_Bob(CONNECT_NUM)

# TODO:
# - perfect bot or NN
# - start, pause and win screen
# - animate peice drops - unlink frame rate and logic?
# - make everything look better

players = (None, Collin)
def main():
    game = Stateizer(
        connect_num=CONNECT_NUM,
        players=players,
        frame_rate=60,
        # res=(1920, 1080)
    )
    game.run()


if __name__ == "__main__":
    main()