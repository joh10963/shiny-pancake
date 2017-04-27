# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 18:36:53 2017

@author: diana
"""
from PyQt4 import QtCore, QtGui

class Memory(QtGui.QWidget):
    
    def __init__(self, title='', date=None, loc='', descr='', tags=[], pic_filename='', parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.title = title
        self.date = date
        if self.date == None:
            self.date = QtCore.QDate()
        self.location = loc
        self.tags = tags
        self.pic_filename = pic_filename
        self.descr = descr

        big_font = QtGui.QFont()
        big_font.setPointSize(24)  
        
        small_font = QtGui.QFont()
        small_font.setPointSize(16) 
        
        self.grid = QtGui.QGridLayout()        

        #Add the picture
        self.pic = QtGui.QLabel()
        self.pixmap = QtGui.QPixmap(self.pic_filename)
        self.pic.setPixmap(self.pixmap)
        
        #Add the labels
        self.title_label = QtGui.QLabel(self.title)
        self.title_label.setFont(big_font)
        
        self.date_label = QtGui.QLabel(self.date.toString())
        self.date_label.setFont(big_font)
        
        self.location_label = QtGui.QLabel(self.location)
        self.location_label.setFont(big_font)
        
        line = ''
        for tag in self.tags:
            line += tag + ', '
        line = line[0:-2]
        self.tags_label = QtGui.QLabel(line) 
        self.tags_label.setFont(big_font)
        
        #Add the description
        self.descr_label = QtGui.QLabel(self.descr)
        self.descr_label.setWordWrap(True)
        self.descr_label.setFont(small_font)
        
        #add the widgets to the layout manager
        self.grid.addWidget(self.pic, 0, 0) 
        self.grid.addWidget(self.tags_label, 1, 0)
        self.grid.addWidget(self.title_label, 2, 0)
        self.grid.addWidget(self.location_label, 3, 0)
        self.grid.addWidget(self.date_label, 4, 0)
        self.grid.addWidget(self.descr_label, 5, 0)
        
        self.setLayout(self.grid) 
    
    def resize_frame(self, width, height):
        self.width = width
        self.height = height
        self.pixmap = self.pixmap.scaled(self.width, self.height/2, QtCore.Qt.KeepAspectRatio)
        self.pic.setPixmap(self.pixmap)
        self.resize(self.width, self.height)
        
    def get_tags(self):
        return self.tags
        
    def get_location(self):
        return self.location
        
    def get_date(self):
        return self.date.toString()
        
if __name__ == "__main__":
    import os
    import sys

    app = QtGui.QApplication(sys.argv)
    
    screenShape = QtGui.QDesktopWidget().screenGeometry()
    width = screenShape.width()/3
    height = screenShape.height() - 80   
    
    mem = Memory(title='Title', date=None, loc='Location', descr='mcksl dmkslv ds', tags=['one', 'two'], pic_filename='stockphoto4.png')
    mem.show()
    
    sys.exit(app.exec_())