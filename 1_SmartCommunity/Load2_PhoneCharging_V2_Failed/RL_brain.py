"""
This part of code is the Q learning brain, which is a brain of the agent.
All decisions are made in here.
"""

import numpy as np
import pandas as pd
import Home_env as HE

class RL(object):
    def __init__(self, action_space, learning_rate=0.05, reward_decay=0.9, e_greedy=0.9, TimeSlots=HE.TotalTime):
        self.actions = action_space  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.TtTime = TimeSlots
        #self.q_table = pd.DataFrame(np.zeros((self.TtTime, len(self.actions))), columns=self.actions)
        self.q_table1 = pd.DataFrame(np.zeros((self.TtTime, 1)), columns=['on'])
        self.q_table2 = pd.DataFrame(np.ones((self.TtTime, 1)), columns=['off'])
        self.q_table = self.q_table1.join(self.q_table2, how='outer')

    def choose_action(self, observation) :
        # action selection
        if observation == 'Terminal':
            action = 'off'  #??
        elif np.random.rand() < self.epsilon:
            # choose best action
            state_action = self.q_table.ix[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))     # some actions have same value
            action = state_action.argmin()
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def learn(self, *args):
        pass


# off-policy
class QLearningTable(RL):
    def __init__(self, actions, learning_rate=0.01, reward_decay=1, e_greedy=0.9): #?? Reward Decay ?= 1??
        super(QLearningTable, self).__init__(actions, learning_rate, reward_decay, e_greedy)

    def learn(self, s, a, r, s_,  done):
        q_predict = self.q_table.ix[s, a]
        if s_ != 'Terminal':
            q_target = r + self.gamma * self.q_table.ix[s_, :].min()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.ix[s, a] += self.lr * (q_target - q_predict)  # update


# on-policy
class SarsaTable(RL):

    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        super(SarsaTable, self).__init__(actions, learning_rate, reward_decay, e_greedy)

    def learn(self, s, a, r, s_, a_, done):
        q_predict = self.q_table.ix[s, a]
        if s_ != 'Terminal':
            q_target = r + self.gamma * self.q_table.ix[s_, a_]  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.ix[s, a] += self.lr * (q_target - q_predict)  # update
