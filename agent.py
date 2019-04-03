import numpy as np
import pickle
import os,logging

class agent:

    def __init__(self,eps,alpha,gamma):
        logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
        self.eps = eps
        self.alpha = alpha 
        self.gamma = gamma
        #self.state = state = np.zeros((101,10),dtype=np.int64)
        self.last_action = []
        self.actions=list(range(10,110,10)) # generate a list from 10 to 100
        self.Qmat =  self.load_Q()
        self.Prev_Q = []
        self.QRew = 0
        
    def take_action(self,traf_den):
        # self.Prev_Q = self.CQ
        r = np.random.rand() # generating a random no. for eps greedy
        if r <= self.eps :
            # print("Now Exploring")
            #take random action i.e. explore
            choice = (np.random.choice(10))  #take a random choice from the 6 possile actions
            green_time = self.actions[choice]
            self.Prev_Q = [traf_den,choice]
        else :
            # print("Now Exploiting")
            #exploit (select the action which has max reward for the given state)
            match_state = self.Qmat[traf_den]
            choice = np.argmax(match_state)
            green_time = self.actions[choice] 
            self.Prev_Q = [traf_den,choice]
        return green_time

    def on_red(self,traf_den):
        #call take_action to take a action
        if self.Prev_Q:
            self.update_Q(traf_den)
        return self.take_action(traf_den)

    def on_reward(self,reward):
        # print("On Reward Called for ",self.last_action)
        self.QRew = reward

    def update_Q(self,new_state):
        Q_cur = self.Qmat[self.Prev_Q[0],self.Prev_Q[1]]
    
        Q_cur=Q_cur + self.alpha*(self.QRew+(self.gamma* np.max(self.Qmat[new_state]))-Q_cur)  
       
        self.Qmat[self.Prev_Q[0],self.Prev_Q[1]] =Q_cur
        return 0
    
    
    def load_Q(self):
        if os.path.exists('./models/Qmat.pickle'):
            pickle_in = open('./models/Qmat.pickle','rb')
            state=np.matrix(pickle.load(pickle_in),dtype=np.float)
            logging.debug("Loaded Pickle")
        else:
            state = np.zeros((101,10),dtype=np.float)
            logging.debug("Made a new state")
        return state



    
    def save_model(self):
        # with open('./models/statespace.pickle','wb') as f :
        #     np.savetxt("./models/statespace.txt",self.state)
        #     pickle.dump(self.state,f)
        # print(self.Qmat)
        
        with open('./models/Qmat.pickle','wb') as f:
            np.savetxt("./models/Qmat.txt",self.Qmat)
            pickle.dump(self.Qmat,f,protocol=2)
        print("Pickle Saved")
            
    # def load_model(self): 
    #     if os.path.exists('./models/statespace.pickle'):
    #         pickle_in = open('./models/statespace.pickle','rb')
    #         state=pickle.load(pickle_in)
    #         logging.debug("Loaded Pickle")
    #     else:
    #         state = np.zeros((101,10),dtype=np.int64)
    #         logging.debug("Made a new state")
    #     return state