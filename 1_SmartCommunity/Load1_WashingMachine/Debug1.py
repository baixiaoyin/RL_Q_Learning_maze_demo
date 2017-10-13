"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the main part which controls the update method of this example.
The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

from Home_env import HEMS_Env
from RL_brain import QLearningTable

'''
def update():
    for episode in range(100):
        # initial observation
        observation = env.reset()       # at the beginning, get the initial state of the episode.

        while True:
            # fresh env
            env.render()

            # RL choose action based on observation
            action = RL.choose_action(str(observation))

            # RL take action and get next observation and reward
            observation_, reward, done = env.update()

            # RL learn from this transition
            RL.learn(str(observation), action, reward, str(observation_))

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break

    # end of game
    print('game over')
    env.destroy()
'''

if __name__ == "__main__":
    env = HEMS_Env()
    #RL = QLearningTable(actions=list(range(env.n_actions)))
    #env.step('on')
    #env.update()
    #print(env.S)
    #env.reset()
    for i in range(20):
        observation_, reward, done = env.step('off')
        env.render()
        if done:
            break

    if done == False:
        env.step('on')
        env.render()
