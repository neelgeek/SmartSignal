import numpy as np
from agent import agent

class Env:
    def __init__(self,ep,a,g):
        self.a = agent(ep,a,g)
        self.last_traffic=0

    

    def red_traffic(self,traf_count):
        traf_den = self.getTraDen(traf_count)
        self.last_traffic = traf_den   
        green_time=self.a.on_red(traf_den)
        return green_time


    def green_traffic(self,traf_count):
        
        traf_den = self.getTraDen(traf_count)
        reward = self.reward(traf_den)
        self.a.on_reward(reward)

    def between_green(self,traf_count):
        traf_den = self.getTraDen(traf_count)
        if traf_den < self.last_traffic/3:
            r=-1
            # print("Negative Reward assigned")
            self.a.on_reward(r)
            return True
        else:
            return False


    def getTraDen(self,count):
        #Some Logic to get Traffic Density
        if count>100:
            count=100
        return count

    def reward(self,traf_den):
        #print(traf_den," ",self.last_traffic)
        if traf_den < self.last_traffic :
            r = 1
        else:
            r = -1
        # print("Reward is ",r)
        return r

    def save_model(self):
        self.a.save_model()

    
