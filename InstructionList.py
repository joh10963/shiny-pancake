# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 13:04:04 2017

@author: diana
"""
from PyQt4 import QtCore, QtGui
from Instruction import Instruction

class InstructionList(QtGui.QWidget):
    '''A list of the step-by-step instruction objects'''
    def __init__(self, instructions=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)
        
        if instructions == None:
            self.instructions = list()
        else:
            self.instructions = instructions
        if len(self.instructions) < 1:
            print 'appending instruction'
            self.instructions.append(Instruction())
        
        self.grid = QtGui.QFormLayout()
        
        self.question_entry = QtGui.QLineEdit()
        self.grid.addRow('Question for patient', self.question_entry)
        
        self.tab_widget = QtGui.QTabWidget()
        self.grid.addRow(self.tab_widget)
        
        for i in range(len(self.instructions)): 
            print 'added to tab widget: ' + str(self.instructions[i])
            self.tab_widget.addTab(self.instructions[i].get_edit_frame(), str(i))
        
        self.delete_button = QtGui.QPushButton('Delete Instruction')
        self.delete_button.clicked.connect(self.delete_instruction)  
        
        self.add_button = QtGui.QPushButton('Add Instruction') 
        self.add_button.clicked.connect(self.add_instruction)

        self.grid2 = QtGui.QGridLayout()
        self.grid2.addWidget(self.add_button, 0, 0)
        self.grid2.addWidget(self.delete_button, 0, 1)
        self.grid.addRow(self.grid2)
        
        self.doo_but = QtGui.QPushButton('doo')
        self.doo_but.clicked.connect(self.doo)
        self.grid.addRow(self.doo_but)
            
        self.setLayout(self.grid)
    
    def doo(self):
        instructs, time = self.get_schedule()
        print instructs
        print time
    
    def get_display_frame(self):
        return self.display_frame
   
    def add_instruction(self):
        if len(self.instructions) > 1:
            previous_time = self.instructions[-1].get_time()
            previous_date = self.instructions[-1].get_date()
        else:
            previous_time = None
            previous_date = None
        self.instructions.append(Instruction(time=previous_time, date=previous_date))
        self.tab_widget.addTab(self.instructions[-1].get_edit_frame(), str(self.tab_widget.count()))
        self.tab_widget.setCurrentWidget(self.instructions[-1].get_edit_frame())
        
    def resize_frame(self, width, height):
        self.width = width
        self.height = height
        #for instr in self.instructions:
            #instr.resize_frame(self.width, self.height/4)
        self.resize(self.width, self.height)
    
    def get_question(self):
        return self.question_entry.text()
        
    def set_question(self, text):
        self.question_entry.setText(text)
    
    def get_instructions(self):
        return self.instructions
    
    def delete_instruction(self):
        '''delete the current instruction'''
        cur = self.tab_widget.currentIndex()
        end = self.tab_widget.count()
        self.tab_widget.removeTab(cur)
        del self.instructions[cur]
        #rename the tabs following the deleted tab
        for t in range(cur, end):
            self.tab_widget.setTabText(t, str(t))
        
    def get_schedule(self):
        '''return a list of instructions and the QTimes to be used by a higher class to send reminders'''
        times = [self.instructions[0].get_time()]
        for i in range(1, len(self.instructions)):
            #calculate the time between the previous time and the next time
            previous_time = self.instructions[i-1].get_time()
            current_time = self.instructions[i].get_time()
            seconds = previous_time.secsTo(current_time)
            times.append(seconds*1000)
            
        return self.instructions, times
        
    def check_times(self):
        '''check that the times are consecutive. return true if ok, return false otherwise'''
        output = True
        for i in range(1, len(self.instructions)):
            #calculate the time between the previous time and the next time
            previous_time = self.instructions[i-1].get_time()
            current_time = self.instructions[i].get_time()
            seconds = previous_time.secsTo(current_time)
            if seconds < 0:
                output = False
        return output
    
if __name__ == "__main__":
    import os
    import sys

    app = QtGui.QApplication(sys.argv)
    
    screenShape = QtGui.QDesktopWidget().screenGeometry()
    width = screenShape.width()/3
    height = screenShape.height() - 80   
    
    iList = InstructionList()
    iList.show()
    
    sys.exit(app.exec_())
    