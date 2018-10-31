import numpy as np
from agent import agent

class Env:
    def __init__(self):
        self.a = agent()
        self.last_traffic=0

    

    def red_traffic(self,traf_count):
        if traf_count>100:
            traf_count=100
        traf_den = self.getTraDen(traf_count)
        self.last_traffic = traf_den   
        green_time=self.a.on_red(traf_den)
        return green_time


    def green_traffic(self,traf_count):
        if traf_count>100:
            traf_count=100
        traf_den = self.getTraDen(traf_count)
        reward = self.reward(traf_den)
        self.a.on_reward(reward)

    def getTraDen(self,count):
        #Some Logic to get Traffic Density
        return count

    def reward(self,traf_den):
        print(traf_den," ",self.last_traffic)
        if self.last_traffic > traf_den:
            r = 1
        else:
            r = -1
        print("Reward is ",r)
        return r

    def save_model(self):
        self.a.save_model()

    
