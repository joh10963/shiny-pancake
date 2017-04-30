# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:16:39 2017

@author: diana
"""
from PyQt4 import QtCore, QtGui
import mywidgets
from Memory import Memory

class Caregiver(QtGui.QWidget):
    
    browseClicked = QtCore.pyqtSignal()    
    availabilityChanged = QtCore.pyqtSignal()
    
    def __init__(self, name='', availability=[0, 0, 0, 0, 0, 0, 0], account=None, parent=None, width=400, height=475):
        QtGui.QWidget.__init__(self, parent=None)
        self.setContentsMargins(0, 0, 0, 0)
        
        self.name = name
        self.availability = availability #[Su, M, Tu, W, Th, Fr, Sat] 0 if not available, 1 if available
        self.account = account
        self.current_activity = None #store the current activity object
        
        self.width = width
        self.height = height
        self.setMaximumSize(self.width, self.height)
        
        self.grid = QtGui.QGridLayout()

        #create a frame that has a memories and activities tab
        self.create_memories_tab()
        self.create_activities_tab()
        
        self.tab = QtGui.QTabWidget()
        self.tab.setMaximumSize(self.width, self.height)
        self.tab.setContentsMargins(0, 0, 0, 0)
        self.tab.addTab(self.memories_tab, 'Memory')
        self.tab.addTab(self.activities_tab, 'Activities')
        self.grid.addWidget(self.tab, 1, 0, 1, 7)
        
        #create some radiobuttons
        labs = ['Su', 'M', 'Tu', 'W', 'Th', 'F', 'Sa']
        self.radiobuts = []
        for i in range(len(self.availability)):
            but = QtGui.QCheckBox(labs[i])
            self.radiobuts.append(but)
            but.stateChanged.connect(lambda event, index=i:self.availability_changed(index))
            self.grid.addWidget(but, 0, i)
            if self.availability[i]:
                but.setChecked(True)

        self.setLayout(self.grid)
        
    def availability_changed(self, index):
        #update the availability
        self.availability[index] = int(self.radiobuts[index].isChecked())
        self.availabilityChanged.emit()
        print 'done'

    def create_memories_tab(self):
        self.memories_tab = QtGui.QFrame()
        self.memories_tab.setMaximumSize(self.width, self.height)
        self.memories_tab.setContentsMargins(0, 0, 0, 0)
        self.memories_grid = QtGui.QFormLayout()
        
        self.filename_entry = mywidgets.EntryAndButton()
        self.memories_grid.addRow('Picture File', self.filename_entry)
        
        self.tags_entry = mywidgets.EntryAndLabel()
        self.memories_grid.addRow('Tags', self.tags_entry) #DROP DOWN
        
        self.title_entry = QtGui.QLineEdit()
        self.memories_grid.addRow('Event Name', self.title_entry)
        
        self.date_entry = mywidgets.ChooseDate()
        self.memories_grid.addRow('Date and Time', self.date_entry)
        
        self.location_entry = QtGui.QLineEdit()
        self.memories_grid.addRow('Location', self.location_entry) #DROP DOWN
        
        self.descr_entry = QtGui.QTextEdit()
        self.descr_entry.setMaximumHeight(75)
        self.memories_grid.addRow('Description', self.descr_entry)
        
        self.add_button = QtGui.QPushButton('Add Memory')
        self.add_button.clicked.connect(self.add_memory)
        
        self.browse_button = QtGui.QPushButton('View All Memories')
        self.browse_button.clicked.connect(self.send_signal)
        
        self.g = QtGui.QGridLayout()
        self.g.addWidget(self.add_button, 0, 0)
        self.g.addWidget(self.browse_button, 0, 1)
        self.memories_grid.addRow(self.g)
        
        self.memories_tab.setLayout(self.memories_grid)
        
    def send_signal(self):
        '''emit the signal that the browse button was clicked'''
        self.browseClicked.emit()
        
    def create_activities_tab(self):
        self.activities_tab = QtGui.QFrame()
        self.activities_tab.setMaximumSize(self.width, self.height)
        self.activities_tab.setContentsMargins(0, 0, 0, 0)
        self.activities_grid = QtGui.QStackedLayout()
        
        self.activities_tab.setLayout(self.activities_grid)
   
    def add_memory(self):
        #get all the info from the text_boxes
        filename = self.filename_entry.text()
        tags = self.tags_entry.get_tags() 
        loc = self.location_entry.text()
        title = self.title_entry.text()
        date = self.date_entry.get_date()
        descr = self.descr_entry.toPlainText()

        self.account.add_memory(title=title, date=date, loc=loc, descr=descr, tags=tags, pic_filename=filename)     

        #clear the fields
        self.filename_entry.clear()
        self.tags_entry.clear()
        self.title_entry.clear()
        self.date_entry.clear()
        self.descr_entry.clear()
        self.location_entry.clear()

    def get_name(self):
        return self.name
        
    def set_availability(self, availability):
        self.availability = availability
        
    def get_availability(self):
        return self.availability

    def suggest_activity(self, activity):
        self.current_activity = activity
        self.current_activity.set_times(20)
        cur = self.activities_grid.addWidget(self.current_activity) #it's okay to add the widget again, it won't double count
        print self.activities_grid.count()        
        self.activities_grid.setCurrentIndex(cur)
        
if __name__ == "__main__":
    import os
    import sys
    from ActivitiesList import ActivitiesList
    
    app = QtGui.QApplication(sys.argv)
    
    screenShape = QtGui.QDesktopWidget().screenGeometry()
    width = screenShape.width()/3
    height = screenShape.height() - 80  
    
    actList = ActivitiesList()
    act = actList.get_activity()
    act.set_times(20)
    act.show()

    diana = Caregiver(name='Diana', availability=[0, 1, 0, 0, 1, 0, 0])
    diana.suggest_activity(act)
    diana.show()
    
    sys.exit(app.exec_())