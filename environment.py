from numpy import random
import torch


class State():
    def __init__(self, hp=1, stamina=1, mp=1, tm=0):
        self.hp = hp
        self.st = stamina
        self.mp = mp
    
    def stay(self, step):
        self.mp += step
        self.st += step
        return True

    def heal(self, step):
        if self.mp < step:
            return False
        self.hp += step
        self.mp -= step
        return True
    
    def attack(self, step):
        if self.st < step:
            return False
        self.st -= step
        return True
    
    def attacked(self, step):
        self.hp -= 2 * step
        return True
    
    def bomb(self, damage, step):
        if self.st < step or self.mp < 2 * step:
            return False
        self.st -= step
        self.mp -= 2 * step
        self.hp -= damage
        return True
    
    def bombed(self, damage):
        self.hp -= 2 * damage
        return True
    
    def is_finite(self,):
        return self.hp <= 0
    
    def __iter__(self,):
        yield self.hp
        yield self.st
        yield self.mp


class Environment():
    def __init__(self, 
        step=1e-1,
        bomb_power=2e-1,
        **kwargs,
    ):
        self.step = step
        self.bomb_power = bomb_power
        self.state_a = State()
        self.state_b = State()

    def get_state(self,):
        # Each player knows their own state and opponent's hp
        input_a = torch.tensor([*self.state_a, self.state_b.hp], dtype=torch.float)
        input_b = torch.tensor([*self.state_b, self.state_a.hp], dtype=torch.float)
        return input_a, input_b

    def check_game_over(self, action_a, action_b):
        # one of the players killed another
        return self.state_a.hp <= 0 or self.state_b.hp <= 0
    
    def sample(self,) -> float:
        return random.randn() * self.bomb_power
    
    def is_initial_state(self, state):
        return state == State()

    def reflect(self, action_a, action_b):
        # Acting
        # stay
        if action_a == 0:
            self.state_a.stay(self.step)
        if action_b == 0:
            self.state_b.stay(self.step)
        
        # heal
        if action_a == 1:
            self.state_a.heal(self.step)
        if action_b == 1:
            self.state_b.heal(self.step)
        
        # attack
        if action_a == 2:
            if self.state_a.attack(self.step):
                self.state_b.attacked(self.step)
        if action_b == 2:
            if self.state_b.attack(self.step):
                self.state_a.attacked(self.step)
        
        # bomb
        if action_a == 3:
            if self.state_a.bomb(self.bomb_power, self.step):
                self.state_b.bombed(self.bomb_power)
        if action_b == 3:
            if self.state_b.bomb(self.bomb_power, self.step):
                self.state_a.bombed(self.bomb_power)

        # Rewarding
        if self.state_a.is_finite() and self.state_b.is_finite():
            self.state_a = State()
            self.state_b = State()
            return 0, 0
        
        if self.state_a.is_finite():
            self.state_a = State()
            self.state_b = State()
            return -1, 1
        
        if self.state_b.is_finite():
            self.state_a = State()
            self.state_b = State()
            return 1, -1

        return 0, 0