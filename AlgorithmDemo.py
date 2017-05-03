# -*- coding: utf-8 -*-
"""
Created on Tue May  2 19:09:24 2017

@author: diana
"""
from PyQt4 import QtGui, QtCore

import numpy as np

from collections import deque

import time

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop




#    for i in range(epochs):
#        #print 'round ' + str(i)
#        model, suggest, accept, order = run_single_epoch(model, state, activities, inputs, recent_activities, gamma)
#        suggested[0, i] = suggest
#        accepted_matrix[0, i] = accept
#        
#        #update the labels
#        for j in range(activities):
#            labels[j].setText(str(order[0, j]))
#        time.sleep(1)

#    figure, ratio = plot_results(suggested, accepted, activities)
#    print ratio

#    canvas = FigureCanvas(figure)
#    
#    grid.addWidget(canvas, 0, 0)
#    
class Demo():
    
    def __init__(self):
        self.frame = QtGui.QFrame()
        self.frame.show() 
        self.grid = QtGui.QGridLayout()
        self.frame.setLayout(self.grid)   
        
        #create 25 labels for each activity
        self.labels = []
        for i in range(25):
            self.labels.append(QtGui.QLabel())
            self.labels[-1].setText(str(i))
            self.grid.addWidget(self.labels[-1], i, 1)
        
    def run(self):
            
        self.activities = 25
        self.attributes = 5
        self.create_random_state()
        self.feedback = self.get_patient_feedback(self.activities)
        
        self.create_model(self.state.shape[0], self.state.size)
        
        #create arrays to save the suggested activity and the accepted activity
        self.epochs = 50
        self.suggested_matrix = np.full((1, self.epochs), self.state.shape[0]+10, dtype='int64')
        self.accepted_matrix = np.zeros((1, self.epochs))
        self.inputs = self.state.size
        self.activities = self.state.shape[0]
        self.recent_activities = deque() #cant suggest an activity if it's in the past 5
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.grid.addWidget(self.canvas, 0, 0, 25, 1)
        plt.xlabel('Iteration')
        plt.ylabel('Activity')
        plt.ylim([0, self.activities])
        
        self.t = np.arange(0, self.suggested_matrix.size)
        
        self.gamma = 0.1
            
        self.count = 0    
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.set_labels)
        self.timer.start(1000)
    
    def get_frame(self):
        return self.frame
    
    def create_model(self, activities, inputs):
        self.model = Sequential()
        self.model.add(Dense(inputs, init='lecun_uniform', input_shape=(inputs,)))
        self.model.add(Activation('relu'))
        
        self.model.add(Dense(inputs*2, init='lecun_uniform'))
        self.model.add(Activation('relu'))
        
        self.model.add(Dense(activities, init='lecun_uniform'))
        self.model.add(Activation('linear')) 
        
        rms = RMSprop()
        self.model.compile(loss='mse', optimizer=rms)
        
    def create_random_state(self):
        '''create the state matrix. [activity, attribute, category]'''
        self.state = np.zeros((self.activities, self.attributes, 3))
        for i in range(self.activities):
            for j in range(self.attributes):
                    self.state[i, j, np.random.randint(0, 3)] = 1
       
    def get_patient_feedback(self, activites):
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
        
    def get_simulation_reward_activity(self, action):
        '''only accept certain activities'''
        if self.feedback[0, action] == 1:
            return 10.0
        else:
            return -10.0
        
    def run_single_epoch(self):
        
        qval = self.model.predict(self.state.reshape(1, self.inputs), batch_size=1)
        action = np.argmax(qval)
        while action in self.recent_activities: #directly to the algorithm - don't suggest to patient
            #print 'action was already suggested' + str(action) + ' ' + str(recent_activities)
            reward = 1
            
            newQ = self.model.predict(self.state.reshape(1,self.inputs), batch_size=1)
            maxQ = np.argmax(newQ)
            
            y = np.zeros((1, self.activities))
            y[:] = qval[:]
            update = reward + self.gamma*maxQ
    
            y[0][action] = update
            self.model.fit(self.state.reshape(1,self.inputs), y, batch_size=1, nb_epoch=1, verbose=0)
            
            action = np.random.randint(0, self.activities)
            
        #print 'action was not already suggested' + str(action)
        #pop the suggested activity onto the recent_activities
        self.recent_activities.append(action)
        m = int(np.sum(self.feedback)/3)
        print m
        if len(self.recent_activities) > m:
            self.recent_activities.popleft()
        reward = self.get_simulation_reward_activity(action)
        
        newQ = self.model.predict(self.state.reshape(1,self.inputs), batch_size=1)
        maxQ = np.argmax(newQ)
        
        y = np.zeros((1, self.activities))
        y[:] = qval[:]
        update = reward + self.gamma*maxQ
    
        y[0][action] = update
        self.model.fit(self.state.reshape(1,self.inputs), y, batch_size=1, nb_epoch=1, verbose=0)
        
        #update the matrices of the saved values
        accepted = 0
        if reward > 0.0:
            accepted = 1
        
        return action, accepted, np.argsort(qval)
        
    def plot_results(self):
        
        for i in range(self.t.size):
            if self.accepted_matrix[0, i]:
                self.figure.axes[0].plot(self.t[i], self.suggested_matrix[0, i], 'o', color='green')
            else:
                self.figure.axes[0].plot(self.t[i], self.suggested_matrix[0, i], 'o', color='red')
        
        #return figure, np.sum(self.accepted_matrix)/sugg

        
    
    def set_labels(self):
    
        suggest, accept, order = self.run_single_epoch()
        self.suggested_matrix[0, self.count] = suggest
        self.accepted_matrix[0, self.count] = accept
        
        ratio = np.sum(self.accepted_matrix)/float(self.count+1)
        print ratio

        #update the labels
        for j in range(25):
            self.labels[j].setText(str(order[0, j]))
        self.plot_results()
        self.count += 1
        if self.count >= self.epochs:
            self.timer.stop()


if __name__ == "__main__":   
    import sys
    
    app = QtGui.QApplication(sys.argv)  

    d = Demo()   
    f = d.get_frame()
    f.show()
    d.run()
    
    sys.exit(app.exec_())
