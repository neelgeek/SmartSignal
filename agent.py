import numpy as np
from envoirment import Env

class agent:

    def __init__(self,eps=0.1, alpha=0.5):
        self.eps = eps
        self.alpha = 0.5
        self.state_history =[]
        self.state = np.zeros((100,10))
        self.last_action = []
        self.actions=list(range(10,110,10)) # generate a list from 10 to 100


    def take_action(self,traf_den):
          r = np.random.rand()
        if r < self.eps :
            #take random action i.e. explore
            choice = (np.random.choice(10))  #take a random choice from the 6 possile actions
            self.last_action = [traf_den,choice]
            red_time = self.actions[choice]
            
        else :
            #exploit (select the action which has max reward for the given state)
            match_state = self.state[traf_den]
            choice = np.argmax(match_state)
            self.last_action = [traf_den,choice]
            red_time = self.actions[choice] 
            
        
        return red_time

           
      


    def on_red(self,traf_den):
        #call take_action to take a action
        return take_action(traf_den)

    def on_reward(self,reward):
        self.state[self.last_action[0],self.last_action[1]] += reward




    
