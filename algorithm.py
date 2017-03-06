# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 14:43:49 2017

@author: diana
"""

import numpy as np

import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop

def create_state(activities, attributes):
    '''create the state matrix. [activity, attribute]'''
#    state = np.zeros((4, 5))
    state = np.zeros((activities, attributes))
    for i in range(activities):
        for j in range(attributes):
            if np.random.random() > 0.5:
                state[i, j] = 1
    
    return state
    
def create_preference(activities):
    preference = np.zeros((1, activities))
    for i in range(activities):
        if np.random.random() > 0.5:
            preference[0, i] = 1
    return preference
    
def create_model(activities, inputs):
    model = Sequential()
    model.add(Dense(inputs, init='lecun_uniform', input_shape=(inputs,)))
    model.add(Activation('relu'))
    
#    model.add(Dense(inputs*2, init='lecun_uniform'))
#    model.add(Activation('relu'))
    
    model.add(Dense(activities, init='lecun_uniform'))
    model.add(Activation('linear')) 
    
    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    return model
    
def get_reward(state, action, preference):
    '''positive reward for action=0 or action==1, negative reward for everything else'''
    # for now we only care about the first attribute
    output = 0
    for i in range(preference.size):
        if state[action][i] == preference[0, i]:
            output += 1
    return output
#    if state[action][0] == preference[0]:
#        return 10.0
#    return 0.0

def train_model(model, state, preference):
    '''train the model, preference is a 1x4 vector indicating the preference of what will be selected'''

    epochs = 50
    
    inputs = state.size
    activities = state.shape[0]
    
    suggested = 0
    accepted = 0
    
    gamma = 0.25
    epsilon = 1
    threshold = 0.75
    
    for i in range(epochs):
        
        done = False
        suggested = 0
        accepted = 0
        
        while not done:
            qval = model.predict(state.reshape(1, inputs), batch_size=1)
            if np.random.random() < epsilon:
                action = np.random.randint(0, activities)
            else:
                action = np.argmax(qval)
                
            reward = get_reward(state, action, preference)
            
            #update the matrices of the saved values
            suggested += 1
            if reward > 0:
                accepted += 1
            
            newQ = model.predict(state.reshape(1,inputs), batch_size=1)
            maxQ = np.argmax(newQ)
            
            y = np.zeros((1, activities))
            y[:] = qval[:]
            update = reward + gamma*maxQ
    
            y[0][action] = update
            model.fit(state.reshape(1,inputs), y, batch_size=1, nb_epoch=1, verbose=0)
            
            if epsilon > 0.1:
                epsilon -= 0.001

            if accepted > 10 and accepted/float(suggested) > threshold:
                done = True
                print accepted/float(suggested)
                print action
                print 'done'
                print 'number of iterations = ' + str(suggested)
    return model
        
def run_simulation(model, state, preference):
    
    #create arrays to save the suggested activity and the accepted activity
    epochs = 50
    suggested = np.zeros((1, epochs))
    accepted = 0
    inputs = state.size
    activities = state.shape[0]
    
    gamma = 0.25
    last_action = -1

    for i in range(epochs):
        qval = model.predict(state.reshape(1, inputs), batch_size=1)
        action = np.argmax(qval)
        if action == last_action:
            q = np.array(qval, copy=True)
            q[0, action] = 0
            action = np.argmax(q)
        last_action = action
        reward = get_reward(state, action, preference)
        
        #update the matrices of the saved values
        suggested[0, i] = action
        if reward > 0.0:
            accepted += 1
        
        newQ = model.predict(state.reshape(1,inputs), batch_size=1)
        maxQ = np.argmax(newQ)
        
        y = np.zeros((1, activities))
        y[:] = qval[:]
        update = reward + gamma*maxQ

        y[0][action] = update
        model.fit(state.reshape(1,inputs), y, batch_size=1, nb_epoch=1, verbose=0)
            
    return accepted, suggested
    
def suggest_activity(state, action):
    '''action is the state to suggest, right now it doesn't change the state'''    
#    if patient_accepts(action):
#        state[0][action] = state[0][action] + 1 #update the frequency
#    state[1][action] = state[1][action] + 1 #update the availability
    
    return state

def patient_accepts(action):
    #This will only accept action=0 or action=1
    if action == 0 or action==1:
        return True
    return False
    


def rand_simulate():
    
    state = create_state()
    rand_suggestions = np.zeros((1, 10))
    
    for i in range(rand_suggestions.size):
        rand_action = np.random.randint(0, 5)
        state = suggest_activity(state, rand_action)
        rand_suggestions[0][i] = rand_action
        
    print rand_suggestions
    print state

    


def plot_results(suggested_matrix):
    plt.figure()
    
    time = np.zeros((1, suggested_matrix.size))
    for i in range(time.size):
        time[0, i] = i
        
    plt.plot(time, suggested_matrix, 'o-')
    
    plt.xlabel('Iteration')
    plt.ylabel('Activity')
    
    plt.show()
    

def main():
    activities = 10
    attributes = 10
    #make up initial data
    preference = create_preference(activities)
    state = create_state(activities, attributes)
    print state
    print preference
    #create the neural network
    model = create_model(state.shape[0], state.size)
    #train the network
    model = train_model(model, state, preference)
    #run simulation
    accepted, suggested = run_simulation(model, state, preference)
    print np.sum(accepted)/float(50)
    plot_results(suggested)
    #plot the results
    
if __name__=='__main__':
    main()
        