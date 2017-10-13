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
        self.done = False
        self.action = 'off'

    def update(self):
        s = self.S
        if self.done:
            self.env_list[s+1] = 'D'
            interaction = ''.join(self.env_list)
            print('\r{}'.format(interaction), end='')
            time.sleep(FRESH_TIME)
            over = 'GameOver,reward = %s' %(self.R)
            time.sleep(FRESH_TIME)
            print('\n ')
            print(over)
            time.sleep(FRESH_TIME)
            #print('\r                                ', end='')
        else:
            self.env_list[s+1] = '0'
            interaction = ''.join(self.env_list)
            print('\r{}'.format(interaction), end='')
            time.sleep(FRESH_TIME)

    def step(self, action):
        # This is how agent will interact with the environment
        s = self.S
        s_current = s
        if action == 'off':
            self.action = 'off'
            if s == TotalTime - Duration:  # terminate: reach to the end of a day
                R = DeviceEnergy*(sum(Eprice_list[s:]))
                self.done = True
                self.action = 'on'
                s_ = "Terminal"
                #self.S = s + 1
                self.R = R
            else:
                s_ = s + 1           # Just move on
                R = 0
                #R = sum(Eprice_list[s+1:][Eprice_list[s+1:].argsort()[:3]])
                self.done = False
                #self.S = s_
                self.R = R
        else:
            self.action = 'on'
            R = DeviceEnergy*(sum(Eprice_list[s_current:s_current+Duration]))
            self.done = True
            #self.S = s + 1
            self.R = R
            s_ = "Terminal"
        done = self.done
        return s_, R, done

    def render(self):
        time.sleep(0.5)
        self.update()


    def reset(self):
        self.env_list = ['S'] + ['-'] * TotalTime + ['T']  # '----------' our environment
        self.S = 0
        self.R = 0
        self.done = False
        self.action = 'off'
        return self.S
