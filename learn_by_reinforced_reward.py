import random
from collections import deque

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter
from typing_extensions import override

from human_player import Human
from picker import PickStick, play, ComputerBase


class Reinforced(ComputerBase):
    def __init__(self, name="AI_net"):
        super().__init__(name=name)
        self.gamma = -0.999
        self.epoch = 0
        self.value_net = nn.Sequential(
            nn.Linear(21, 3),
        )
        self.rb = deque(maxlen=10000)
        self.train = True


    def sample(self):
        assert self.train, "AI_net must in train mode"
        pos = random.randrange(0, len(self.rb))
        return self.rb[pos]

    def prepare_inputs(self, stick):
        return self.prepare_inputs2(stick.sticks, num_classes=stick.start_sticks)

    def prepare_inputs2(self, pos, num_classes):
        return nn.functional.one_hot(torch.Tensor([pos - 1]).type(torch.int64), num_classes=num_classes).type(torch.float32)

    def train(self):
        self.train = True

    def eval(self):
        self.train = False

    @override
    def query(self, stick):
        observation = self.prepare_inputs(stick)
        actions = self.value_net(observation)
        if self.train:
            # fully random action
            best_index = torch.rand(size=(actions.shape[0], 1)) * min(stick.sticks, 3)
            best_index = best_index.type(torch.int64)
        else:
            # best_index = torch.multinomial(torch.softmax(actions, 1), 1).reshape((actions.shape[0], 1))
            _best_value, best_index = torch.max(actions, dim=1, keepdim=True)
        take_action = best_index + 1
        take_action[take_action > stick.sticks] = stick.sticks
        if self.train:
            reward = torch.where(stick.sticks - take_action == 0,
                                 -100.0,  # loose if taking last
                                 0)
            if len(self.rb) == self.rb.maxlen:
                self.rb.popleft()
            self.rb.append((observation, reward, take_action))
        return take_action

    @override
    def print_weights(self):
        print(self.name, "WEIGHTS", self.value_net.state_dict())



def main_reinforced():
    """Learning by playing against itself"""
    logger = SummaryWriter()
    global_step = 0
    stick = PickStick(21)
    players = [Reinforced(name="Ava"), Reinforced(name="HAL 9000")]
    optimizers = [torch.optim.SGD(p.value_net.parameters(), lr=3e-3) for p in players]
    for game in range(10000):
        stick.reset()
        winner = play(stick, players)
        winner.wins += 1
        print("WINS", "\t".join([f"{p.name}: {p.wins:3d}" for p in players]))
        for player_ai, optimizer in zip(players, optimizers):
            for s in range(10):
                global_step += 1
                observation, reward, action = player_ai.sample()  # TODO: sample(10)
                observation_next = torch.argmax(observation) + 1 - action
                with torch.no_grad():
                    if observation_next == 0:
                        actions_next = torch.Tensor()
                        td_target = reward
                    else:
                        actions_next = player_ai.value_net(player_ai.prepare_inputs2(observation_next, stick.start_sticks))
                        impossible = observation_next
                        actions_next[:, impossible:] = -1000
                        target_max, _ = torch.max(actions_next, dim=1, keepdim=True)
                        td_target = reward + player_ai.gamma * target_max

                index = action - 1
                action_est = player_ai.value_net(observation)
                td_est = action_est.gather(1, index)
                #print(f"{torch.argmax(observation).item()+1:2d}, {action.detach().numpy()}, {reward.item():-7.2f}",
                #      "action est", action_est.detach().numpy(), td_est.item(),
                #      "action next", actions_next.numpy(), td_target.item())
                loss = F.mse_loss(td_est, td_target)
                logger.add_scalar("loss", loss.item(), global_step=global_step)

                # perform our gradient decent step
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            if game % 1000 == 0:
                player_ai.print_weights()

    logger.close()

    players = [Human(), random.choice(players)]
    players[1].wins = 0
    players[1].eval()
    print("Playing against", players[1].name)
    while True:
        stick.reset()
        winner = play(stick, players)
        winner.wins += 1
        print("WINS", "\t".join([f"{p.name}: {p.wins:3d}" for p in players]))

if __name__ == '__main__':
    main_reinforced()
