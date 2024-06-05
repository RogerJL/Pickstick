import random
from typing_extensions import override

from picker import ComputerBase, PickStick, play, Human


class Analytical(ComputerBase):
    @override
    def query(self, stick: PickStick):
        to_remove = (stick.sticks - 1) % 4
        if to_remove == 0:
            to_remove = random.randint(1, min(3, stick.sticks))
        return to_remove

    @override
    def print_weights(self):
        pass  # Analytical uses no weights



def main_analytical():
    """Learning by playing analytical solution."""
    stick = PickStick(21)

    players = [Human(), Analytical()]
    print("Playing against", players[1].name)
    while True:
        stick.reset()
        winner = play(stick, players)
        winner.wins += 1
        print("WINS", "\t".join([f"{p.name}: {p.wins:3d}" for p in players]))


if __name__ == '__main__':
    main_analytical()
