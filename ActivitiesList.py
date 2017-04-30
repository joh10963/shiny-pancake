# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 14:44:45 2017

@author: diana
"""
from PyQt4 import QtCore, QtGui

from Activity import Activity
from Instruction import Instruction
from InstructionList import InstructionList

import random

class ActivitiesList(QtGui.QWidget):
    '''manages all the activities'''
    def __init__(self, activities=None, parent=None, account=None):
        
        QtGui.QWidget.__init__(self, parent)
        self.activities = activities #list of activity objects
        if self.activities == None:
            self.activities = []
        self.account = account
        
        if len(self.activities) < 1:
            #create some defaults info
            instructions1 = [Instruction(title='Instruction1', date=None, time=None, location='Location1', description='Description1'),
                             Instruction(title='Instruction2', date=None, time=None, location='Location2', description='Description2'),
                             Instruction(title='Instruction3', date=None, time=None, location='Location3', description='Description3')]
            instructionlist1 = InstructionList(instructions=instructions1)
            instructions2 = [Instruction(title='Instruction1', date=None, time=None, location='Location1', description='Description1'),
                             Instruction(title='Instruction2', date=None, time=None, location='Location2', description='Description2'),
                             Instruction(title='Instruction3', date=None, time=None, location='Location3', description='Description3')]
            instructionlist2 = InstructionList(instructions=instructions2)
            instructions3 = [Instruction(title='Instruction1', date=None, time=None, location='Location1', description='Description1'),
                             Instruction(title='Instruction2', date=None, time=None, location='Location2', description='Description2'),
                             Instruction(title='Instruction3', date=None, time=None, location='Location3', description='Description3')]
            instructionlist3 = InstructionList(instructions=instructions3)
            instructions4 = [Instruction(title='Instruction1', date=None, time=None, location='Location1', description='Description1'),
                             Instruction(title='Instruction2', date=None, time=None, location='Location2', description='Description2'),
                             Instruction(title='Instruction3', date=None, time=None, location='Location3', description='Description3')]
            instructionlist4 = InstructionList(instructions=instructions4)
            instructions5 = [Instruction(title='Instruction1', date=None, time=None, location='Location1', description='Description1'),
                             Instruction(title='Instruction2', date=None, time=None, location='Location2', description='Description2'),
                             Instruction(title='Instruction3', date=None, time=None, location='Location3', description='Description3')]
            instructionlist5 = InstructionList(instructions=instructions5)
            instructions6 = [Instruction(title='Instruction1', date=None, time=None, location='Location1', description='Description1'),
                             Instruction(title='Instruction2', date=None, time=None, location='Location2', description='Description2'),
                             Instruction(title='Instruction3', date=None, time=None, location='Location3', description='Description3')]
            instructionlist6 = InstructionList(instructions=instructions6)
        
            self.activities.append(Activity(title='Cool Activity', index=0, instruction_list=instructionlist1))
            self.activities.append(Activity(title='Another Cool Activity', index=1, instruction_list=instructionlist2))
            self.activities.append(Activity(title='The other Cool Activity', index=2, instruction_list=instructionlist3))
            self.activities.append(Activity(title='This Activity', index=3, instruction_list=instructionlist4))
            self.activities.append(Activity(title='That Activity', index=4, instruction_list=instructionlist5))
            self.activities.append(Activity(title='The Activity', index=5, instruction_list=instructionlist6))
            
        for activity in self.activities:
            activity.accepted.connect(self.ask_patient)

    def ask_patient(self, boolean, index):
        '''this gets called once the caregivers accept/decline activity'''
        print 'ask patient of activities list'
        if boolean:
            if self.account.check_activity(self.activities[index]): #if the times are correct
                self.account.send_to_patient(self.activities[index])
        else:
            print 'the caregiver no want to do update algorithm'
        self.account.suggest_activity(self.get_activity())
        print 'suggested'
            
    def get_activities(self):
        return self.activities
        
    def get_activity(self):
        i = random.randint(0, len(self.activities)-1)
        return self.activities[i]
        
if __name__ == "__main__":
    import os
    import sys

    app = QtGui.QApplication(sys.argv)
    
    screenShape = QtGui.QDesktopWidget().screenGeometry()
    width = screenShape.width()/3
    height = screenShape.height() - 80   
    
    actList = ActivitiesList()
    act = actList.get_activity()
    act.show()
    
    sys.exit(app.exec_())