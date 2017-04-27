# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:32:03 2017

@author: diana
"""

from PyQt4 import QtCore, QtGui
import random

class Instruction(object):
    ''' One step by step instruction'''
    def __init__(self, title='', date='', time='', location='', description='', parent=None):
        
        self.title = title
        self.date = date
        self.time = time
        self.location = location
        self.description = description
        
        self.big_font = QtGui.QFont()
        self.big_font.setPointSize(36)  
        
        self.small_font = QtGui.QFont()
        self.small_font.setPointSize(20) 
        
        self.parent = parent
        
        self.create_edit_frame()
        
    def create_display_frame(self):
        '''create a frame to display the instruction in the app'''
        self.frame = QtGui.QFrame(self.parent)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)        
        self.frame.setAutoFillBackground(True) 

        self.grid = QtGui.QGridLayout(self.frame)
        
        #Create the top part of the frame
        self.title_frame = QtGui.QFrame(self.frame)
        self.title_frame_grid = QtGui.QHBoxLayout(self.title_frame)
      
        self.title_frame.setAutoFillBackground(True) 
        self.title_frame.palette().setColor(self.title_frame.backgroundRole(), QtCore.Qt.blue)
        self.title_frame.setPalette(self.title_frame.palette())

        self.title_label = QtGui.QLabel(self.title)
        self.title_label.setFont(self.big_font)
        self.title_frame_grid.addStretch(1)
        self.title_frame_grid.addWidget(self.title_label)
        self.title_frame_grid.addStretch(1)
        
        self.title_frame.setLayout(self.title_frame_grid)

        #Create the line in the middle
        self.line = QtGui.QFrame(self.frame)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        
        #Create the bottom part of the frame
        self.descr_frame = QtGui.QFrame(self.frame)
        self.descr_frame_grid = QtGui.QFormLayout(self.descr_frame)
        
        self.date_label = QtGui.QLabel(self.date, self.descr_frame)
        self.date_label.setFont(self.small_font)
        self.time_label = QtGui.QLabel(self.time, self.descr_frame)
        self.time_label.setFont(self.small_font)
        self.location_label = QtGui.QLabel(self.location, self.descr_frame)
        self.location_label.setFont(self.small_font)
        self.descr_label = QtGui.QLabel(self.description, self.descr_frame)
        self.descr_label.setFont(self.small_font)
        self.descr_label.setWordWrap(True)

        self.descr_frame_grid.addRow('Time: ', self.time_label)
        self.descr_frame_grid.addRow('Location: ', self.location_label)
        self.descr_frame_grid.addRow(self.descr_label)
        
        self.descr_frame.setLayout(self.descr_frame_grid)
        
        self.grid.addWidget(self.title_frame, 0, 0)
        self.grid.addWidget(self.line, 1, 0)
        self.grid.addWidget(self.descr_frame, 2, 0)
        self.frame.setLayout(self.grid)
        
    def create_edit_frame(self):
        '''create a frame with entry boxes so the user can edit things'''
        self.edit_frame = QtGui.QFrame(self.parent)
        self.edit_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.edit_frame.setFrameShadow(QtGui.QFrame.Raised)        
        self.edit_frame.setAutoFillBackground(True) 
        
        self.edit_grid = QtGui.QFormLayout(self.edit_frame)
        
        self.title_entry = QtGui.QLineEdit()
        self.time_entry = QtGui.QLineEdit()
        self.loc_entry = QtGui.QLineEdit()
        self.descr_entry = QtGui.QTextEdit()
        
        self.title_entry.setText(self.title)
        self.time_entry.setText(self.time)
        self.loc_entry.setText(self.location)
        self.descr_entry.setText(self.description)
        
        self.edit_grid.addRow('Title', self.title_entry)
        self.edit_grid.addRow('Time', self.time_entry)
        self.edit_grid.addRow('Location', self.loc_entry)
        self.edit_grid.addRow('Description', self.descr_entry)
        
        self.edit_frame.setLayout(self.edit_grid)

    def get_display_frame(self):
        return self.frame
        
    def get_edit_frame(self):
        return self.edit_frame
        
    def resize_frame(self, width, height):
        self.width = width
        self.height = height
        self.frame.resize(self.width, self.height)
     
    def get_title(self):
        return self.title
        
    def save(self):
        #save all the entries to the variables
        self.title = self.title_entry.text()
        self.time = self.time_entry.text()
        self.location = self.loc_entry.text()
        self.description = self.descr_entry.toPlainText()
        
        self.create_display_frame()
     
#    def set_title(self, new_title):
#        self.title = new_title
#        self.title_label.setText(self.title)
#        
#    def set_datetime(self, new_datetime):
#        self.datetime = new_datetime
#        self.datetime_label.setText(self.datetime)
#        
#    def set_location(self, new_location):
#        self.location = new_location
#        self.location_label.setText(self.location)
#        
#    def set_description(self, new_description):
#        self.description = new_description
#        self.descr_label.setText(self.description)
        
#    def get_title(self):
#        return self.title
#    
#    def get_datetime(self):
#        return self.datetime
#        
#    def get_location(self):
#        return self.location
#        
#    def get_description(self):
#        return self.description

class InstructionList(object):
    '''A list of the step-by-step instruction objects'''
    def __init__(self, instructions=[], parent=None):
        
        self.instructions = instructions
        self.current_instruction = 0 #keep track of the current instruction
        
        self.parent = parent
        self.create_edit_frame()
        
    def create_edit_frame(self):
        self.frame = QtGui.QFrame()
        self.grid = QtGui.QGridLayout(self.frame)
        
        self.scroll_area = QtGui.QScrollArea(self.frame)
        self.scroll_area.setWidgetResizable(True)
        
        self.scroll_frame = QtGui.QFrame(self.scroll_area)
        self.scroll_grid = QtGui.QFormLayout(self.scroll_frame)
        
        self.question_entry = QtGui.QLineEdit()
        self.scroll_grid.addRow('Question for patient', self.question_entry)
        
        for i in range(len(self.instructions)): 
            # Add the instruction frame to the self.frame
            self.scroll_grid.addRow(self.instructions[i].get_edit_frame())
            print 'added instruction: ' + str(i)
            
        self.scroll_frame.setLayout(self.scroll_grid)
        self.scroll_area.setWidget(self.scroll_frame)
        self.grid.addWidget(self.scroll_area, 0, 0)
        
        self.add_button = QtGui.QPushButton('Add Instruction') 
        self.add_button.clicked.connect(self.add_instruction)
        self.grid.addWidget(self.add_button, 1, 0)
            
        self.frame.setLayout(self.grid)
        
    def create_display_frame(self):
        self.display_frame = QtGui.QFrame()
        self.display_grid = QtGui.QFormLayout()
        
        for instruction in self.instructions:
            self.display_grid.addRow(instruction.get_display_frame())
        
        self.display_frame.setLayout(self.display_grid)

    def save(self):
        self.question = self.question_entry.text()
        for instruction in self.instructions:
            instruction.save()
        self.create_display_frame()
    
    def get_display_frame(self):
        return self.display_frame
   
    def add_instruction(self):
        self.instructions.append(Instruction())
        self.scroll_grid.addRow(self.instructions[-1].get_edit_frame())

    def get_frame(self):
        return self.frame
        
    def resize_frame(self, width, height):
        self.width = width
        self.height = height
        #for instr in self.instructions:
            #instr.resize_frame(self.width, self.height/4)
        self.frame.resize(self.width, self.height)
    
    def get_question(self):
        return self.question
    
    def get_instructions(self):
        return self.instructions
    
    def delete_instruction(self, new_instruction, i=None):
        pass

    def delay(self, time_delay):
        '''delay the all instructions by the time delay starting with the self.current_instruction'''
        # for i in range(current_instruction, end):
        #   self.instructions[i].set_datetime(self.instructions[i].get_datetime() + time_delay)
        pass

    def accept(self):
        '''the current instruction has been completed, move on to the next one'''
        # self.current_instruction += 1 unless it's the last one
        pass
    
    
        
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
        

class ActivitiesList(object):
    '''manages all the activities'''
    def __init__(self, activities=[]):
        self.activities = activities #list of activity objects
        
        if len(self.activities) < 1:
            #create some defaults info
            self.activities.append(Activity(title='Cool Activity', description='descritiotn'))
            self.activities.append(Activity(title='Another Cool Activity', description='descritiotn'))
            self.activities.append(Activity(title='The other Cool Activity', description='descritiotn'))
            self.activities.append(Activity(title='This Activity', description='descritiotn'))
            self.activities.append(Activity(title='That Activity', description='descritiotn'))
            self.activities.append(Activity(title='The Activity', description='descritiotn'))
            
        print self.activities[0].get_instruction_list()
        print self.activities[1].get_instruction_list()
        print self.activities[2].get_instruction_list()
        print self.activities[3].get_instruction_list()
        print self.activities[4].get_instruction_list()
        print self.activities[5].get_instruction_list()
        

    def accepted(self, activity):
        '''tell the neural network that you accepted the activity'''
        pass
            
    def get_activities(self):
        return self.activities
        
    def suggest_activity(self):
        i = random.randint(0, len(self.activities)-1)
        return self.activities[i]
                
class Memory(object):
    
    def __init__(self, title='', datetime='', loc='', descr='', tags=[], pic_filename='', parent=None):
        
        self.title = title
        self.datetime = datetime
        self.location = loc
        self.tags = tags
        self.pic_filename = pic_filename
        self.descr = descr
        
        self.parent = parent
        self.create_frame()
        
    def create_frame(self):
        self.frame = QtGui.QFrame(self.parent)
        self.frame.setFrameShape(QtGui.QFrame.Box) 
        
        big_font = QtGui.QFont()
        big_font.setPointSize(24)  
        
        small_font = QtGui.QFont()
        small_font.setPointSize(16) 
        
        self.grid = QtGui.QGridLayout()        

        #Add the picture
        self.pic = QtGui.QLabel(self.frame)
        self.pixmap = QtGui.QPixmap(self.pic_filename)
        self.pic.setPixmap(self.pixmap)
        
        #Add the labels
        self.title_label = QtGui.QLabel(self.title, self.frame)
        self.title_label.setFont(big_font)
        
        self.datetime_label = QtGui.QLabel(self.datetime, self.frame)
        self.datetime_label.setFont(big_font)
        
        self.location_label = QtGui.QLabel(self.location, self.frame)
        self.location_label.setFont(big_font)
        
        line = ''
        for tag in self.tags:
            line += tag + ', '
        line = line[0:-2]
        self.tags_label = QtGui.QLabel(line, self.frame) 
        self.tags_label.setFont(big_font)
        
        #Add the description
        self.descr_label = QtGui.QLabel(self.descr, self.frame)
        self.descr_label.setWordWrap(True)
        self.descr_label.setFont(small_font)
        
        #add the widgets to the layout manager
        self.grid.addWidget(self.pic, 0, 0) 
        self.grid.addWidget(self.tags_label, 1, 0)
        self.grid.addWidget(self.title_label, 2, 0)
        self.grid.addWidget(self.location_label, 3, 0)
        self.grid.addWidget(self.datetime_label, 4, 0)
        self.grid.addWidget(self.descr_label, 5, 0)
        
        self.frame.setLayout(self.grid) 
    
    def get_frame(self):
        return self.frame
    
    def resize_frame(self, width, height):
        self.width = width
        self.height = height
        self.pixmap = self.pixmap.scaled(self.width, self.height/2, QtCore.Qt.KeepAspectRatio)
        self.pic.setPixmap(self.pixmap)
        self.frame.resize(self.width, self.height)
        
    def get_tags(self):
        return self.tags
        
    def get_location(self):
        return self.location
        
    def get_date(self):
        return self.datetime
        
        
if __name__ == "__main__":

    import sys, os    

    app = QtGui.QApplication(sys.argv)
    
    screenShape = QtGui.QDesktopWidget().screenGeometry()
    width = screenShape.width()/3
    height = screenShape.height() - 50 
    
    instructions = 5*[None]
    
    for i in range(len(instructions)):
        instructions[i] = Instruction('Instruction ' + str(i), '12:24', 'My House', 'fd jfkkdfjv mvm vklxklds v nvnvjkdnvjf n fnds vnks nvjk snvjk nnjjsnvjd')
        #instructions[i].resize_frame(width, height/6)
        
    instruction_list = InstructionList(instructions)
    
    act = Activity(title='ancjlndlksv', instruction_list=instruction_list)
    act.get_frame().show()
    
    act.save_instructions()
    
    #create a new activity
    act2 = Activity(title='fdfdsfdsfd')
    act2.get_frame().show()

    
#    act = Activity('Activity 1', 'fnnnckk ckkkdc djjd kkd', instruction_list)
#    act.resize_frame(width, height)
#    act.get_frame().show()
#    
#    a = 'Name of Event'
#    b = 'Saturday, April 1'
#    c = 'Description bvdjnsv vkmdsvd dvmlsdmvkd mvdk  vdk siiisv llsf nndsln v'
#    d = 'Person1, Person2, Person3'
#    e = 'dog.png'
#    loc = 'locations'
#    mem =  Memory(title=a, loc=loc, datetime=b, descr=c, tags=d, pic_filename=e)
#    mem.resize_frame(width, height/2)
#    mem.get_frame().show()    
    
    sys.exit(app.exec_())     

        