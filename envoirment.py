import numpy as np
from agent import agent

class Env:
    # def __init__(self):
    
    a = agent()

    def red_traffic(self,traf_count):
        traf_den = self.getTraDen(traf_count)
        green_time=self.a.on_red(traf_den)
        return green_time


    def green_traffic(self,traf_count):
        traf_den = self.getTraDen(traf_count)
        reward = self.reward(traf_den)
        self.a.on_reward(reward)

    def getTraDen(self,count):
        #Some Logic to get Traffic Density
        return 0

    def reward(self,traf_den):
        '''
        Some Logic to get Reward based on 
        traffic density after the light turn red again
        '''
        return 0

    def save_model():
        #Logic to save the statespace using Pickle

    
