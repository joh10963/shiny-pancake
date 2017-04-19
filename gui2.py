# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:18:09 2017

@author: diana
"""
import sys, os
from PyQt4 import QtCore, QtGui
from Accounts import Account, Caregiver
import random

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
    pass

class CaregiverWindow(BaseFrame):
    
    def __init__(self, width=0, height=0, parent=None, account=None):
        BaseFrame.__init__(self, width=width, height=height, parent=parent)
        
        #Save the account object
        self.account = account  
        
        #create a widget that to display different caregiver screens 
        self.caregiver_frames = []
        self.cw = QtGui.QStackedWidget()
        for caregiver in self.account.get_caregivers():
            self.caregiver_frames.append(CaregiverFrame(height=self.height,
                                                        width=self.width,
                                                        parent=parent,
                                                        caregiver=caregiver,
                                                        account=self.account))
            self.cw.addWidget(self.caregiver_frames[-1])
        self.grid.addWidget(self.cw, 1, 0)
        
        #Create a dropdown menu to change the screen of the current caregiver
        self.current_dropdown = QtGui.QComboBox(self)
        i = 0
        for caregiver in account.get_caregivers():
            self.current_dropdown.insertItem(i, caregiver.get_name())
            i += 1
        self.current_dropdown.currentIndexChanged.connect(self.change_caregiver)   
        self.current_dropdown.setCurrentIndex(0)
        
        self.grid.addWidget(self.current_dropdown, 0, 0)
        
    def change_caregiver(self):
        current_caregiver = self.current_dropdown.currentIndex()
        self.cw.setCurrentWidget(self.caregiver_frames[current_caregiver])

class CaregiverFrame(QtGui.QFrame):
    
    def __init__(self, height=0, width=0, parent=None, caregiver=None, account=None):
        QtGui.QFrame.__init__(self, parent)
        self.caregiver = caregiver #Caregiver object
        self.account = account
        
        self.height = height
        self.width = width
        
        self.resize(self.width, self.height)
        
        self.grid = QtGui.QGridLayout(self)
        
        #Calendar
        self.cal = AvailabilityCalendar(account=self.account)
        self.cal.resize(self.width, self.height)
        self.cal.updateCells()
        self.cal.selectionChanged.connect(self.show_schedule)
        self.grid.addWidget(self.cal, 0, 0, 1, len(self.account.get_caregivers()))
        
        #Key to calendar
        self.keys = []
        for i in range(len(self.account.get_colors())):
            l = QtGui.QLabel()
            l.setText(self.account.get_caregivers()[i].get_name())
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Foreground, self.account.get_colors()[i])
            l.setPalette(palette)
            self.keys.append(l)
            self.grid.addWidget(l, 1, i)
            
        #create a frame that has a memories and activities tab
        self.create_memories_frame()
        self.create_activities_frame()
        self.create_browse_tab()
        self.create_schedule_tab()
        
        self.tab = QtGui.QTabWidget()
        self.tab.addTab(self.memories_tab, 'Add Memory')
        self.tab.addTab(self.browse_tab, 'Browse Memories') ##### It doesn't seem like a good idea to have all these here, think of a way besides tabs
        self.tab.addTab(self.activities_tab, 'Suggested Activities')
        self.tab.addTab(self.schedule_tab, 'Scheduled Activities')
        self.grid.addWidget(self.tab, 2, 0, 1, len(self.account.get_caregivers()))
        
        self.setLayout(self.grid)
    
    def create_browse_tab(self):
        self.browse_tab = QtGui.QFrame()
        self.browse_grid = QtGui.QGridLayout()
        
        l = QtGui.QLabel()
        l.setText('Browse Memories')
        self.browse_grid.addWidget(l, 0, 0)        
        
        self.browse_tab.setLayout(self.browse_grid)
        
    def create_schedule_tab(self):
        self.schedule_tab = QtGui.QFrame()
        self.schedule_grid = QtGui.QGridLayout()
        
        l = QtGui.QLabel()
        l.setText('schedule')
        self.schedule_grid.addWidget(l, 0, 0)        
        
        self.schedule_tab.setLayout(self.schedule_grid)
    
    def create_memories_frame(self):
        self.memories_tab = QtGui.QFrame()
        self.memories_grid = QtGui.QFormLayout()
        
        self.filename_entry = QtGui.QLineEdit()
        self.memories_grid.addRow('Picture Filename', self.filename_entry)
        
        self.tags_entry = QtGui.QLineEdit()
        self.memories_grid.addRow('Tagged People', self.tags_entry)
        
        self.title_entry = QtGui.QLineEdit()
        self.memories_grid.addRow('Event Name', self.title_entry)
        
        self.datetime_entry = QtGui.QLineEdit()
        self.memories_grid.addRow('Date and Time', self.datetime_entry)
        
        self.descr_entry = QtGui.QTextEdit()
        self.memories_grid.addRow('Description', self.descr_entry)
        
        self.add_button = QtGui.QPushButton('Add Memory')
        self.memories_grid.addRow(self.add_button)
        
        self.memories_tab.setLayout(self.memories_grid)
        
    def create_activities_frame(self):
        self.activities_tab = QtGui.QFrame()
        self.activities_grid = QtGui.QGridLayout()
        
        l = QtGui.QLabel()
        l.setText('activities')
        self.activities_grid.addWidget(l, 0, 0)
        
        self.activities_tab.setLayout(self.activities_grid)
        
    def show_schedule(self, date):
        #look for scheduled activities for date
        #change the tab widget
        print 'show schedule'
        
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