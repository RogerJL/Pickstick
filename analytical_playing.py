import random
from typing_extensions import override

from human_player import Human
from picker import ComputerPlayer, PickStick, play_best_of


class Analytical(ComputerPlayer):
    @override
    def query(self, game: PickStick) -> int:
        to_remove = (game.sticks - 1) % 4
        if to_remove == 0:
            to_remove = random.randint(1, min(3, game.sticks))
        return to_remove

    @override
    def show_weights(self):
        pass  # Analytical uses no weights


def main_analytical():
    """Learning by playing analytical solution."""
    play_best_of(PickStick(21),
                 [Human(), Analytical()])


if __name__ == '__main__':
    main_analytical()
