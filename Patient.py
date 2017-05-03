# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 12:24:15 2017

@author: diana
"""
from PyQt4 import QtCore, QtGui
from collections import deque
import mywidgets

class Patient(mywidgets.BaseFrame):
    
    def __init__(self, width, height, parent=None, account=None, memory_browse=None):
        mywidgets.BaseFrame.__init__(self, width, height, parent)
        
        self.memory_browse = memory_browse
        self.account = account
        
        self.small_font = QtGui.QFont()
        self.small_font.setPointSize(16)     
        
        self.activity_count = 0 #count how many activities are done in a session
        
        #patient screen flags - so we know what is displayed (only display 1 thing at a time)
        self.already_visible = False #flag for patient yes/no question  
        self.is_during_activity = False #set to true when started an instruction list and false when finished
        
        self.activity_queue = deque() #this is the activities that the patient sees
        self.instructions = deque()
        self.times = deque()
        self.current_instruction_index = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.send_instruction)
        
        #create a stack to hold the question frame, memory browse, or reminders
        self.stack = QtGui.QStackedLayout()   
        self.grid.addLayout(self.stack, 0, 0)
        
        #create the question frame
        self.question_frame = QtGui.QFrame()
        self.question_layout = QtGui.QVBoxLayout()
        self.question_frame.setLayout(self.question_layout)
        self.question_label = QtGui.QLabel()
        self.question_label.setFont(self.small_font)
        self.accept_button = QtGui.QPushButton('Yes')
        self.accept_button.clicked.connect(self.accepted_activity)
        self.decline_button = QtGui.QPushButton('No')
        self.decline_button.clicked.connect(self.declined_activity)
        self.hgrid = QtGui.QHBoxLayout()
        self.hgrid.addStretch(1)
        self.hgrid.addWidget(self.accept_button)
        self.hgrid.addWidget(self.decline_button)
        self.hgrid.addStretch(1)
        self.question_layout.addWidget(self.question_label)
        self.question_layout.addLayout(self.hgrid)
        self.question_layout.addStretch(10)
        
        self.stack.addWidget(self.question_frame)
        
        #create a blank frame
        self.blank = QtGui.QFrame()
        self.stack.addWidget(self.blank)
        self.stack.setCurrentWidget(self.blank)
        
        #add the memory browse
        self.grid.addWidget(self.memory_browse, 1, 0)
        
    def send(self, activity):
        '''send the activity to the patient screen'''
        self.activity_queue.append(activity)
        if not self.already_visible and not self.is_during_activity: #This is the first activity sent to them
            #pop the first one off
            self.stack.setCurrentWidget(self.question_frame)
            self.question_label.setText(self.activity_queue[0].get_question())
            self.already_visible = True
            
    def accepted_activity(self):
        instructions, times = self.activity_queue[0].get_scheduled_reminders()
        self.schedule(instructions, times)
        self.activity_queue.popleft()
        if len(self.activity_queue) > 0 and not self.is_during_activity:
            self.question_label.setText(self.activity_queue[0].get_question())
        else:
            #Either start an activity or show random memories
            self.stack.setCurrentWidget(self.blank)
            self.already_visible = False #we ran out of activities to send to the patient
            
    def declined_activity(self):
        print 'patient declined activity tell the algorithm'
        self.activity_queue.popleft()
        if len(self.activity_queue) > 0 and not self.is_during_activity:
            self.question_label.setText(self.activity_queue[0].get_question())
        else:
            #Either start an activity or show random memories
            self.stack.setCurrentWidget(self.blank)
            self.already_visible = False #we ran out of activities to send to the patient
            
    def schedule(self, instructions, times):
        if len(self.times) > 0:
            #check that this doesn't conflict
            end_instruction = self.instructions[-1][-1]
            end_time = end_instruction.get_time()
            if end_time.secsTo(times[0]) < 0:
                msg = QtGui.QMessageBox()
                msg.setIcon(QtGui.QMessageBox.Warning)
                msg.setText("This activity cannot be scheduled because it overlaps with another activity")
                msg.setWindowTitle("Scheduling Error")
                msg.setStandardButtons(QtGui.QMessageBox.Ok)
                msg.exec_()
                print 'these activities overlap'
                return
        #pop it on the queue but for now just set to variables
        self.instructions.append(instructions)
        self.times.append(times)
        
        #calculate the time until the first instruction starts
        current_time = QtCore.QTime.currentTime()
        t = current_time.secsTo(self.times[0][0])
        
        if t < 0:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText("This activity cannot be scheduled because it is past the time")
            msg.setWindowTitle("Scheduling Error")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.exec_()
            self.instructions.popleft()
            self.times.popleft()
            print 'This activity cannot be scheduled because it is past the time'
        else:
            self.timer.start(t*1000)
        
    def send_instruction(self):
        '''send the instruction to the patient'''
        self.timer.stop()
        self.is_during_activity = True
        self.already_visible = False
        #first send the current instruction
        self.instructions[0][self.current_instruction_index].completed.connect(self.completed_instruction)
        self.instructions[0][self.current_instruction_index].canceled.connect(self.canceled_instruction)
        self.stack.addWidget(self.instructions[0][self.current_instruction_index].get_display_frame())
        self.stack.setCurrentWidget(self.instructions[0][self.current_instruction_index].get_display_frame())
            
    def completed_instruction(self):
        #then set the timer again
        self.current_instruction_index += 1
        if self.current_instruction_index >= len(self.instructions[0]):
            self.activity_count += 1
            print 'activity count' + str(self.activity_count)
            self.stack.setCurrentWidget(self.blank)
            self.is_during_activity = False
            self.instructions.popleft()
            self.times.popleft()
            self.current_instruction_index = 0
            #check if there's another activity scheduled
            if len(self.instructions) > 0: #set the timer again
                #calculate the time until the first instruction starts
                current_time = QtCore.QTime.currentTime()
                t = current_time.secsTo(self.times[0][0])
                print 't: ' + str(t)
                if t < 0:
                    #the other activity ran over - just start it now
                    self.timer.start(1000)
                else:
                    self.timer.start(t*1000)
            else: #check if there's activity suggestions
                if not self.already_visible and not self.is_during_activity and len(self.activity_queue) > 0: 
                    #pop the first one off
                    self.stack.setCurrentWidget(self.question_frame)
                    self.question_label.setText(self.activity_queue[0].get_question())
                    self.already_visible = True
        else:
            self.stack.setCurrentWidget(self.blank)
            self.timer.start(self.times[0][self.current_instruction_index])

    def canceled_instruction(self):
        self.timer.stop()
        self.stack.setCurrentWidget(self.blank)
        self.is_during_activity = False
        self.instructions.popleft()
        self.times.popleft()
        self.current_instruction_index = 0
        #check if there's another activity scheduled
        if len(self.instructions) > 0: #set the timer again
            #calculate the time until the first instruction starts
            current_time = QtCore.QTime.currentTime()
            t = current_time.secsTo(self.times[0][0])
            if t < 0:
                #the other activity ran over - just start it now
                self.timer.start(1000)
            else:
                self.timer.start(t*1000)
        else: #check if there's activity suggestions
            if not self.already_visible and not self.is_during_activity and len(self.activity_queue) > 0: 
                #pop the first one off
                self.stack.setCurrentWidget(self.question_frame)
                self.question_label.setText(self.activity_queue[0].get_question())
                self.already_visible = True
        
    def get_activities_completed(self):
        return self.activity_count
        
        
        

if __name__ == "__main__":
    import os
    import sys
    from Activity import Activity

    app = QtGui.QApplication(sys.argv)
    
    screenShape = QtGui.QDesktopWidget().screenGeometry()
    width = screenShape.width()/3
    height = screenShape.height() - 80   
    act = Activity(title='GOing to the mall')
    pat = Patient(width=width, height=height)
    pat.show()
    pat.send(act)
    
#    msg = QtGui.QMessageBox()
#    msg.setIcon(QtGui.QMessageBox.Warning)
#    msg.setText("This activity cannot be scheduled because it is past the time")
#    msg.setWindowTitle("Scheduling Error")
#    msg.setStandardButtons(QtGui.QMessageBox.Ok)
#    msg.exec_()
    
    sys.exit(app.exec_())
        