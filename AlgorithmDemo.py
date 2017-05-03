# -*- coding: utf-8 -*-
"""
Created on Tue May  2 19:09:24 2017

@author: diana
"""
from PyQt4 import QtGui, QtCore

import numpy as np

from collections import deque

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop

   
class Demo():
    
    def __init__(self):
        self.frame = QtGui.QFrame()
        #self.frame.show() 
        self.grid = QtGui.QGridLayout()
        self.frame.setLayout(self.grid)
        
        self.green_p = QtGui.QPalette()
        self.green_p.setColor(QtGui.QPalette.Foreground, QtCore.Qt.green)
        self.red_p = QtGui.QPalette()
        self.red_p.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
        
        #create 25 labels for each activity
        self.labels = []
        for i in range(25):
            self.labels.append(QtGui.QLabel())
            self.labels[-1].setText('Activity ' + str(i))
            self.grid.addWidget(self.labels[-1], i, 1)
            
        self.activities = 25
        self.attributes = 3
        self.create_random_state()
        
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
        plt.xlabel('Time')
        plt.ylabel('Activity')
        plt.ylim([0, self.activities])
        
        self.t = np.arange(0, self.suggested_matrix.size)
        
        self.gamma = 0.1
        self.epsilon = 1.0
            
        self.count = 0    
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.set_labels)
         
        #create a frame to get the user input
        self.qframe = QtGui.QWidget()
        self.qgrid = QtGui.QGridLayout()
        self.qframe.setLayout(self.qgrid)
        
        self.l1 = self.attributes*[None] #labels for attributes
        for i in range(self.attributes):
            self.l1[i] = QtGui.QLabel('Attribute ' + str(i))
            self.qgrid.addWidget(self.l1[i], 0, i+3)
        
        self.cb = self.activities*[None]
        self.ls = self.activities*[None]
        self.dd = self.activities*[None] #dropdowns [activity, attribute]
        for i in range(self.activities):
            self.cb[i] = QtGui.QCheckBox()
            self.ls[i] = QtGui.QLabel()
            self.ls[i].setText('Activity ' +str(i))
            
            self.qgrid.addWidget(self.cb[i], i+2, 0)
            self.qgrid.addWidget(self.ls[i], i+2, 1)
            
            self.dd[i] = self.attributes*[None]
            for j in range(self.attributes):
                self.dd[i][j] = QtGui.QComboBox()
                self.dd[i][j].addItems(['0', '1', '2'])
                self.dd[i][j].setCurrentIndex(np.random.randint(0, 3))
                
                self.qgrid.addWidget(self.dd[i][j], i+2, j+3)
                
        self.run_but = QtGui.QPushButton('Run')
        self.run_but.clicked.connect(self.get_input)
        self.qgrid.addWidget(self.run_but, self.activities+3, 0, 1, self.attributes+3)
        
        #check 10 activities
        for i in range(10):
            self.cb[i].setChecked(True)
            
        self.qframe.show()
         
    def get_input(self):
        '''set self.feedback based on check buttons'''
        self.feedback = np.zeros((1, self.activities))
        for i in range(self.activities):
            if self.cb[i].isChecked():
                self.feedback[0, i] = 1
                self.labels[i].setPalette(self.green_p)
            else:
                self.labels[i].setPalette(self.red_p)
        
        self.qframe.hide()
        self.run()
        
    def run(self):
        self.frame.show()
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
            
            a = qval.argsort()
            print a
            index = np.random.randint(0, int(self.activities/2))
            print index
            action = a[0, index]
            
        #print 'action was not already suggested' + str(action)
        #pop the suggested activity onto the recent_activities
        self.recent_activities.append(action)
        if len(self.recent_activities) > 2:
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
        
        order = qval.argsort()
        return action, accepted, order
        
    def plot_results(self):
        
        for i in range(self.t.size):
            if self.accepted_matrix[0, i]:
                self.figure.axes[0].plot(self.t[i], self.suggested_matrix[0, i], 'o', color='green')
            else:
                self.figure.axes[0].plot(self.t[i], self.suggested_matrix[0, i], 'o', color='red')
    
    def set_labels(self):
    
        suggest, accept, order = self.run_single_epoch()
        self.suggested_matrix[0, self.count] = suggest
        self.accepted_matrix[0, self.count] = accept
        
        ratio = np.sum(self.accepted_matrix)/float(self.count+1)
        print ratio

        #update the labels
        i = 0 #counter for label position
        for j in reversed(range(25)):
            self.labels[i].setText('Activity ' + str(order[0, j]))
            if self.feedback[0, order[0, j]] == 1: #green
                self.labels[i].setPalette(self.green_p)
            else:
                self.labels[i].setPalette(self.red_p)
            i += 1
        self.plot_results()
        self.count += 1
        if self.count >= self.epochs:
            self.timer.stop()


if __name__ == "__main__":   
    import sys
    
    app = QtGui.QApplication(sys.argv)  

    d = Demo()   
    #f = d.get_frame()
    #f.show()
    #d.run()
    
    sys.exit(app.exec_())
