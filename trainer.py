from agent import Agent
from environment import Environment
import yaml


class Trainer():
    def __init__(self, exp_name=None):
        self.exp_name = exp_name or ''

        # Reading training config
        with open("config.yaml", "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)
        
        print('Configuration file read')

        # creating actor instance
        self.agent = Agent(self.config['agent'])
        print('Agent instance created')

        # creating environment instance
        self.env = Environment()
        print('Environment instance created')


    def log(self,):
        pass
    
    def train(self,):
        pass
