from typing_extensions import override

from picker import Player, PickStick

STICK_SYMBOL = " ❙"


class Human(Player):
    def __init__(self):
        super().__init__("Human")
        self.verbose = True
        self.visual = True

    @override
    def query(self, game: PickStick) -> int:
        picked = '?' if self.verbose else ''
        while True:
            if self.visual:
                if self.verbose:
                    columns = game.sticks // (game.max + 1)
                    final_rows = game.sticks % (game.max + 1)
                    for row in range(game.max + 1):
                        print(STICK_SYMBOL * columns, end="")
                        print(STICK_SYMBOL if row < final_rows else "")
                else:
                    print(STICK_SYMBOL * game.sticks)
            else:
                print(f"There are {game.sticks} sticks on the table.")
                if picked == '?':
                    print(f"You can pick {game.min} to {game.max} sticks")
                    print(f"Picker of last stick looses")
            picked = input(f"How many sticks do you want to pick [?, {game.min}..{min(game.max, game.sticks)}] ")
            if picked.isalnum():
                picked = int(picked)
                if game.min <= picked <= game.max and picked <= game.sticks:
                    return picked
                print("ERROR Choose too many or too few sticks")
