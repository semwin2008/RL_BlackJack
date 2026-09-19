import torch
import torch.nn as nn

class Agent(nn.Module):
    def __init__(self, params):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(1, 32),
            nn.LeakyReLU(inplace=True),
            nn.Linear(32, 32),
            nn.LeakyReLU(inplace=True),
            nn.Linear(32, 2),
        )
        self.activ = nn.Softmax(dim=-1)

    def forward(self, x):
        return self.activ(self.network(x / 21))

    def act(self, state):
        return torch.multinomial(self.forward(state), 1)


class RandomAgent():
    def __init__(self,):
        pass

    def act(self, state):
        return torch.randint(0, 2, (1,))


class AlgoAgent():
    def __init__(self,):
        pass

    def act(self, state):
        if state < 19:
            return 1
        return 0
