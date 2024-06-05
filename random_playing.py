import random

from human_player import Human
from picker import ComputerBase, PickStick, play


class Random(ComputerBase):
    def query(self, stick: PickStick):
        return random.randint(1, min(3, stick.sticks))

    def print_weights(self):
        pass  # Random uses no weights

def main_random():
    """Learning by playing analytical solution."""
    stick = PickStick(21)

    players = [Human(), Random()]
    print("Playing against", players[1].name)
    while True:
        stick.reset()
        winner = play(stick, players)
        winner.wins += 1
        print("WINS", "\t".join([f"{p.name}: {p.wins:3d}" for p in players]))


if __name__ == '__main__':
    main_random()
