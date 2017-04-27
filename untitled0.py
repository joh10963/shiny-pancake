# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 14:09:58 2017

@author: diana
"""

class Activity(object):
    
    def __init__(self, title='', description='', instruction_list=None, parent=None):
        
        self.instruction_list = instruction_list 
        if self.instruction_list == None:
            print 'creating new instruction list'
            self.instruction_list = InstructionList()
            #self.instruction_list.add_instruction()
        
        self.title = title
        self.description = description
        
        self.big_font = QtGui.QFont()
        self.big_font.setPointSize(36)  
        
        self.small_font = QtGui.QFont()
        self.small_font.setPointSize(20) 
        
        self.parent = parent
        self.create_frame()
        
    def create_frame(self):
        self.frame = QtGui.QFrame()
        self.grid = QtGui.QGridLayout()
        
        self.title_label = QtGui.QLabel(self.title)
        self.title_label.setFont(self.big_font)
        self.description_label = QtGui.QLabel(self.description)
        self.description_label.setFont(self.small_font)
        self.description_label.setWordWrap(True)
          
        self.grid.addWidget(self.instruction_list.get_frame(), 0, 0)
        
        self.frame.setLayout(self.grid)
        
    def get_frame(self):
        return self.frame
     
    def resize_frame(self, width, height):
        self.width = width
        self.height = height
        #self.instruction_list.resize_frame(self.width, 3*self.height/4)
        self.frame.resize(self.width, self.height)

    def save_instructions(self):
        self.instruction_list.save()
        
    def get_instructions(self):
        return self.instruction_list.get_instructions()
        
    def get_instruction_list(self):
        return self.instruction_list
        
    def get_title(self):
        return self.title
        
    def get_question(self):
        return self.instruction_list.get_question()