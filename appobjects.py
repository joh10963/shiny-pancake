# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:32:03 2017

@author: diana
"""

from PyQt4 import QtCore, QtGui

class Instruction(object):
    ''' One step by step instruction'''
    def __init__(self, title='', datetime='', location='', description='', parent=None):
        
        self.title = title
        self.datetime = datetime
        self.location = location
        self.description = description
        
        self.parent = parent
        
        self.create_frame()
        
    def create_frame(self):
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
        
        self.datetime_label = QtGui.QLabel(self.datetime, self.descr_frame)
        self.location_label = QtGui.QLabel(self.location, self.descr_frame)
        self.descr_label = QtGui.QLabel(self.description, self.descr_frame)
        self.descr_label.setWordWrap(True)

        self.descr_frame_grid.addRow('Time: ', self.datetime_label)
        self.descr_frame_grid.addRow('Location: ', self.location_label)
        self.descr_frame_grid.addRow(self.descr_label)
        
        self.descr_frame.setLayout(self.descr_frame_grid)
        
        self.grid.addWidget(self.title_frame, 0, 0)
        self.grid.addWidget(self.line, 1, 0)
        self.grid.addWidget(self.descr_frame, 2, 0)
        self.frame.setLayout(self.grid)

    def get_frame(self):
        return self.frame
        
    def resize_frame(self, width, height):
        self.width = width
        self.height = height
        self.frame.resize(self.width, self.height)
        
    def set_title(self, new_title):
        self.title = new_title
        self.title_label.setText(self.title)
        
    def set_datetime(self, new_datetime):
        self.datetime = new_datetime
        self.datetime_label.setText(self.datetime)
        
    def set_location(self, new_location):
        self.location = new_location
        self.location_label.setText(self.location)
        
    def set_description(self, new_description):
        self.description = new_description
        self.descr_label.setText(self.description)
        
    def get_title(self):
        return self.title
    
    def get_datetime(self):
        return self.datetime
        
    def get_location(self):
        return self.location
        
    def get_description(self):
        return self.description

class InstructionList(object):
    '''A list of the step-by-step instruction objects'''
    def __init__(self, instructions=None, parent=None):
        
        self.instructions = instructions
        self.current_instruction = 0 #keep track of the current instruction
        
        self.parent = parent
        self.create_frame()
        
    def create_frame(self):
        self.frame = QtGui.QFrame(self.parent)
        self.grid = QtGui.QGridLayout(self.frame)
        
        self.scroll_area = QtGui.QScrollArea(self.frame)
        
        self.scroll_frame = QtGui.QFrame(self.scroll_area)
        self.scroll_grid = QtGui.QGridLayout(self.scroll_frame)
        
        for i in range(len(self.instructions)): #THIS WILL NEED TO CHANGE IF NOT A LIST
            # Add the instruction frame to the self.frame
            self.scroll_grid.addWidget(self.instructions[i].get_frame(), i, 0)
            
        self.scroll_frame.setLayout(self.scroll_grid)
        self.scroll_area.setWidget(self.scroll_frame)
        self.grid.addWidget(self.scroll_area, 0, 0)
            
        self.frame.setLayout(self.grid)

    def get_frame(self):
        return self.frame
        
    def resize_frame(self, width, height):
        self.width = width
        self.height = height
        self.frame.resize(self.width, self.height)
    
    def add_instruction(self, new_instruction, i=None):
        '''add the instruction to the back of the list if no index i is given, otherwise add it to ith location'''
        pass
    
    def delete_instruction(self, new_instruction, i=None):
        pass

    def delay(self, time_delay):
        '''delay the all instructions by the time delay starting with the self.current_instruction'''
        # for i in range(current_instruction, end):
        #   self.instructions[i].set_datetime(self.instructions[i].get_datetime() + time_delay)
        pass

    def edit(self, i, new_title=None, new_datetime=None, new_location=None, new_description=None):
        '''edit the ith instruction with the new data if it's given'''
        # if new_title != None:
        #   self.instructions[i].set_title(new_title)
        # repeat with others
        pass

    def accept(self):
        '''the current instruction has been completed, move on to the next one'''
        # self.current_instruction += 1 unless it's the last one
        pass
    
    def get_datetime(self):
        '''returns the datetime of the Instructions which would be the datetime of the first instruction?'''
        if self.instructions == None:
            return ''
        return self.instructions[0].get_datetime()
        
    def get_location(self):
        '''return the location which would be the location of the last instruction?'''
        if self.instructions == None:
            return ''
        return self.instructions[-1].get_location()
    
        
class Activity(object):
    
    def __init__(self, title='', description='', instruction_list=None, parent=None):
        
        self.instruction_list = instruction_list  
        
        self.title = title
        self.description = description
        self.datetime = self.instruction_list.get_datetime()
        self.location = self.instruction_list.get_location()
        
        self.parent = parent
        self.create_frame()
        
    def create_frame(self):
        self.frame = QtGui.QFrame()
        self.grid = QtGui.QGridLayout()
        
        self.title_label = QtGui.QLabel(self.title)
        self.datetime_label = QtGui.QLabel(self.datetime)
        self.description_label = QtGui.QLabel(self.description)
    
        self.grid.addWidget(self.title_label, 0, 0)
        self.grid.addWidget(self.datetime_label, 1, 0)
        self.grid.addWidget(self.description_label, 2, 0)        
        self.grid.addWidget(self.instruction_list.get_frame(), 3, 0)
        
        self.frame.setLayout(self.grid)
        
    def get_frame(self):
        return self.frame
     
    def resize_frame(self, width, height):
        self.width = width
        self.height = height
        self.frame.resize(self.width, self.height)

class ActivitiesList(object):
    '''manages all the activities'''
    pass
        
class Memory(object):
    
    def __init__(self, title='', datetime='', descr='', tagged_people='', pic_filename='', parent=None):
        
        self.title = title
        self.datetime = datetime
        self.tagged_people = tagged_people
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
        
        self.tags_label = QtGui.QLabel(self.tagged_people, self.frame) ############These need to be clickable labels
        self.tags_label.setFont(big_font)
        
        #Add the description
        self.descr_label = QtGui.QLabel(self.descr, self.frame)
        self.descr_label.setWordWrap(True)
        self.descr_label.setFont(small_font)
        
        #add the widgets to the layout manager
        self.grid.addWidget(self.pic, 0, 0) 
        self.grid.addWidget(self.tags_label, 1, 0)
        self.grid.addWidget(self.title_label, 2, 0)
        self.grid.addWidget(self.datetime_label, 3, 0)
        self.grid.addWidget(self.descr_label, 4, 0)
        
        self.frame.setLayout(self.grid) 
    
    def get_frame(self):
        return self.frame
    
    def resize_frame(self, width, height):
        self.width = width
        self.height = height
        self.pixmap = self.pixmap.scaled(self.width, self.height/2, QtCore.Qt.KeepAspectRatio)
        self.pic.setPixmap(self.pixmap)
        self.frame.resize(self.width, self.height)
        
        
if __name__ == "__main__":
    import sys, os    

    app = QtGui.QApplication(sys.argv)
    
    screenShape = QtGui.QDesktopWidget().screenGeometry()
    width = screenShape.width()/3
    height = screenShape.height() - 50 
    
    instructions = 5*[None]
    
    for i in range(len(instructions)):
        instructions[i] = Instruction('Instruction ' + str(i), '12:24', 'My House', 'fd jfkkdfjv mvm vklxklds v nvnvjkdnvjf n fnds vnks nvjk snvjk nnjjsnvjd')
        instructions[i].resize_frame(width, height/6)
        
    instruction_list = InstructionList(instructions)
    instruction_list.resize_frame(width, 3*height/4)
    
    act = Activity('Activity 1', 'fnnnckk ckkkdc djjd kkd', instruction_list)
    act.resize_frame(width, height)
    act.get_frame().show()
    
    a = 'Name of Event'
    b = 'Saturday, April 1'
    c = 'Description bvdjnsv vkmdsvd dvmlsdmvkd mvdk  vdk siiisv llsf nndsln v'
    d = 'Person1, Person2, Person3'
    e = 'dog.png'
    mem =  Memory(title=a, datetime=b, descr=c, tagged_people=d, pic_filename=e)
    mem.resize_frame(width, height/2)
    mem.get_frame().show()    
    
    sys.exit(app.exec_())     

        