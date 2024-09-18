import random

from human_player import Human
from learn_by_playing import Learner
from picker import PickStick, play, update, play_best_of

SELF_PLAY_GAMES = 10


def main_self_play():
    """Learning by playing against itself"""
    game = PickStick(21)
    players = [Learner(name="Ava"), Learner(name="HAL 9000")]
    for game_no in range(SELF_PLAY_GAMES):
        game.reset()
        winner = play(game, players)
        update(players, winner)
        print("WINS", "\t".join([f"{p.name}: {p.wins:3d}" for p in players]))

    # Select one of the trained AIs to let the human play against
    play_best_of(game,
                 [Human(), random.choice(players)])


if __name__ == '__main__':
    main_self_play()
