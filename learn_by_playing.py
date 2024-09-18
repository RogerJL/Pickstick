import random
from typing_extensions import override

from human_player import Human
from picker import ComputerPlayer, PickStick, argmax, play_best_of


class Learner(ComputerPlayer):

    def __init__(self, name="AI"):
        super().__init__(name)
        self.start_sticks = None
        self.goodness = None
        self.taken_by = None
        self.gradients = None
        self._show_weights = False  # Change to True to see how weights change

    def zero_array(self):
        return [0 for _ in range(self.start_sticks)]

    def rand_array(self):
        return [random.randint(-1, 1) for _ in range(self.start_sticks)]

    @override
    def query(self, game: PickStick) -> int:
        if self.start_sticks is None:
            self.start_sticks = game.start_sticks
        if self.goodness is None:
            self.goodness = self.rand_array()
        if self.taken_by is None:
            self.taken_by = self.zero_array()
        if game.sticks < game.start_sticks:
            self.taken_by[game.sticks] = -1
        index, _ = argmax([self.goodness[pos - 1] for pos in game.range()])
        to_remove = index + 1
        self.taken_by[game.sticks - to_remove] = +1
        return to_remove

    def backward(self, win):
        gradient = 1 if win else -1
        self.gradients = [who * gradient for who in self.taken_by]
        self.taken_by = self.zero_array()

    def step(self):
        for index, gradient in enumerate(self.gradients):
            self.goodness[index] += gradient

    def zero_grad(self):
        self.gradients = None

    @override
    def show_weights(self):
        if self._show_weights:
            print(self.name, "WEIGHTS", ",".join([f"{v:3d}" for v in self.goodness]))

    @override
    def update(self, win: bool) -> None:
        self.zero_grad()  # optimizer.zero_grad()
        self.backward(win)  # loss.backward()
        self.step()  # optimizer.step()
        self.show_weights()


def main_learn():
    """Learning by playing against human"""
    play_best_of(PickStick(21),
                 [(Human()), (Learner())])


if __name__ == '__main__':
    main_learn()
