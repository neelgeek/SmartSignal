import numpy as np

class Env:
    def __init__(self):
        self.states = np.zeros((100,3))

    def print(self):
        print(self.states)


    def getTraDen(self):
        #Some Logic to get Traffic Density
        return 0

    def reward(self):
        '''
        Some Logic to get Reward based on 
        traffic density after the light turn red again
        '''
        return 0
