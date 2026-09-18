from random import randint


class Environment():
    def __init__(self, 
        threshold=21,
        max_value=10,
    ):
        self.threshold = threshold
        self.max_value = max_value
        self.state_a = 0
        self.state_b = 0
    
    def get_state(self,):
        return self.state_a, self.state_b

    def update_state(self, action_a, action_b):
        # both players passed or at least one reached threshold => game is over
        if action_a == 0 and action_b == 0 or \
            self.state_a >= self.threshold or self.state_b >= self.threshold:
            yield True
            self.state_a = 0
            self.state_b = 0
            return None
        yield False
    
    def sample(self,) -> int:
        return randint(1, self.max_value)
    
    def winner_num(self,) -> int:
        if self.state_a < self.threshold and self.state_b < self.threshold:
            return max(self.state_a, self.state_b)
        if self.state_a == self.threshold or self.state_b == self.threshold:
            return self.threshold
        return min(self.state_a, self.state_b)
        

    def reflect(self, action_a, action_b):
        # acting
        if action_a == 1:
            self.state_a += self.sample()
        if action_b == 1:
            self.state_b += self.sample()
        
        # checking if game is over
        call = update_state(action_a, action_b)
        if next(call):
            winner_num = self.winner_num()
            if self.state_a == winner_num and self.state_b == winner_num:
                reward_a, reward_b = 0, 0
            elif self.state_a == winner_num:
                reward_a, reward_b = 1, -1
            else:
                reward_a, reward_b = -1, 1
        else:
            reward_a, reward_b = 0, 0
        # updating states if game is over
        next(call)

        return reward_a, reward_b