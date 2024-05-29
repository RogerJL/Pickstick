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

    def query(self, stick):
        picked = '?' if self.verbose else ''
        self.verbose = False
        while True:
            print(f"There are {stick.sticks} sticks on the table.")
            if picked == '?':
                print(f"You can pick {stick.min} to {stick.max} sticks")
                print(f"Picker of last stick looses")
            picked = input(f"How many sticks do you want to pick [?, {stick.min}..{stick.max}] ")
            if picked.isalnum():
                picked = int(picked)
                if stick.min <= picked <= stick.max and picked <= stick.sticks:
                    return picked
                print("ERROR Choose too many or too few sticks")


class AI(Player):

    def __init__(self, stick):
        super().__init__("AI")
        self.stick = stick
        self.goodness = None
        self.taken_by = None
        self.gradients = None

    def zero_array(self):
        return [0 for _ in range(self.stick.start_sticks)]

    def rand_array(self):
        return [random.randint(-1,1) for _ in range(self.stick.start_sticks)]

    def query(self, stick):
        if self.goodness is None:
            self.goodness = self.rand_array()
        if self.taken_by is None:
            self.taken_by = self.zero_array()
        if stick.sticks < stick.start_sticks:
            self.taken_by[stick.sticks] = -1
        index, _ = argmax([self.goodness[pos - 1] for pos in stick.range()])
        to_remove = index + 1
        self.taken_by[stick.sticks - to_remove] = +1
        return to_remove

    def backward(self, winner):
        gradient = 1 if winner == self else -1
        self.gradients = [who * gradient for who in self.taken_by]
        self.taken_by = self.zero_array()

    def step(self):
        for index, gradient in enumerate(self.gradients):
            self.goodness[index] += gradient

    def zero_grad(self):
        self.gradients = None


def argmax(values):
    best_index = None
    best_value = float('-inf')
    for index, value in enumerate(values):
        if value > best_value:
            best_value = value
            best_index = index
    return best_index, best_value


def play(stick, players):
    previous_player = None
    while stick.sticks > 0:
        for player in players:
            to_remove = player.query(stick)
            last_picked = stick.remove(to_remove)
            if last_picked:
                break
            previous_player = player
    return previous_player


def main():
    """Learning by playing agains human"""
    stick = PickStick(21)
    player_h = Human()
    player_ai = AI(stick)
    players = [player_h, player_ai]
    while True:
        stick.reset()
        winner = play(stick, players)
        winner.wins += 1
        print("WINS", "\t".join([f"{p.name}: {p.wins:3d}" for p in players]))
        player_ai.zero_grad()
        player_ai.backward(winner)
        player_ai.step()
        print("DEBUG", player_ai.goodness)


def main_rl():
    """Learning by playing against itself"""
    stick = PickStick(21)
    players = [AI(stick), AI(stick)]
    for game in range(10):
        stick.reset()
        winner = play(stick, players)
        winner.wins += 1
        print("WINS", "\t".join([f"{p.name}: {p.wins:3d}" for p in players]))
        for player_ai in players:
            player_ai.zero_grad()
            player_ai.backward(winner)
            player_ai.step()
            print("DEBUG", ",".join([f"{v:3d}" for v in player_ai.goodness]))


if __name__ == '__main__':
    main_rl()
