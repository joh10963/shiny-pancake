# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 19:03:41 2017

@author: diana
"""
from PyQt4 import QtCore, QtGui
from ActivitiesList import ActivitiesList
from Memory import Memory
from Caregiver import Caregiver
import mywidgets
import random
from collections import deque

class Account(object):
    
    def __init__(self, filename=''):
        self.filename = filename   
        
        screenShape = QtGui.QDesktopWidget().screenGeometry()
        self.width = screenShape.width()/3
        self.height = screenShape.height() - 100  
        
        #Create the activities before creating the caregivers
        self.activities_list = ActivitiesList(account=self)
        
        #Store memory objects
        self.memories = []  
        #create a bunch of fake data
        people = ['Bill', 'Frank', 'Jess', 'Penelope', 'Faith', 'Kale', 'JJ']
        for i in range(10):
            a = 'Event Title ' + str(i)
            b = QtCore.QDate.currentDate()
            c = 'Description ' + str(i) + 'Generic description of the event, add more details, more details, descriptions, more descriptions, it was fun'
            d = [people[random.randint(0, 6)], people[random.randint(0, 6)], people[random.randint(0, 6)]]
            e = 'stockphoto' + str(i) + '.png'
            self.memories.append(Memory(title=a, date=b, descr=c, tags=d, pic_filename=e))
            self.memories[-1].resize_frame(width=self.width, height=3*self.height/6)
        self.memory_browse = mywidgets.MemoryBrowse(elements=self.memories, tags=self.get_tags(), locs=self.get_locations(), account=self)
        
        #populate with fake data -- eventually either read in data or start from scratch
        self.caregivers = []
        self.caregivers.append(Caregiver(name='Diana', availability=[0, 1, 0, 0, 0, 1, 0], account=self))
        self.caregivers.append(Caregiver(name='Caregiver 1', availability=[0, 0, 1, 0, 0, 0, 0], account=self))
        self.caregivers.append(Caregiver(name='Caregiver 2', availability=[0, 0, 0, 1, 0, 0, 0], account=self))
        self.caregivers.append(Caregiver(name='Caregiver 3', availability=[0, 0, 0, 0, 1, 0, 0], account=self))

        #create a list of colors corresponding to each caregiver
        self.colors = []
        for caregiver in self.caregivers:
            self.colors.append(QtGui.QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255), 150))
        
        #create the screens
        self.create_caregiver_screen()
        
        #stack for regular caregiver screen, browse memories
        self.cw = QtGui.QStackedLayout() 
        self.cw.addWidget(self.cs)
        self.cw.addWidget(self.memory_browse)
        
        self.caregiver_screen = mywidgets.BaseFrame(width=self.width, height=self.height)    
        self.caregiver_screen.grid.addLayout(self.cw, 0, 0)
        
        #patient screen flags - so we know what is displayed (only display 1 thing at a time)
        self.started = False #flag for patient yes/no question  
        self.is_during_activity = False #set to true when started and false when finished
        
        self.activity_queue = deque() #this is the activities that the patient sees
        self.current_activity = None
        self.patient_screen = mywidgets.BaseFrame(width=self.width, height=self.height)
        self.question_frame = QtGui.QFrame()
        self.question_layout = QtGui.QGridLayout()
        self.question_frame.setLayout(self.question_layout)
        self.question_label = QtGui.QLabel()
        self.accept_button = QtGui.QPushButton('Yes')
        self.accept_button.clicked.connect(self.patient_accepted_activity)
        self.decline_button = QtGui.QPushButton('No')
        self.decline_button.clicked.connect(self.patient_declined_activity)
        self.question_layout.addWidget(self.question_label, 0, 0, 1, 2)
        self.question_layout.addWidget(self.accept_button, 1, 0)
        self.question_layout.addWidget(self.decline_button, 1, 1)
        self.patient_screen.grid.addWidget(self.question_frame, 0, 0)
        self.question_frame.hide()
        
        #suggest an activity
        self.caregivers[self.current_caregiver()].suggest_activity(self.activities_list.get_activity())
        
        #create a timer to check on things
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.do_checks)
        #self.timer.start()
        
    def do_checks(self):
        print 'do checks'
        #Check to make sure that 

    def create_caregiver_screen(self):
        
        self.cs = QtGui.QWidget()
        self.cs.setContentsMargins(0, 0, 0, 0)
        self.cs_grid = QtGui.QGridLayout()
        self.cs.setLayout(self.cs_grid)
    
        #Create a dropdown menu to change the screen of the current caregiver
        self.current_dropdown = QtGui.QComboBox()
        i = 0
        for caregiver in self.caregivers:
            self.current_dropdown.insertItem(i, caregiver.get_name())
            i += 1
        self.current_dropdown.currentIndexChanged.connect(self.change_caregiver)   
        self.current_dropdown.setCurrentIndex(0)
        self.cs_grid.addWidget(self.current_dropdown, 0, 0)        
        
        self.calendar = mywidgets.AvailabilityCalendar(caregivers=self.caregivers, colors=self.colors)
        self.cs_grid.addLayout(self.calendar, 1, 0)
        
        self.browse_button = QtGui.QPushButton('Browse Memories')
        self.browse_button.clicked.connect(self.open_browse_memories)
        self.cs_grid.addWidget(self.browse_button, 2, 0)

        self.cf = QtGui.QStackedWidget()
        for caregiver in self.caregivers:
            self.cf.addWidget(caregiver)
        self.cs_grid.addWidget(self.cf, 3, 0)
    
    def suggest_activity(self, activity):
        #This shouldn't just be the current caregiver but based on availability
        self.caregivers[self.current_caregiver()].suggest_activity(activity)
    
    def current_caregiver(self):
        return self.current_dropdown.currentIndex()
        
    def open_browse_memories(self):
        self.cw.setCurrentWidget(self.memory_browse)
        
    def goto_home_screen(self):
        self.cw.setCurrentWidget(self.cs)
        
    def change_caregiver(self):
        current_caregiver = self.current_dropdown.currentIndex()
        self.cf.setCurrentWidget(self.caregivers[current_caregiver])
        
    def send_to_patient(self, activity):
        #push the activity onto the queue
        self.activity_queue.append(activity)
        if not self.started: #This is the first activity sent to them
            #pop the first on off
            self.question_frame.show()
            act = self.activity_queue.popleft()
            self.question_label.setText(act.get_question())
            self.current_activity = act
            self.started = True
        
    def patient_accepted_activity(self):
        if self.current_activity != None:
            print 'start schedule'
            instructions, times = self.current_activity.get_scheduled_reminders()
            print instructions
            print times
            print 'end schedule'
        if len(self.activity_queue) > 0:
            act = self.activity_queue.popleft()
            self.question_label.setText(act.get_question())
            self.current_activity = act
        else:
            self.question_frame.hide()
            self.started = False #we ran out of activities to send to the patient
            self.current_activity = None
            
    def patient_declined_activity(self):
        print 'patient declined activity tell the algorithm'
        if len(self.activity_queue) > 0:
            act = self.activity_queue.popleft()
            self.question_label.setText(act.get_question())
            self.current_activity = act
        else:
            self.question_frame.hide()
            self.started = False #we ran out of activities to send to the patient
            self.current_activity = None
    
    def get_caregivers(self):
        return self.caregivers
        
    def get_patient(self):
        return self.patient
        
    def get_colors(self):
        '''return a list of colors that correspond to each caregiver'''
        return self.colors
        
    def add_memory(self, title='', date=None, loc='', descr='', tags=None, pic_filename=''):
        self.memories.append(Memory(title=title, date=date, loc=loc, descr=descr, tags=tags, pic_filename=pic_filename))
        self.memories[-1].resize_frame(width=self.width, height=3*self.height/5)
        self.memory_browse.add_element(self.memories[-1], tags=self.get_tags(), locs=self.get_locations())
    
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

    def run(self):
        #show the screens
        self.caregiver_screen.show()
        self.patient_screen.show()
        
if __name__ == "__main__":
    import sys
    
    app = QtGui.QApplication(sys.argv)
    
    account = Account()
    account.run()
    
    sys.exit(app.exec_())