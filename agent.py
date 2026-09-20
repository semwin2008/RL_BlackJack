import torch
import torch.nn as nn

class Agent(nn.Module):
    def __init__(self, params):
        super().__init__()

        # temperature to maintain Exploration/Exploitaion balance
        self.temp = params['temp']
        self.step = params['step']

        self.network = nn.Sequential(
            nn.Linear(4, 64),
            nn.LeakyReLU(inplace=True),
            nn.Linear(64, 64),
            nn.LeakyReLU(inplace=True),
            nn.Linear(64, 4),
        )

    def forward(self, x, train=False):
        # annealing the Exploration to converge to zero
        if train:
            self.temp *= self.step
        x = self.network(x)
        EPS = .5
        y = x / (x.std() + EPS)
        return nn.functional.gumbel_softmax(y, tau=self.temp, hard=False)

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
        hp, st, mp, hp_opp = state
        # Если здоровье критически низкое (< 0.3), лечимся
        if hp < 0.3 and mp >= 0.1:
            return 1  # heal
        
        # Если у противника мало здоровья, добиваем атакой
        if hp_opp < 0.2 and st >= 0.1:
            return 2  # attack
        
        # Если много маны и выносливости, используем бомбу
        if mp >= 0.2 and st >= 0.1:
            return 3  # bomb
        
        # Если мало выносливости или маны, накапливаем ресурсы
        if st < 0.1 or mp < 0.1:
            return 0  # stay
        
        # По умолчанию атакуем
        return 2  # attack

class UserAgent():
    def __init__(self,):
        pass

    def act(self, state):
        print('State is:', torch.round(state, 2), 'Enter action (integer 0-3)')
        return int(input())
