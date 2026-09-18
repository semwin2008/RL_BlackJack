import torch
import torch.nn as nn

class Agent(nn.Module):
    def __init__(self, **params):
        super().__init__()

        self.network = nn.Linear(1, 2)
        self.activ = nn.Sigmoid()

    def forward(self, x):
        return self.activ(self.network(x))

    def act(self, state):
        return self.forward(state)
