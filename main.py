from trainer import Trainer
import sys


if __name__ == '__main__':
    exp_name = sys.argv[1] if len(sys.argv) > 1 else None
    rl_trainer = Trainer(exp_name=exp_name)
    rl_trainer.train()
