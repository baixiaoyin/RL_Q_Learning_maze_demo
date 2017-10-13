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
import Home_env
from RL_brain import QLearningTable
import numpy as np
import matplotlib.pyplot as plt


def update():
    Bill = np.zeros(300)
    for episode in range(300):
        # initial observation
        observation = env.reset()       # at the beginning, get the initial state of the episode.

        while True:

            # RL take action and get next observation and reward
            action1 = RL.choose_action(observation)

            observation_, reward, done, action = env.step(action1)
            #env.render()
            RL.learn(observation, action, reward, observation_,  env.done)  # RL learn from this transition

            # swap observation

            env.S = observation_
            observation = observation_



            if done:
                break
        index = RL.q_table["on"].argsort()[:Home_env.Duration]
        #if RL.q_table["on"][index] <= RL.q_table["off"][index]:
        Bill[episode] = Home_env.DeviceEnergy * (sum(Home_env.Eprice_list[index]))

    # end of game
    print('Game over')
    #print(RL.q_table)
    plt.plot(Bill)
    plt.ylabel('Electricity Cost')
    plt.xlabel('Step')
    plt.show()

if __name__ == "__main__":
    env = HEMS_Env()
    RL = QLearningTable(actions=env.action_space)
    update()
