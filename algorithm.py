# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 14:43:49 2017

@author: diana
"""

import numpy as np

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop

def create_state():
    '''create the state matrix'''
    state = np.zeros((2, 5))
    state = np.array([[2, 0, 1, 2, 3],
                      [3, 4, 4, 10, 16]])
    
    return state
    
def suggest_activity(state, action):
    '''action is the state to suggest'''    
    if patient_accepts(action):
        state[0][action] = state[0][action] + 1 #update the frequency
    state[1][action] = state[1][action] + 1 #update the availability
    
    return state

def patient_accepts(action):
    #This will only accept the first activity
    if action == 0:
        return True
    return False
    
def get_reward(state):
    '''calculate the frequency:availability ratio'''
    reward = 0
    for i in range(5):
        reward += state[0][i]/state[1][i]
    return reward

def rand_simulate():
    
    state = create_state()
    rand_suggestions = np.zeros((1, 10))
    
    for i in range(rand_suggestions.size):
        rand_action = np.random.randint(0, 5)
        state = suggest_activity(state, rand_action)
        rand_suggestions[0][i] = rand_action
        
    print rand_suggestions
    print state
    
def create_model():
    model = Sequential()
    model.add(Dense(5, init='lecun_uniform', input_shape=(10,)))
    model.add(Activation('relu'))
    
    model.add(Dense(15, init='lecun_uniform'))
    model.add(Activation('relu'))
    
    model.add(Dense(5, init='lecun_uniform'))
    model.add(Activation('linear')) 
    
    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    return model
    
def run_simulation():
    #make the state and the ANN
    state = create_state()
    model = create_model()
    
    gamma = 0.25
    epsilon = 1
    
    for i in range(50):
        qval = model.predict(state.reshape(1, 10), batch_size=1)
        if np.random.random() < epsilon:
            action = np.random.randint(0, 5)
        else:
            action = np.argmax(qval)
        
        new_state = suggest_activity(state, action)
        reward = get_reward(new_state)
        
        newQ = model.predict(new_state.reshape(1,10), batch_size=1)
        maxQ = np.argmax(newQ)
        
        y = np.zeros((1, 5))
        y[:] = qval[:]
        update = reward + gamma*maxQ

        y[0][action] = update
        model.fit(state.reshape(1,10), y, batch_size=1)
        state = new_state
        
        if epsilon > 0.1:
            epsilon -= 0.001
            
    print state
    
if __name__=='__main__':
#    rand_simulate()
    run_simulation()
        