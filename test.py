import numpy as np 

a =np.array([[0,1,1,1,1],[1,2,3,4,5]])
actions=list(range(10,110,10))
b = [1,2,1,121,12143]
a[0]=b
print(actions[np.argmax(a[0])])

# while True:
#     print(np.random.choice(10))
