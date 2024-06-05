import random

from human_player import Human
from lear_by_playing import Learner
from picker import PickStick, play


def main_self_play():
    """Learning by playing against itself"""
    stick = PickStick(21)
    players = [Learner(name="Ava"), Learner(name="HAL 9000")]
    for game in range(10):
        stick.reset()
        winner = play(stick, players)
        winner.wins += 1
        print("WINS", "\t".join([f"{p.name}: {p.wins:3d}" for p in players]))
        for player_ai in players:
            player_ai.zero_grad()
            player_ai.backward(winner)
            player_ai.step()
            player_ai.print_weights()

    players = [Human(), random.choice(players)]
    players[1].wins = 0
    print("Playing against", players[1].name)
    while True:
        stick.reset()
        winner = play(stick, players)
        winner.wins += 1
        print("WINS", "\t".join([f"{p.name}: {p.wins:3d}" for p in players]))


if __name__ == '__main__':
    main_self_play()
