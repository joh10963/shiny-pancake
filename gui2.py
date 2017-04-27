# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:18:09 2017

@author: diana
"""
import sys, os
from PyQt4 import QtCore, QtGui
from Accounts import Account, Caregiver
import random
import appobjects
import mywidgets

#Create some font sizes
font_24 = QtGui.QFont()
font_24.setPointSize(24)

font_18 = QtGui.QFont()
font_18.setPointSize(18)

class BaseFrame(QtGui.QFrame):
    '''Creates a Frame widget that displays the current date and time'''
    def __init__(self, width=0, height=0, parent=None):
        QtGui.QFrame.__init__(self, parent)

        self.width = width
        self.height = height
        self.resize(self.width, self.height) 
        
        self.time_label = QtGui.QLabel('Time', self)
        self.time_label.setFont(font_24)
        self.date_label = QtGui.QLabel('Date', self)
        self.date_label.setFont(font_18)
        
        #Place them at the top of the frame     
        self.gridHt = QtGui.QHBoxLayout() 
        self.gridHt.addStretch(1)
        self.gridHt.addWidget(self.time_label)
        self.gridHt.addStretch(1)
        
        self.gridHd = QtGui.QHBoxLayout()
        self.gridHd.addStretch(1)
        self.gridHd.addWidget(self.date_label)
        self.gridHd.addStretch(1)
        
        self.gridV = QtGui.QVBoxLayout()
        self.gridV.addLayout(self.gridHd)
        self.gridV.addLayout(self.gridHt)
        #self.gridV.addStretch(1)
        
        self.frame = QtGui.QFrame()
        self.frame.resize(self.width, self.height-150)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.grid = QtGui.QGridLayout()
        self.frame.setLayout(self.grid)
        
        self.gridV.addWidget(self.frame)
        self.gridV.addStretch(1)
    
        self.setLayout(self.gridV)
        
        #Set a timer to update the date and time periodically
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_display)
        self.update_display()
        self.timer.start()
        
    def update_display(self):
        self.time_label.setText(QtCore.QDateTime.currentDateTime().time().toString())
        self.date_label.setText(QtCore.QDateTime.currentDateTime().date().toString())


class PatientWindow(BaseFrame):
    
    def __init__(self, width=0, height=0, parent=None, account=None):
        BaseFrame.__init__(self, width=width, height=height, parent=parent)
        
        self.account = account
        
        #question widgets
        self.quest_grid = QtGui.QGridLayout()
        self.question_label = QtGui.QLabel()
        self.accept_button = QtGui.QPushButton('Yes')
        self.accept_button.clicked.connect(self.accepted_activity)
        self.decline_button = QtGui.QPushButton('No')
        self.decline_button.clicked.connect(self.declined_activity)
        self.quest_grid.addWidget(self.question_label, 0, 0, 1, 2)
        self.quest_grid.addWidget(self.accept_button, 1, 0)
        self.quest_grid.addWidget(self.decline_button, 1, 1)
        self.grid.addLayout(self.quest_grid, 0, 0)
        
    def ask_question(self, activity):
        self.current_activity = activity
        self.question_label.setText(activity.get_question())
        
    def accepted_activity(self):
        self.question_label.setText('This activity has been accepted')
        self.account.patient_accepted_activity(self.current_activity)
        
    def declined_activity(self):
        self.question_label.setText('This activity has been declined')
        self.account.patient_declined_activity(self.current_activity)

class CaregiverWindow(BaseFrame):
    
    def __init__(self, width=0, height=0, parent=None, account=None):
        BaseFrame.__init__(self, width=width, height=height, parent=parent)
        
        #Save the account object
        self.account = account  
        
        self.cw = QtGui.QStackedWidget()
        
        #Create the main frame
        self.create_main_frame()
        
        #Create a frame that holds the memories
        self.memory_frame = MemoryBrowse(account=self.account, parent=parent, window=self)
        
        #add the frames to the stacked widget
        self.cw.addWidget(self.frame) #main frame = 0
        self.cw.addWidget(self.memory_frame) #memory frame = 1
        
        self.grid.addWidget(self.cw)
        self.cw.setCurrentIndex(0) #main frame
        
    def create_main_frame(self):
        self.frame = QtGui.QFrame()
        self.frame_grid = QtGui.QGridLayout()
        
        #Create a dropdown menu to change the screen of the current caregiver
        self.current_dropdown = QtGui.QComboBox(self)
        i = 0
        for caregiver in self.account.get_caregivers():
            self.current_dropdown.insertItem(i, caregiver.get_name())
            i += 1
        self.current_dropdown.currentIndexChanged.connect(self.change_caregiver)   
        self.current_dropdown.setCurrentIndex(0)
        self.frame_grid.addWidget(self.current_dropdown, 0, 0)
        
        #Calendar
        self.cal = AvailabilityCalendar(account=self.account)
        self.cal.resize(self.width, self.height)
        self.cal.updateCells()
        #self.cal.selectionChanged.connect(self.show_schedule)
        self.frame_grid.addWidget(self.cal, 1, 0, 1, len(self.account.get_caregivers()))
        
        #Legend below calendar
        self.keys = []
        for i in range(len(self.account.get_colors())):
            l = QtGui.QLabel()
            l.setText(self.account.get_caregivers()[i].get_name())
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Foreground, self.account.get_colors()[i])
            l.setPalette(palette)
            self.keys.append(l)
            self.frame_grid.addWidget(l, 2, i)
        
        #create a widget that to display different caregiver screens 
        self.caregiver_frames = []
        self.cf = QtGui.QStackedWidget()
        for caregiver in self.account.get_caregivers():
            self.caregiver_frames.append(caregiver.get_frame())
            self.cf.addWidget(self.caregiver_frames[-1])
        self.frame_grid.addWidget(self.cf, 3, 0, 1, len(self.account.get_caregivers()))

        #Create a browse button to browse the memories
        self.browse_button = QtGui.QPushButton('Browse Memories')
        self.browse_button.clicked.connect(self.browse_memories)
        self.frame_grid.addWidget(self.browse_button, 4, 0, 1, len(self.account.get_caregivers()))
        
        self.frame.setLayout(self.frame_grid)
    
    def browse_memories(self):
        self.cw.setCurrentIndex(1)
        
    def goto_home_screen(self):
        self.cw.setCurrentIndex(0)
        
    def change_caregiver(self):
        current_caregiver = self.current_dropdown.currentIndex()
        self.cf.setCurrentWidget(self.caregiver_frames[current_caregiver])
        
    def add_memory(self, memory):
        self.memory_frame.add_element(memory)
        
class AvailabilityCalendar(QtGui.QCalendarWidget):
    '''calendar that fills in each day with a color corresponding to caregivers availabilities'''
    def __init__(self, parent=None, account=None):
        QtGui.QCalendarWidget.__init__(self, parent)
        
        self.account = account
        self.caregiver_list = self.account.get_caregivers()
        self.color_list = self.account.get_colors()
        
    def paintCell(self, painter, rect, date):
        QtGui.QCalendarWidget.paintCell(self, painter, rect, date)
        
        fill, color = self.get_color(date)
        if fill:
            painter.fillRect(rect, color)
     
    def get_color(self, date):
        #get the day of the week 1=Mon, 7=Sunday
        day = date.dayOfWeek()
        
        fill = False #assume that nobody is available
        color = None
        for caregiver in self.account.get_caregivers():
            if caregiver.get_availability()[day%7] == 1:
                fill = True
                color = self.color_list[self.account.get_caregivers().index(caregiver)]
                
        return fill, color
        
class MemoryBrowse(QtGui.QFrame):
    '''displays one widget from elements at a time. scroll through list with buttons'''
    
    def __init__(self, account=None, parent=None, window=None): 
        QtGui.QFrame.__init__(self, parent)        
        self.account = account
        self.window = window #CaregiverWindow
        
        self.elements = []
        for mem in self.account.get_memories():
            self.elements.append(mem)
        self.elements.reverse()
        self.n = len(self.elements)       
        
        #Create the layout manager
        self.grid = QtGui.QGridLayout()
        
        #The elements will be stored in a QStackedWidget so only one is available to view at a time
        self.cw = QtGui.QStackedWidget()
        for e in self.elements:
            self.cw.addWidget(e.get_frame())
        
        #create a pointer of the currently displayed widget
        self.current = 0
        self.cw.setCurrentIndex(self.current)
            
        #Create the up and down buttons
        self.left = QtGui.QPushButton('Previous')
        self.left.clicked.connect(self.clicked_left)
        
        self.right = QtGui.QPushButton('Next')
        self.right.clicked.connect(self.clicked_right)
        
        #add the widgets to the frame
        self.grid.addWidget(self.cw, 0, 0, 1, 2)
        self.grid.addWidget(self.left, 1, 0)
        self.grid.addWidget(self.right, 1, 1)
        
        #Add the searching tools
        self.search_layout = QtGui.QFormLayout()
        
        self.tags_search = QtGui.QComboBox()
        self.tags_search.addItems(self.account.get_tags())
        self.loc_search = QtGui.QComboBox()
        self.loc_search.addItems(self.account.get_locations())
        self.date_search = mywidgets.EntryAndCalendar()
        self.search_button = QtGui.QPushButton('Search')
        self.search_button.clicked.connect(self.search)
        
        self.search_layout.addRow('Tags', self.tags_search)
        self.search_layout.addRow('Location', self.loc_search)
        self.search_layout.addRow('Date', self.date_search)
        self.search_layout.addRow(self.search_button)
        
        self.grid.addLayout(self.search_layout, 2, 0, 1, 2)
        
        #Return to home button
        self.home_button = QtGui.QPushButton('Main Menu')
        self.home_button.clicked.connect(self.window.goto_home_screen)
        self.grid.addWidget(self.home_button, 3, 0)
            
        #Set the layout manager to the frame
        self.setLayout(self.grid)
    
    def clicked_left(self):
        '''the left button was clicked'''
        if self.current <= 0: #you can't go up anymore
            print 'no go up'
        else:
            self.current -= 1
            self.cw.setCurrentIndex(self.current)
            
    def clicked_right(self):
        '''the right button was clicked'''
        if self.current >= self.n: #you can't go down anymore
            print 'no go down'
        else:
            self.current += 1
            self.cw.setCurrentIndex(self.current)
            
    def add_element(self, element):
        '''add the element to the front of the list, set as current widget'''
        self.elements.insert(0, element)
        self.cw.insertWidget(0, element.get_frame())
        
        self.current = 0
        self.cw.setCurrentIndex(self.current)
        
        #Uodate other things
        self.tags_search.clear()
        self.tags_search.addItems(self.account.get_tags())
        self.loc_search.clear()
        self.loc_search.addItems(self.account.get_locations())
        
    def search(self):
        tag = self.tags_search.currentText()
        loc = self.loc_search.currentText()
        date = self.date_search.text()
        
        self.elements = self.account.search(tag=tag, loc=loc, date=date) #returns the memories in search order
        
        #remove all the widgets in the stack
        for i in range(self.cw.count()):
            widget = self.cw.widget(i)            
            self.cw.removeWidget(widget)
            
        #add in the new order
        for e in self.elements:
            self.cw.addWidget(e.get_frame())

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    
    screenShape = QtGui.QDesktopWidget().screenGeometry()
    width = screenShape.width()/3
    height = screenShape.height() - 80   
    
    account = Account()
    
#    cg = Caregiver('Diana')
#    win = CaregiverFrame(caregiver=cg)
#    win.show()
    
#    patient = PatientWindow(width=width, height=height)
#    patient.show()  
    
    caregiver = CaregiverWindow(width=width, height=height, account=account)
    caregiver.show()
    
    sys.exit(app.exec_())