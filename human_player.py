from typing_extensions import override

from picker import Player, PickStick

STICK_SYMBOL = " ❙"


class Human(Player):
    def __init__(self):
        super().__init__("Human")
        self.verbose = True
        self.visual = True

    @override
    def query(self, stick: PickStick) -> int:
        picked = '?' if self.verbose else ''
        while True:
            if self.visual:
                if self.verbose:
                    columns = stick.sticks // (stick.max + 1)
                    final_rows = stick.sticks % (stick.max + 1)
                    for row in range(stick.max + 1):
                        print(STICK_SYMBOL * columns, end="")
                        print(STICK_SYMBOL if row < final_rows else "")
                else:
                    print(STICK_SYMBOL * stick.sticks)
            else:
                print(f"There are {stick.sticks} sticks on the table.")
                if picked == '?':
                    print(f"You can pick {stick.min} to {stick.max} sticks")
                    print(f"Picker of last stick looses")
            picked = input(f"How many sticks do you want to pick [?, {stick.min}..{min(stick.max, stick.sticks)}] ")
            if picked.isalnum():
                picked = int(picked)
                if stick.min <= picked <= stick.max and picked <= stick.sticks:
                    return picked
                print("ERROR Choose too many or too few sticks")
