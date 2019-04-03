
from collections import deque # double-ended queue
from numpy import random
import simpy
from simpy.util import start_delayed
from envoirment import Env

class Struct(object):
   """
   This simple class allows one to create an object whose attributes are
   initialized via keyword argument/value pairs.  One can update the attributes
   as needed later.
   """
   def __init__(self, **kwargs):
      self.__dict__.update(kwargs)



e = Env(0.8,0.3,0.3)
reward_done = False
# Section 2: Initializations.

random.seed([1, 2, 3])

# Total number of seconds to be simulated:
end_time= (3600* 24 * 1) # seconds in hour * hours * days+

# Cars cars arrive at the traffic light according to a Poisson process with an
# average rate of 0.2 per second:
arrival_rate= 0.2
t_interarrival_mean= 1.0 / arrival_rate

# Traffic light green and red durations:
t_green= 30.0; t_red= 40.0; new_red=0;new_green=0

# The time for a car at the head of the queue to depart (clear the intersection)
# is modeled as a triangular distribution with specified minimum, maximum, and
# mode.
t_depart_left= 1.6; t_depart_mode= 2.0; t_depart_right= 2.4

# Initially, no cars are waiting at the light:
queue= deque()

# Track number of cars:
arrival_count= departure_count= 0

Q_stats= Struct(count=0, cars_waiting=0)
W_stats= Struct(count=0, waiting_time=0.0)


# Section 3: Arrival event.

def arrival():
   """
   This generator functions simulates the arrival of a car.  Cars arrive
   according to a Poisson process having rate `arrival_rate`.  The times between
   subsequent arrivals are i.i.d. exponential random variables with mean

      t_interarrival_mean= 1.0 / arrival_rate
   """
   global arrival_count, env, light, queue

   while True:
      arrival_count+= 1
      
      if light == 'red' or len(queue):

         # The light is red or there is a queue of cars.  ==> The new car joins
         # the queue.  Append a tuple that contains the number of the car and
         # the time at which it arrived:
         queue.append((arrival_count, env.now))
        #  print("Car #%d arrived and joined the queue at position %d at time "
          #  "%.3f." % (arrival_count, len(queue), env.now))

      else:

         # The light is green and no cars are waiting.  ==> The new car passes
         # through the intersection immediately.
        #  print("Car #%d arrived to a green light with no cars waiting at time "
          #  "%.3f." % (arrival_count, env.now))

         # Record waiting time statistics.  (This car experienced zero waiting
         # time, so we increment the count of cars, but the cumulative waiting
         # time remains unchanged.
         W_stats.count+= 1

      # Schedule next arrival:
      yield env.timeout( random.exponential(t_interarrival_mean))


# Section 4: Define event functions.

# Section 4.1: Departure event.

def departure():
   """
   This generator function simulates the 'departure' of a car, i.e., a car that
   previously entered the intersection clears the intersection.  Once a car has
   departed, we remove it from the queue, and we no longer track it in the
   simulation.
   """
   global env, queue

   while True:

      # The car that entered the intersection clears the intersection:
      car_number, t_arrival= queue.popleft()
      # print("Car #%d departed at time %.3f, leaving %d cars in the queue."
        # % (car_number, env.now, len(queue)))

      # Record waiting time statistics:
      W_stats.count+= 1
      W_stats.waiting_time+= env.now - t_arrival
    
      # If the light is red or the queue is empty, do not schedule the next
      # departure.  `departure` is a generator, so the `return` statement
      # terminates the iterator that the generator produces.
      if light == 'red' or len(queue) == 0:
         return

      # Generate departure delay as a random draw from triangular distribution:
      delay= random.triangular(left=t_depart_left, mode=t_depart_mode,
        right=t_depart_right)
      # Schedule next departure:
      yield env.timeout(delay)


# Section 4.2: Light change-of-state event.

def light():
   """
   This generator function simulates state changes of the traffic light.  For
   simplicity, the light is either green or red--there is no yellow state.
   """
   global env, light, new_red , new_green

   while True:


      # Section 4.2.1: Change the light to green.

      light= 'green'
      # print("\nThe light turned green at time %.3f." % env.now)
      # new_green = int(env.now)+t_green
      # If there are cars in the queue, schedule a departure event:
      if len(queue):

         # Generate departure delay as a random draw from triangular
         # distribution:
         delay= random.triangular(left=t_depart_left, mode=t_depart_mode,
           right=t_depart_right)

         start_delayed(env, departure(), delay=delay)
         
      # Schedule event that will turn the light red:
      yield env.timeout(t_green)

      
      # Section 4.2.2: Change the light to red.
      light= 'red'
      new_red = int(env.now)+t_red
      if not reward_done:
        after_Green(len(queue))
      # print("\nThe light turned red at time %.3f."   % env.now)
      
      # Schedule event that will turn the light green:
      yield env.timeout(t_red)
     


# Section 4.3: Schedule event that collects Q_stats.

def monitor():
   """
   This generator function produces an interator that collects statistics on the
   state of the queue at regular intervals.  An alternative approach would be to
   apply the PASTA property of the Poisson process ('Poisson Arrivals See Time
   Averages') and sample the queue at instants immediately prior to arrivals.
   """
   global env, Q_stats,reward_done

   while True:
      Q_stats.count+= 1
      Q_stats.cars_waiting+= len(queue)
      if(int(env.now) == int(new_red) - 6):
         before_Red(len(queue))
         reward_done=False
      if(int(env.now) == int(new_green)-(t_green/2)):
        if(bet_Green(len(queue))):
          reward_done = True
        else:
          reward_done = False
        
      yield env.timeout(1.0)


def before_Red(count):
  global t_green
  t_green=e.red_traffic(count) #call before end of red,so that green timing can be taken from agent
  
  # print("New green is: ",t_green)

def after_Green(count):
  e.green_traffic(count) #call at end of green,so that reward can be given

def bet_Green(count): #check if green time is too much
  return e.between_green(count)

  

print("\nSimulation of Cars Arriving at Intersection Controlled by a Traffic "
  "Light\n\n")

# Initialize environment:
env= simpy.Environment()

# Schedule first change of the traffic light:
env.process(light())

# Schedule first arrival of a car:
t_first_arrival= random.exponential(t_interarrival_mean)
start_delayed(env, arrival(), delay=t_first_arrival)

# Schedule first statistical monitoring event:
env.process(monitor())

# Let the simulation run for specified time:
env.run(until=end_time)

e.save_model()

# Section 6: Report statistics.

print("\n\n      *** Statistics ***\n\n")

print("Mean number of cars waiting: %.3f"
  % (Q_stats.cars_waiting / float(Q_stats.count)))

print("Mean waiting time (seconds): %.3f"
  % (W_stats.waiting_time / float(W_stats.count)))
