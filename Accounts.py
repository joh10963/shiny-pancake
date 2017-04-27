# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:44:32 2017

@author: diana
"""

import appobjects
import random
import sys, os
from PyQt4 import QtCore, QtGui
import gui2
import mywidgets

class Patient(object):
    ''' Activities, memories, neural network, '''
    def __init__(self, name='', account=None):
        self.name = name
        self.account = account

class Caregiver(object):
    
    def __init__(self, name='', availability=[0, 0, 0, 0, 0, 0, 0], account=None):
        self.name = name
        self.availability = availability #[Su, M, Tu, W, Th, Fr, Sat] 0 if not available, 1 if available
        self.account = account
        self.current_activity = None #store the current activity object
        self.activities = []  
        
        self.create_frame()
    
    def create_frame(self):
        self.frame = QtGui.QFrame()
        
        self.grid = QtGui.QGridLayout(self.frame)

        #create a frame that has a memories and activities tab
        self.create_memories_frame()
        self.create_activities_frame()
        
        self.tab = QtGui.QTabWidget()
        self.tab.addTab(self.memories_tab, 'Memory')
        self.tab.addTab(self.activities_tab, 'Activities')
        self.grid.addWidget(self.tab, 0, 0)
        
        self.frame.setLayout(self.grid)
    
    def create_memories_frame(self):
        self.memories_tab = QtGui.QFrame()
        self.memories_grid = QtGui.QFormLayout()
        
        self.filename_entry = mywidgets.EntryAndButton()
        self.memories_grid.addRow('Picture File', self.filename_entry)
        
        self.tags_entry = mywidgets.EntryAndLabel()
        self.memories_grid.addRow('Tags', self.tags_entry) #DROP DOWN
        
        self.title_entry = QtGui.QLineEdit()
        self.memories_grid.addRow('Event Name', self.title_entry)
        
        self.datetime_entry = mywidgets.EntryAndCalendar()
        self.memories_grid.addRow('Date and Time', self.datetime_entry)
        
        self.location_entry = QtGui.QLineEdit()
        self.memories_grid.addRow('Location', self.location_entry) #DROP DOWN
        
        self.descr_entry = QtGui.QTextEdit()
        self.memories_grid.addRow('Description', self.descr_entry)
        
        self.add_button = QtGui.QPushButton('Add Memory')
        self.add_button.clicked.connect(self.add_memory)
        self.memories_grid.addRow(self.add_button)
        
        self.memories_tab.setLayout(self.memories_grid)
        
    def create_activities_frame(self):
        self.activities_tab = QtGui.QFrame()
        self.activities_grid = QtGui.QGridLayout()
        
        self.question_frame = QtGui.QFrame()
        self.question_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.question_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.question_grid = QtGui.QGridLayout()
        
        self.question_label = QtGui.QLabel()
        self.yes_button = QtGui.QPushButton('Accept')
        self.yes_button.clicked.connect(self.accept_activity)
        self.no_button = QtGui.QPushButton('Decline')
        self.no_button.clicked.connect(self.decline_activity)
        
        self.question_grid.addWidget(self.question_label, 0, 0, 1, 2)
        self.question_grid.addWidget(self.yes_button, 1, 0)
        self.question_grid.addWidget(self.no_button, 1, 1)
        
        self.question_frame.setLayout(self.question_grid)
        
        self.activities_grid.addWidget(self.question_frame, 0, 0)
        
        self.activity_stack = QtGui.QStackedWidget()
        self.activities_grid.addWidget(self.activity_stack, 1, 0)
        
        self.activities_tab.setLayout(self.activities_grid)        
        
    def accept_activity(self):
        #Tell self.account that you accepted 
        self.account.caregiver_accepted_activity(self.current_activity)
        
        #replace with another question
        self.suggest_activity(self.account.get_random_activity())
        
    def decline_activity(self):
        #Tell self.account that you accepted 
        self.account.caregiver_declined_activity(self.current_activity)
        
        #replace with another question
        self.suggest_activity(self.account.get_random_activity())
       
    def add_memory(self):
        #get all the info from the text_boxes
        filename = self.filename_entry.text()
        tags = self.tags_entry.text() 
        loc = self.location_entry.text()
        title = self.title_entry.text()
        datetime = self.datetime_entry.text()
        descr = self.descr_entry.toPlainText()
        
        #create a memory object
        memory = appobjects.Memory(title=title, datetime=datetime, loc=loc, descr=descr, tags=tags, pic_filename=filename)         
        self.account.add_memory(memory)
        
        #clear the fields
        self.filename_entry.clear()
        self.tags_entry.clear()
        self.title_entry.clear()
        self.datetime_entry.clear()
        self.descr_entry.clear()
        self.location_entry.clear()
    
    def get_frame(self):
        return self.frame
    
    def get_name(self):
        return self.name
        
    def set_availability(self, availability):
        self.availability = availability
        
    def get_availability(self):
        return self.availability

    def suggest_activity(self, activity):
        self.current_activity = activity
        self.activity_stack.addWidget(self.current_activity.get_frame()) #it's okay to add the widget again, it won't double count
        print self.activity_stack.count()        
        self.activity_stack.setCurrentWidget(self.current_activity.get_frame())
        self.question_label.setText(self.current_activity.get_title())

class Account(object):
    
    def __init__(self, filename=''):
        self.filename = filename   
        
        screenShape = QtGui.QDesktopWidget().screenGeometry()
        self.width = screenShape.width()/3
        self.height = screenShape.height() - 80  
        
        #Create the activities before creating the caregivers
        self.activities_list = appobjects.ActivitiesList()
        
        #Store memory objects
        self.memories = []  
        #create a bunch of fake data
        people = ['Bill', 'Frank', 'Jess', 'Penelope', 'Faith', 'Kale', 'JJ']
        for i in range(10):
            a = 'Event Title ' + str(i)
            b = 'Saturday, April ' + str(i)
            c = 'Description ' + str(i) + 'Generic description of the event, add more details, more details, descriptions, more descriptions, it was fun'
            d = [people[random.randint(0, 6)], people[random.randint(0, 6)], people[random.randint(0, 6)]]
            e = 'stockphoto' + str(i) + '.png'
            self.memories.append(appobjects.Memory(title=a, datetime=b, descr=c, tags=d, pic_filename=e))
            self.memories[-1].resize_frame(width=self.width, height=3*self.height/5)
        
        #populate with fake data -- eventually either read in data or start from scratch
        self.caregivers = []
        self.caregivers.append(Caregiver(name='Diana', availability=[0, 1, 0, 0, 0, 1, 0], account=self))
        self.caregivers.append(Caregiver(name='Caregiver 1', availability=[0, 0, 1, 0, 0, 0, 0], account=self))
        self.caregivers.append(Caregiver(name='Caregiver 2', availability=[0, 0, 0, 1, 0, 0, 0], account=self))
        self.caregivers.append(Caregiver(name='Caregiver 3', availability=[0, 0, 0, 0, 1, 0, 0], account=self))
        
#        for caregiver in self.caregivers:
#            caregiver.suggest_activity(self.get_random_activity())
        self.caregivers[0].suggest_activity(self.get_random_activity())
        
        self.patient = Patient(name='Patient')
        
        #create a list of colors corresponding to each caregiver
        self.colors = []
        for caregiver in self.caregivers:
            self.colors.append(QtGui.QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255), 150))
        
        #create the screens
        self.caregiver_screen = gui2.CaregiverWindow(width=self.width, height=self.height, account=self)
        self.patient_screen = gui2.PatientWindow(width=self.width, height=self.height, account=self)
        
    def caregiver_accepted_activity(self, activity):
        activity.save_instructions()
        self.activities_list.accepted(activity)
        self.send_to_patient(activity)
    
    def caregiver_declined_activity(self, activity):
        print 'caregiver declined activity'
        
    def send_to_patient(self, activity):
        self.patient_screen.ask_question(activity)
        
    def patient_accepted_activity(self, activity):
        print 'patient accepted activity need to schedule it now'
        
    def patient_declined_activity(self, activity):
        print 'patient declined activity tell the algorithm'
        
    def get_random_activity(self):
        return self.activities_list.suggest_activity()
    
    def get_caregivers(self):
        return self.caregivers
        
    def get_patient(self):
        return self.patient
        
    def get_colors(self):
        '''return a list of colors that correspond to each caregiver'''
        return self.colors
        
    def add_memory(self, memory):
        self.memories.append(memory)
        self.memories[-1].resize_frame(width=self.width, height=3*self.height/5)
        self.caregiver_screen.add_memory(memory)
    
    def get_memories(self):
        return self.memories
        
    def get_tags(self):
        output = []
        for mem in self.memories:
            tags = mem.get_tags()
            for t in tags:
                if t not in output:
                    output.append(t)
        return output
        
    def get_locations(self):
        output = []
        for mem in self.memories:
            loc = mem.get_location()
            if loc not in output:
                output.append(loc)
        print output
        return output
        
    def search(self, tag='', loc='', date=''):
        '''return memories that match  these search criteria'''
        one_match = [] #memories that match one criteria
        two_match = [] #memories that match two criteria
        all_match = [] #memories that match all criteria (that are given - empty strings do not count)
        no_match = [] #memories that do not match any criteria
        
        for mem in self.memories:
            count = 0
            if tag != '' and tag in mem.get_tags():
                count += 1
            if loc != '' and loc == mem.get_location():
                count += 1
            if date != '' and date == mem.get_date():
                count += 1
            
            if count == 0:
                no_match.append(mem)
            elif count == 1:
                one_match.append(mem)
            elif count == 2:
                two_match.append(mem)
            else:
                all_match.append(mem)
        
        return all_match + two_match + one_match + no_match
    
    def get_another_activity(self):
        #ask the algorithm for another activity but for now just do random
        activity = appobjects.Activity(title='Another Cool Activity', description='descritiotn')
        self.caregivers[0].suggest_activity(activity)

    def run(self):
        #show the screens
        self.caregiver_screen.show()
        self.patient_screen.show()
        
if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    
    account = Account()
    account.run()
    
    sys.exit(app.exec_())
        

#class Account(object):
#    
#    def __init__(self, width, height):
#        
#        self.width = width
#        self.height = height        
#        
#        #create a bunch of fake data
#        self.memories = 10*[None]
#        people = ['Bill', 'Frank', 'Jess', 'Penelope', 'Faith', 'Kale', 'JJ']
#        for i in range(10):
#            a = 'Event Title ' + str(i)
#            b = 'Saturday, April ' + str(i)
#            c = 'Description ' + str(i) + 'Generic description of the event, add more details, more details, descriptions, more descriptions, it was fun'
#            d = people[random.randint(0, 6)] + ', ' + people[random.randint(0, 6)] + ', ' + people[random.randint(0, 6)]
#            e = 'stockphoto' + str(i) + '.png'
#            self.memories[i] = appobjects.Memory(title=a, datetime=b, descr=c, tagged_people=d, pic_filename=e)
#            self.memories[i].resize_frame(width=self.width, height=3*self.height/4)
#        
#        acts = {'Bowling':{'descr':'Bowling with the family for Bills 7th birthday.', 
#                           'instructions':{'Step 1':{'descr':'Pack your bowling shoes and bowling ball', 'datetime':'April 2, 4:30 PM', 'location':'House'},
#                                           'Step 2':{'descr':'Get picked up by Susan', 'datetime':'April 2, 4:45 PM', 'location':'House'},
#                                           'Step 3':{'descr':'Bowl with family and eat dinner', 'datetime':'April 2, 5:00 PM', 'location':'Bowling Alley'},
#                                           'Step 4':{'descr':'Store your bowling ball and shoes back in the basement', 'datetime':'April 2, 7:00 PM', 'location':'House'}}},
#               'Beach Day':{'descr':'Go to the beach with Susan and other descriptions make this a really long description more details more details add more details.', 
#                           'instructions':{'Step 1':{'descr':'Pack your beach bag: sunscreen, towel, grapes, and water bottle', 'datetime':'April 5, 12:00 PM', 'location':'House'},
#                                           'Step 2':{'descr':'Drive to the beach. Follow GPS instructions.', 'datetime':'April 5, 12:30 PM', 'location':'Beach'},
#                                           'Step 3':{'descr':'Walk to the west beach, to the left of the pavillion to meet Susan', 'datetime':'April 2, 12:45 PM', 'location':'Beach'},
#                                           'Step 4':{'descr':'Put your towel in the wash', 'datetime':'April 5, 3:00 PM', 'location':'House'}}},
#                'Making soup for Sarahs tonsils':{'descr':'Make Chicken Wild Rice soup for Sarah and other descriptions make this a really long description more details more details add more details.', 
#                           'instructions':{'Step 1':{'descr':'Drive to the grocery store. Follow GPS instructions.', 'datetime':'April 7, 12:00 PM', 'location':'Grocery Store'},
#                                           'Step 2':{'descr':'At the store, pick up carrots, celery, chicken, milk, and butter', 'datetime':'April 5, 12:30 PM', 'location':'Grocery Store'},
#                                           'Step 3':{'descr':'Drive home. Follow GPS instructions.', 'datetime':'April 2, 12:45 PM', 'location':'Home'},
#                                           'Step 4':{'descr':'In a pot, boil some chicken broth.', 'datetime':'April 5, 1:00 PM', 'location':'House'},
#                                            'Step 5':{'descr':'Add the carrots, celery, and chicken', 'datetime':'April 5, 1:15 PM', 'location':'House'},
#                                            'Step 6':{'descr':'Add the milk and butter.', 'datetime':'April 5, 1:30 PM', 'location':'House'},
#                                            'Step 7':{'descr':'Package up a serving of soup and give to Sarah.', 'datetime':'April 5, 2:00 PM', 'location':'House'}}}}
#        
#        self.activities = []
#        for title, info in acts.iteritems():
#            instructions = []
#            for i, i_info in info['instructions'].iteritems():
#                instructions.append(appobjects.Instruction(title=i, datetime=i_info['datetime'], location=i_info['location'], description=i_info['descr']))
#                instructions[-1].resize_frame(self.width, self.height/6)
#            instruction_list = appobjects.InstructionList(instructions)
#            instruction_list.resize_frame(self.width, 3*self.height/4)
#            self.activities.append(appobjects.Activity(title=title, description=info['descr'], instruction_list=instruction_list))
#            self.activities[-1].resize_frame(self.width, self.height) 
#    
#    def get_activities(self):
#        return self.activities
#        
#    def get_memories(self):
#        return self.memories
#    
#    def add_caregiver(self, caregiver):
#        pass
#    
#    def delete_caregiver(self, caregiver):
#        pass
#    
#    def edit_patient(self, **kwargs):
#        pass
#    
#    def edit_caregiver(self, caregiver, **kwargs):
#        pass
#    
#    def resume(self, filename):
#        '''resume a session after reading from a file'''
#        pass
#    
#    def pause(self, filename):
#        '''write all the info to filename'''
#        pass
# 
