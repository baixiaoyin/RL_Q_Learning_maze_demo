"""
Reinforcement learning HEMS Env for Type 1 load, like washing machine, deferrable but not interruptable.

This script is the environment part of this example.
The RL is in RL_brain.py.

"""


import numpy as np
import time
import sys
import csv
import pandas as pd


df = pd.read_csv("Price_List.csv")
saved_column = df.USEP #you can also use df['column_name']
Eprice_list = np.array(saved_column)
TotalTime = len(Eprice_list)
DeviceEnergy = 1
FRESH_TIME = 0.1
Duration = 4

class HEMS_Env(object) :
    def __init__(self):
        self.action_space = ['on', 'off']
        self.n_actions = len(self.action_space)
        self.TtTime = TotalTime
        self.price_list = Eprice_list
        self.env_list = ['S']+['-'] * TotalTime + ['T']  # '----------' our environment
        self.S = 0
        self.R = 0
        self.count = 0
        self.done = False
        self.action = 'off'

    def update(self):
        s = self.S
        if self.action == 'on':
            self.env_list[s+1] = 'D'
            interaction = ''.join(self.env_list)
            print('\r{}'.format(interaction), end='')
            time.sleep(FRESH_TIME)

        elif self.action == 'off':
            self.env_list[s+1] = '0'
            interaction = ''.join(self.env_list)
            print('\r{}'.format(interaction), end='')
            time.sleep(FRESH_TIME)

        elif self.action == 'unknown':

            interaction = ''.join(self.env_list)
            print('\r{}'.format(interaction), end='')
            time.sleep(FRESH_TIME)

    def step(self, action):
        # This is how agent will interact with the environment
        s = self.S
        Eprice_list_t = Eprice_list
        if s == TotalTime -1:
            s_ = "Terminal"
            self.done = True
        elif self.count == Duration:
        # elif (self.count == Duration - 1 and action == 'on'):
            s_ = "Terminal"
            self.done = True
        else:
            s_ = s + 1
            self.done = False

        if action == 'off':
            if s >= TotalTime - Duration + self.count:
                self.action = 'on'
                self.count = self.count + 1
                R = DeviceEnergy*(Eprice_list[s])
                #Rt = DeviceEnergy * (Eprice_list[s])
                self.R = self.R + R
            else:
                self.action = 'off'
                R = DeviceEnergy*max(Eprice_list[Eprice_list.argsort()[:Duration]])
                #R = DeviceEnergy * (np.average(Eprice_list_t))
                #R = DeviceEnergy*(max(np.delete(Eprice_list_t, s)))
                #Rt = 0
                self.R = self.R + R
        else:
            self.action = 'on'
            R = DeviceEnergy * (Eprice_list[s])
            #Rt = DeviceEnergy*(Eprice_list[s])
            self.count = self.count + 1
            self.R = self.R + R

        '''        if self.done:
            R = self.R
        else:
            R = 0
'''

        done = self.done
        return s_, R, done, self.action

    def render(self):
        time.sleep(0.1)
        self.update()


    def reset(self):
        self.env_list = ['S'] + ['-'] * TotalTime + ['T']  # '----------' our environment
        self.S = 0
        self.R = 0
        self.done = False
        self.action = 'unknown'
        self.count = 0
        return self.S
