import numpy as np
import pickle
import os,logging

class agent:

    def __init__(self,eps=0.7, alpha=0.5):
        logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
        self.eps = eps
        self.alpha = 0.3
        if os.path.exists('./statespace.pickle'):
            pickle_in = open('statespace.pickle','rb')
            self.state=pickle.load(pickle_in)
            logging.debug("Loaded Pickle")
        else:
            self.state = np.zeros((101,10),dtype=np.int64)
            logging.debug("Made a new state")
        self.last_action = []
        self.actions=list(range(10,110,10)) # generate a list from 10 to 100
        

    def take_action(self,traf_den):
        r = np.random.rand() # generating a random no. for eps greedy
        if r <= self.eps :
            print("Now Exploring")
            #take random action i.e. explore
            choice = (np.random.choice(10))  #take a random choice from the 6 possile actions
            self.last_action = [traf_den,choice]
            green_time = self.actions[choice]
            
        else :
            print("Now Exploiting")
            #exploit (select the action which has max reward for the given state)
            match_state = self.state[traf_den]
            choice = np.argmax(match_state)
            self.last_action = [traf_den,choice]
            green_time = self.actions[choice] 
            
        return green_time

           
      


    def on_red(self,traf_den):
        #call take_action to take a action
        return self.take_action(traf_den)

    def on_reward(self,reward):
        print("On Reward Called for ",self.last_action)
        if self.last_action:
            self.state[self.last_action[0],self.last_action[1]] += reward
    
    def save_model(self):
        with open('statespace.pickle','wb') as f :
            np.savetxt("statespace.txt",self.state)
            pickle.dump(self.state,f)
            





    

