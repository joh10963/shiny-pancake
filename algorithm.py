# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 14:43:49 2017

@author: diana
"""

import numpy as np

from collections import deque

import math

import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop

def create_random_state(activities, attributes):
    '''create the state matrix. [activity, attribute, category]'''
    state = np.zeros((activities, attributes, 3))
    for i in range(activities):
        for j in range(attributes):
                state[i, j, np.random.randint(0, 3)] = 1
    
    return state
   
def get_patient_feedback(activites):
    '''Ask the patient which activity they like better
    1 or 0 for each activity
    1: they like it 
    0: they don't like it
    '''
    #they like all the activities
    output = np.zeros((1, activites))
    
    #I'm just gonna say they like the first 10 of the activities
    output[0, 0:10] = 1
    
    return output
    
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
    
def get_simulation_reward_activity(action):
    '''only accept certain activities'''
    if action in range(10):
        return 10.0
    else:
        return -10.0

def get_simulation_reward_attribute(action, state):
    '''Only accept Attribute 3 100'''
    if state[action, 2, 0] == 1:
        return 1.0
    else:
        return -1.0

def get_training_reward(action, feedback, state):
    '''try to simulate a real-life person'''
    if feedback[0, action] == 1: #this means they said they liked the activity
    #if state[action, 2, 0] == 1:
        prob = np.random.normal(0.6, 0.2)
    else:
        prob = np.random.normal(0.4, 0.2)
    
    #use the probability to simulate if they pick the activity or not
    stop = int(prob*100.0)
    draw = np.zeros((1, 100))
    draw[0, 0:stop] = 1
    pick = draw[0, np.random.randint(0, 100)]
    if pick == 0:
        return -1.0
    if pick == 1:
        return 1.0

def train_model(model, state, feedback, epochs=1):
    '''train the model, preference is a 1x4 vector indicating the preference of what will be selected'''
    
    inputs = state.size
    activities = state.shape[0]
    
    suggested = 0
    accepted = 0
    
    gamma = 0.4
    epsilon = 1
    threshold = 0.5
    
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
                
            reward = get_training_reward(action, feedback, state)
            
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

            if accepted > activities and accepted/float(suggested) > threshold or suggested > 1000:
                done = True
#                print accepted/float(suggested)
#                print action
#                print 'done'
#                print 'number of iterations = ' + str(suggested)
    return model
        
def run_simulation(model, state):
    
    #create arrays to save the suggested activity and the accepted activity
    epochs = 50
    suggested = np.full((1, epochs), state.shape[0]+10)
    accepted = 0
    accepted_matrix = np.zeros((1, epochs))
    inputs = state.size
    activities = state.shape[0]
    recent_activities = deque() #cant suggest an activity if it's in the past 5
    
    gamma = 0.1
    
    i = 0
    for i in range(epochs):
        #print 'round ' + str(i)
        qval = model.predict(state.reshape(1, inputs), batch_size=1)
        action = np.argmax(qval)
        while action in recent_activities: #directly to the algorithm - don't suggest to patient
            #print 'action was already suggested' + str(action) + ' ' + str(recent_activities)
            reward = 1
            
            newQ = model.predict(state.reshape(1,inputs), batch_size=1)
            maxQ = np.argmax(newQ)
            
            y = np.zeros((1, activities))
            y[:] = qval[:]
            update = reward + gamma*maxQ
    
            y[0][action] = update
            model.fit(state.reshape(1,inputs), y, batch_size=1, nb_epoch=1, verbose=0)
            
            action = np.random.randint(0, activities)
            
        #print 'action was not already suggested' + str(action)
        #pop the suggested activity onto the recent_activities
        recent_activities.append(action)
        if len(recent_activities) > 3:
            recent_activities.popleft()
        reward = get_simulation_reward_activity(action)
        #reward = get_simulation_reward_attribute(action, state)
        
        #update the matrices of the saved values
        suggested[0, i] = action
        if reward > 0.0:
            accepted += 1
            accepted_matrix[0, i] = 1
        
        newQ = model.predict(state.reshape(1,inputs), batch_size=1)
        maxQ = np.argmax(newQ)
        
        y = np.zeros((1, activities))
        y[:] = qval[:]
        update = reward + gamma*maxQ

        y[0][action] = update
        model.fit(state.reshape(1,inputs), y, batch_size=1, nb_epoch=1, verbose=0)
        
        i += 1
            
    return suggested, accepted_matrix
    

def patient_accepts(action):
    #This will only accept action=0 or action=1
    if action == 0 or action==1:
        return True
    return False
    


def random_simulation(activites):
    '''only accepts activity 3 and 6'''
    suggested_matrix = np.random.randint(0, activites, size=(1,50))
    accepted_matrix = np.zeros(suggested_matrix.shape)
    
    for i in range(suggested_matrix.size):
        if suggested_matrix[0, i] == 10:
            accepted_matrix[0, i] = 1
    
    return suggested_matrix, accepted_matrix

def random_simulation_attributes(state, activities):
    '''only accepts attribute 2 100'''
    suggested_matrix = np.random.randint(0, activities, size=(1,50))
    accepted_matrix = np.zeros(suggested_matrix.shape)
    
    for i in range(suggested_matrix.size):
        suggested_activity = suggested_matrix[0, i]
        if  state[suggested_activity, 2, 0] == 1:
            accepted_matrix[0, i] = 1
    
    return suggested_matrix, accepted_matrix

def window(suggested, accepted, num_acts, window_length=10.0):
    windows = int(math.ceil(suggested.size/window_length))
    output = np.zeros((1, windows))
    
    for i in range(windows):
        j = 0
        sugg = 0
        while j < window_length and i*window_length+j < suggested.size:
            if accepted[0, int(i*window_length+j)] == 1:
                output[0, i] += 1
            if suggested[0, int(i*window_length+j)] < num_acts:
                sugg += 1
            j += 1
        output[0, i] = output[0, i]/float(sugg)

    return output            


def plot_results(suggested_matrix, accepted_matrix, activities, attributes=False, state=None):
    plt.figure()
    
    time = np.arange(0, suggested_matrix.size)
    sugg = 0
    
    for i in range(time.size):
        if suggested_matrix[0, i] < activities:
            sugg += 1
        if accepted_matrix[0, i]:
            plt.plot(time[i], suggested_matrix[0, i], 'o', color='green')
        else:
            plt.plot(time[i], suggested_matrix[0, i], 'o', color='red')
            
    
    plt.xlabel('Iteration')
    plt.ylabel('Activity')
    plt.ylim([0, activities])
    
    if attributes:
        #draw a horizontal line for the accepted attributes
        for act in range(activities):
            if state[act, 2, 0] == 1: #accepted activity
                plt.plot([0, 50], [act, act], '-', color='blue')
    
    plt.show()
    
    return np.sum(accepted_matrix)/sugg
    
def main2():
    activities = 25
    attributes = 5
    state = create_random_state(activities, attributes)
    feedback = get_patient_feedback(activities)

    #Random simulation
#    suggested, accepted = random_simulation(activities)
#    plot_results(suggested, accepted, activities)
#    
#    windowed_result = np.zeros((50, 10))    
#    
#    for i in range(50):
#        print 'starting round ' + str(i)
#        suggested, accepted = random_simulation(activities)
#        #plot_results(suggested, accepted, activities)
#        output = window(suggested, accepted, 5.0)
#        windowed_result[i] = output
#    
#    plt.figure()
#    time = np.arange(0, windowed_result.shape[1])
#    avg_window = np.mean(windowed_result, axis=0)
#    plt.plot(time, avg_window, 'o', color='blue')
#    plt.xlabel('Window')
#    plt.ylabel('Percent Accepted')
#    plt.ylim([0, 1])
#    plt.show()
    
    #Show a random simulation
#    suggested, accepted = random_simulation_attributes(state, activities)
#    plot_results(suggested, accepted, activities, attributes=True, state=state)
        
#    windowed_result = np.zeros((50, 10))    
#    
#    for i in range(50):
#        print 'starting round ' + str(i)
#        suggested, accepted = random_simulation_attributes(state, activities)
#        #plot_results(suggested, accepted, activities)
#        output = window(suggested, accepted, 5.0)
#        windowed_result[i] = output
#    
#    plt.figure()
#    time = np.arange(0, windowed_result.shape[1])
#    avg_window = np.mean(windowed_result, axis=0)
#    plt.plot(time, avg_window, 'o', color='blue')
#    plt.xlabel('Window')
#    plt.ylabel('Percent Accepted')
#    plt.ylim([0, 1])
#    plt.show()

    #Test that the training is appropriate

    #Without training
#    model = create_model(state.shape[0], state.size)
#    suggested, accepted = run_simulation(model, state)
#    plot_results(suggested, accepted, activities)
    
    #with training
#    model = create_model(state.shape[0], state.size)
#    train_model(model, state, feedback)
#    suggested, accepted = run_simulation(model, state)
#    plot_results(suggested, accepted, activities)

    #Show that the predictions get better over time
    windowed_result = np.zeros((50, 10))    
    
    for i in range(50):
        print 'starting round ' + str(i)
        model = create_model(state.shape[0], state.size)
        #train_model(model, state, feedback)
        suggested, accepted = run_simulation(model, state)
        #print suggested
        #ratio = plot_results(suggested, accepted, activities)
        #print ratio
        output = window(suggested, accepted, activities, 5.0)
        windowed_result[i] = output
    
    plt.figure()
    time = np.arange(0, windowed_result.shape[1])
    avg_window = np.nanmean(windowed_result, axis=0)
    plt.plot(time, avg_window, 'o', color='blue')
    plt.xlabel('Window')
    plt.ylabel('Percent Accepted')
    plt.ylim([0, 1])
    plt.show()
    
    
if __name__=='__main__':
    main2()
        