# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:44:32 2017

@author: diana
"""

import appobjects
import random
import sys, os
from PyQt4 import QtCore, QtGui

class Patient(object):
    ''' Activities, memories, neural network, '''
    def __init__(self, name=''):
        self.name = name

class Caregiver(object):
    
    def __init__(self, name='', availability=[0, 0, 0, 0, 0, 0, 0]):
        self.name = name
        self.availability = availability #[Su, M, Tu, W, Th, Fr, Sat] 0 if not available, 1 if available
        
    def get_name(self):
        return self.name
        
    def set_availability(self, availability):
        self.availability = availability
        
    def get_availability(self):
        return self.availability


class Account(object):
    
    def __init__(self, filename=''):
        self.filename = filename      
        
        #populate with fake data -- eventually either read in data or start from scratch
        self.caregivers = []
        self.caregivers.append(Caregiver(name='Diana', availability=[0, 1, 0, 0, 0, 1, 0]))
        self.caregivers.append(Caregiver(name='Caregiver 1', availability=[0, 0, 1, 0, 0, 0, 0]))
        self.caregivers.append(Caregiver(name='Caregiver 2', availability=[0, 0, 0, 1, 0, 0, 0]))
        self.caregivers.append(Caregiver(name='Caregiver 3', availability=[0, 0, 0, 0, 1, 0, 0]))
        
        self.patient = Patient(name='Patient')
        
        #create a list of colors corresponding to each caregiver
        self.colors = []
        for caregiver in self.caregivers:
            self.colors.append(QtGui.QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255), 150))
        
    def get_caregivers(self):
        return self.caregivers
        
    def get_patient(self):
        return self.patient
        
    def get_colors(self):
        '''return a list of colors that correspond to each caregiver'''
        return self.colors
        
        

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
   
if __name__ == "__main__":

    pass