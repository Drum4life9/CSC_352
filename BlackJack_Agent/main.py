from agent import *
from environment import BlackjackEnvironment

agent = BlackJackAgentLearned()
agent.loadQ("pickle")
wins = 0
num_episodes = 40000000
for _ in range(num_episodes):
    env = BlackjackEnvironment()
    res = env.run_game(agent)
    if res == 1:
        wins += 1

agent.saveQ("pickle")
print(agent.Q)

print('----------------win percentage-------------')
print(wins * 1.0 / num_episodes)
