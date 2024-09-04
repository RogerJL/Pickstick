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
        self._name = name
        self._wins = 0

    def query(self, game: PickStick) -> int:
        raise NotImplementedError("query() not implemented")

    def update(self, win: bool) -> None:
        pass

    @property
    def name(self):
        return self._name

    @property
    def wins(self) -> int:
        return self._wins

    def increment_wins(self):
        self._wins += 1

    def reset_wins(self):
        self._wins = 0


class ComputerPlayer(Player):
    """Base class for all computer implementations"""
    def __init__(self, name="AI"):
        super().__init__(name=name)

    def show_weights(self):
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
    """Play a game of Pickstick/NIM"""
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


def update(players: list[Player], winner: Player):
    winner.increment_wins()
    for player in players:
        player.update(win=player is winner)


def play_best_of(game, players):
    for player in players:
        player.reset_wins()
    print("Playing against", players[1].name)
    while True:
        game.reset()
        winner = play(game, players)
        update(players, winner)
        print("WINS", "\t".join([f"{p.name}: {p.wins:3d}" for p in players]))
