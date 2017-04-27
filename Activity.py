# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 14:09:58 2017

@author: diana
"""
from PyQt4 import QtCore, QtGui

from InstructionList import InstructionList

class Activity(QtGui.QWidget):
    #signal emitted when the activity is accpeted/declined
    accepted = QtCore.pyqtSignal(bool, int) #bool is true=accepted, false=declined and int is the index in ActivitiesList
    
    def __init__(self, title='', index=0, instruction_list=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)
        
        self.instruction_list = instruction_list 
        if self.instruction_list == None:
            self.instruction_list = InstructionList()
        
        self.title = title
        self.index = index #this is the index in the ActivitiesList
        self.instruction_list.set_question('Would you like to ' + self.title)
        
        self.big_font = QtGui.QFont()
        self.big_font.setPointSize(36)  
        
        self.small_font = QtGui.QFont()
        self.small_font.setPointSize(20) 
        
        self.grid = QtGui.QGridLayout()
        
        self.title_label = QtGui.QLabel(self.title)
        self.title_label.setFont(self.small_font)
        self.accept_button = QtGui.QPushButton('Send to Patient')
        self.decline_button = QtGui.QPushButton('Decline')
        self.accept_button.clicked.connect(self.accept_activity)
        self.decline_button.clicked.connect(self.decline_activity)
         
        self.grid.addWidget(self.title_label, 0, 0, 1, 2)
        self.grid.addWidget(self.accept_button, 1, 0, 1, 1)
        self.grid.addWidget(self.decline_button, 1, 1, 1, 1)
        self.grid.addWidget(self.instruction_list, 2, 0, 1, 2)
        
        self.setLayout(self.grid)
        
    def accept_activity(self):
        #need to check that all the times are consecutive
        if self.instruction_list.check_times():
            self.accepted.emit(True, self.index)
        else:
            print 'the times are not consecutive'

    def decline_activity(self):
        self.accepted.emit(False, self.index)      
        
    def resize_frame(self, width, height):
        self.width = width
        self.height = height
        #self.instruction_list.resize_frame(self.width, 3*self.height/4)
        self.frame.resize(self.width, self.height)
        
    def get_instruction_list(self):
        return self.instruction_list
        
    def get_title(self):
        return self.title
        
    def get_question(self):
        return self.instruction_list.get_question()
        
    def get_scheduled_reminders(self):
        return self.instruction_list.get_schedule()
        
if __name__ == "__main__":
    import os
    import sys

    app = QtGui.QApplication(sys.argv)
    
    screenShape = QtGui.QDesktopWidget().screenGeometry()
    width = screenShape.width()/3
    height = screenShape.height() - 80   
    
    act = Activity(title='GOing to the mall')
    act.show()
    
    sys.exit(app.exec_())