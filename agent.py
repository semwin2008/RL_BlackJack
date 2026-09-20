import torch
import torch.nn as nn

class Agent(nn.Module):
    def __init__(self, params):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(4, 64),
            nn.LeakyReLU(inplace=True),
            nn.Linear(64, 64),
            nn.LeakyReLU(inplace=True),
            nn.Linear(64, 4),
        )
        self.activ = nn.Softmax(dim=-1)

    def forward(self, x):
        return self.activ(self.network(x))

    def act(self, state):
        return torch.multinomial(self.forward(state), 1)


class RandomAgent():
    def __init__(self,):
        pass

    def act(self, state):
        return torch.randint(0, 4, (1,))


class AlgoAgent():
    def __init__(self,):
        pass

    def act(self, state):
        pass
