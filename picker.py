import random


class PickStick:
    def __init__(self, sticks):
        self.min = 1
        self.max = 3
        self.start_sticks = sticks
        self.sticks = None

    def range(self):
        assert self.sticks is not None, "Should reset() before use"
        return range(self.sticks - self.min + 1, max(0, self.sticks - self.max), -1)

    def remove(self, to_remove: int) -> bool:
        assert self.sticks is not None, "Should reset() before use"
        assert self.min <= to_remove <= self.max, f"Removed sticks should be in range [{self.min}, {self.max}]"
        assert self.sticks >= to_remove, "Can't remove more sticks than exists"
        self.sticks -= to_remove
        return self.sticks == 0

    def reset(self):
        self.sticks = self.start_sticks


class Player:
    def __init__(self, name):
        self.name = name
        self.wins = 0

class Human(Player):
    def __init__(self):
        super().__init__("Human")
        self.verbose = True
        self.visual = True

    def query(self, stick):
        picked = '?' if self.verbose else ''
        while True:
            if self.visual:
                if self.verbose:
                    columns = stick.sticks // (stick.max + 1)
                    final_rows = stick.sticks % (stick.max + 1)
                    for row in range(stick.max + 1):
                        print(" ❙" * columns, end="")
                        print(" ❙" if row < final_rows else "")
                else:
                    print(" ❙" * stick.sticks)
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


class AI(Player):
    def __init__(self, name="AI"):
        super().__init__(name=name)

    def print_weights(self):
        print(self.name, "WEIGHTS", "unknown")


def argmax(values):
    best_index = None
    best_value = float('-inf')
    for index, value in enumerate(values):
        if value > best_value:
            best_value = value
            best_index = index
    return best_index, best_value


def play(stick, players):
    players = random.sample(players, k=len(players))
    previous_player = None
    while stick.sticks > 0:
        for player in players:
            to_remove = player.query(stick)
            last_picked = stick.remove(to_remove)
            if last_picked:
                break
            previous_player = player
    return previous_player
