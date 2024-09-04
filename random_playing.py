import random
from typing import override

from human_player import Human
from picker import ComputerPlayer, PickStick, play, update, play_best_of


class Random(ComputerPlayer):
    @override
    def query(self, game: PickStick) -> int:
        return random.randint(1, min(3, game.sticks))

    @override
    def show_weights(self):
        pass  # Random uses no weights


def main_random():
    """Learning by playing analytical solution."""
    play_best_of(PickStick(21),
                 [Human(), Random()])


if __name__ == '__main__':
    main_random()
