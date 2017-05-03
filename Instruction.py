# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 11:49:22 2017

@author: diana
"""

from PyQt4 import QtCore, QtGui
import mywidgets

class Instruction(QtGui.QWidget):
    ''' One step by step instruction'''

    completed = QtCore.pyqtSignal()  
    canceled = QtCore.pyqtSignal()
    
    def __init__(self, title='', date=None, time=None, location='', description='', parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.title = title
        self.date = date
        self.time = time
        self.location = location
        self.description = description
        
        if self.date == None:
            self.date = QtCore.QDate()
        if self.time == None:
            self.time = QtCore.QTime()
        
        self.big_font = QtGui.QFont()
        self.big_font.setPointSize(36)  
        
        self.small_font = QtGui.QFont()
        self.small_font.setPointSize(20) 
        
        self.create_display_frame()
        self.create_edit_frame()
        self.update()
        
    def create_display_frame(self):
        '''create a frame to display the instruction in the app'''
        self.frame = QtGui.QFrame()
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)        

        self.grid = QtGui.QFormLayout(self.frame)
        
        self.title_label = QtGui.QLabel()
        self.title_label.setFont(self.small_font)
        self.time_label = QtGui.QLabel()
        self.date_label = QtGui.QLabel()
        self.loc_label = QtGui.QLabel()
        self.descr_label = QtGui.QLabel()
        self.descr_label.setWordWrap(True)
        
        self.grid.addRow(self.title_label)
        self.grid.addRow(self.date_label, self.time_label)
        self.grid.addRow(self.loc_label)
        
        #create the yes and no buttons
        self.completed_button = QtGui.QPushButton('Completed')
        self.completed_button.clicked.connect(self.completed_instruction)
        self.cancel_button = QtGui.QPushButton('Cancel Activity')
        self.cancel_button.clicked.connect(self.canceled_instruction)
        
        self.g = QtGui.QGridLayout()
        self.g.addWidget(self.completed_button, 0, 0)
        self.g.addWidget(self.cancel_button, 0, 1)
        
        self.grid.addRow(self.g)
        
        self.frame.setLayout(self.grid)
        
    def completed_instruction(self):
        '''send out a signal when the completed button is pressed'''
        self.completed.emit()
        
    def canceled_instruction(self):
        '''send out a signal when the completed button is pressed'''
        self.canceled.emit()
        
    def create_edit_frame(self):
        '''create a frame with entry boxes so the user can edit things'''
        self.edit_frame = QtGui.QFrame()
        self.edit_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.edit_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.edit_frame.setContentsMargins(0, 0, 0, 0)        
        
        self.edit_grid = QtGui.QFormLayout(self.edit_frame)
        
        self.title_entry = QtGui.QLineEdit()
        self.time_entry = mywidgets.ChooseTime(time=self.time)
        self.date_entry = mywidgets.ChooseDate(date=self.date)
        self.loc_entry = QtGui.QLineEdit()
        self.descr_entry = QtGui.QTextEdit()
        self.descr_entry.setMaximumHeight(50)
        
        self.title_entry.textChanged.connect(self.update)
        self.loc_entry.textChanged.connect(self.update)
        self.descr_entry.textChanged.connect(self.update)
        self.time_entry.timeChanged.connect(self.update)
        self.date_entry.dateChanged.connect(self.update)
        
        self.title_entry.setText(self.title)
        self.time_entry.setText(self.time)
        self.date_entry.setText(self.date.toString())
        self.loc_entry.setText(self.location)
        self.descr_entry.setText(self.description)
        
        self.edit_grid.addRow('Title', self.title_entry)
        self.edit_grid.addRow('Date', self.date_entry)
        self.edit_grid.addRow('Time', self.time_entry)
        self.edit_grid.addRow('Location', self.loc_entry)
        #self.edit_grid.addRow('Description', self.descr_entry)
        
        self.edit_frame.setLayout(self.edit_grid)

    def update(self):
        '''update the feilds everytime something is changed'''
        #update the fields
        self.title_label.setText(self.title_entry.text())
        self.time_label.setText(self.time_entry.text())
        self.date_label.setText(self.date_entry.toString())
        self.loc_label.setText(self.loc_entry.text())
        self.descr_label.setText(self.descr_entry.toPlainText())
        
    def set_time(self, time):
        self.time_entry.setText(time)
        
    def set_date(self, date):
        self.date_entry.setDate(date)
        
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
        
    def get_date(self):
        return self.date_entry.get_date()
        
    def get_time(self):
        return self.time_entry.time()
        
    def get_location(self):
        return self.loc_entry.text()
        
    def get_description(self):
        return self.descr_entry.toPlainText()
        
        
if __name__ == "__main__":
    import os
    import sys

    app = QtGui.QApplication(sys.argv)
    
    screenShape = QtGui.QDesktopWidget().screenGeometry()
    width = screenShape.width()/3
    height = screenShape.height() - 80   
    
    instruction = Instruction()
    instruction.get_edit_frame().show()
    instruction.get_display_frame().show()
    
    sys.exit(app.exec_())
     
