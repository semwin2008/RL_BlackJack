from agent import Agent, RandomAgent, AlgoAgent
from environment import Environment
import yaml
from tensorboardX import SummaryWriter
import datetime


LOGDIR = './.logs/'

class Trainer():
    def __init__(self, exp_name=None):

        # Reading training config
        with open("config.yaml", "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)
        
        print('Configuration file read')

        # creating actor instance
        self.agent = Agent(self.config['agent'])
        print('Agent instance created')
        
        # creating optimizer
        self.optim = torch.optim.AdamW(self.agent.parameters(), lr=self.config['train']['lr'])
        print('Agent optimizer created')

        # creating environment instance
        self.env = Environment()
        print('Environment instance created')

        # creating logging env
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        exp_name = exp_name or f'experiment-{timestamp}'
        self.writer = SummaryWriter(LOGDIR + exp_name)
        self.writer.add_hparams(self.config, {'placeholder': 0})
        print('Started logging experiment:', exp_name)

    def log(self, metric, value):
        self.writer.add_scalar(metric, value)

    def make_step(self, data):
        loss = 0
        for state, action, reward in data:
            probs = torch.log(self.agent(state))
            logit = torch.zeros_like(probs)
            logit[action] = reward
            loss += probs * logit
        loss.backward()
        self.optim.step()
        self.optim.zero_grad()

    def validate(self, test_agent) -> float:
        test_env = Environment()

        num_steps = self.config['valid']['num_steps']
        sum_reward = 0
        for i in range(num_steps):
            state_a, state_b = test_env.get_state()
            action_a, action_b = self.agent.act(state_a), test_agent.act(state_b)
            reward_a, reward_b = test_env.reflect(action_a, action_b)
            sum_reward += reward_a
        
        return sum_reward / num_steps

    def train(self,):
        num_epochs = self.config['train']['num_epochs']
        for epoch in range(num_epochs):
            buffer = []
            sum_reward = 0
            num_steps = self.config['train']['num_steps']

            # Experience loop
            for step in range(num_steps):
                state_a, state_b = self.env.get_state()
                action_a, action_b = self.agent.act(state_a), self.agent.act(state_b)
                reward_a, reward_b = self.env.reflect(action_a, action_b)
                buffer.append((state_a, action_a, reward_a))
                buffer.append((state_b, action_b, reward_b))
                sum_reward += reward_a + reward_b

            # Validation
            random_score = validate(RandomAgent())
            algo_score = validate(AlgoAgent())
            self.log('Random | Mean Rew', random_score)
            self.log('Algo | Mean Rew', algo_score)

            # Logging
            print(f'Epoch [{epoch:{len(str(num_epochs))}}/{num_epochs}] ended')
            mean_reward = sum_reward / 2 / num_steps
            self.log('Self | Mean Rew', mean_reward)

            # Training step
            self.make_step(buffer)
        
        print('Training finished')
