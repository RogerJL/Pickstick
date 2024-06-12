import random
from typing_extensions import override

from human_player import Human
from picker import ComputerPlayer, PickStick, play, argmax


class Learner(ComputerPlayer):

    def __init__(self, name="AI"):
        super().__init__(name)
        self.start_sticks = None
        self.goodness = None
        self.taken_by = None
        self.gradients = None

    def zero_array(self):
        return [0 for _ in range(self.start_sticks)]

    def rand_array(self):
        return [random.randint(-1, 1) for _ in range(self.start_sticks)]

    @override
    def query(self, stick: PickStick) -> int:
        if self.start_sticks is None:
            self.start_sticks = stick.start_sticks
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

    @override
    def show_weights(self):
        print(self.name, "WEIGHTS", ",".join([f"{v:3d}" for v in self.goodness]))


def main_org():
    """Learning by playing against human"""
    stick = PickStick(21)
    player_h = Human()
    player_ai = Learner()
    players = [player_h, player_ai]
    while True:
        stick.reset()
        winner = play(stick, players)
        winner.wins += 1
        print("WINS", "\t".join([f"{p.name}: {p.wins:3d}" for p in players]))
        player_ai.zero_grad()  # optimizer.zero_grad()
        player_ai.backward(winner)  # loss.backward()
        player_ai.step()  # optimizer.step()
        player_ai.show_weights()


if __name__ == '__main__':
    main_org()
