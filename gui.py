# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 12:11:53 2017

@author: diana
"""

import sys, os
from PyQt4 import QtCore, QtGui
import appobjects

class BaseFrame(QtGui.QFrame):
    '''Creates a Frame widget that displays the current date and time'''
    def __init__(self, width=0, height=0, parent=None):
        QtGui.QFrame.__init__(self, parent)

        self.width = width
        self.height = height
        self.resize(self.width, self.height) 
        
        #set the font sizes
        self.big_font = QtGui.QFont()
        self.big_font.setPointSize(24)
        
        self.small_font = QtGui.QFont()
        self.small_font.setPointSize(18)
        
        #Create the widgets
        self.time_label = QtGui.QLabel('Time', self)
        self.time_label.setFont(self.big_font)
        self.date_label = QtGui.QLabel('Date', self)
        self.date_label.setFont(self.small_font)
        
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

class Master(QtGui.QFrame):
    
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        
        screenShape = QtGui.QDesktopWidget().screenGeometry()
        self.width = screenShape.width()/3
        self.height = screenShape.height() - 50 
        self.resize(self.width, self.height) 
        
        self.frames = 3*[None]

        #create a list of widgets
        elements = 5*[None]
        for i in range(5):
            a = 'Name ' + str(i)
            b = 'Saturday, April ' + str(i)
            c = 'Description ' + str(i) + 'bvdjnsv vkmdsvd dvmlsdmvkd mvdk  vdk siiisv llsf nndsln v'
            d = 'Person ' + str(i)
            e = 'dog.png'
            elements[i] = Memory(name=a, date_time=b, descr=c, tagged_people=d, pic_filename=e, width=self.width, height=3*self.height/4)
            
        m = MainFrame(master=self, memories=elements, width=self.width, height=self.height)
        
        self.frames[0] = m
        
        steps = [{'title':'Step1','description':'Go to Mall'}, {'title':'Step2','description':'Get Frozen Yogurt'}, {'title':'Step3','description':'Pay'}]
        info = {'name':'Activity 1', 'datetime':'April 1, 2017', 'description':'Going to the mall for frozen yogurt', 'steps':steps}
        a = ActivityFrame(info, width=self.width, height=self.height)
        
        self.frames[1] = a

        sched = ScheduleFrame(width=self.width, height=self.height)
        self.frames[2] = sched        
        
        self.cw = QtGui.QStackedWidget()
        self.cw.addWidget(a)
        self.cw.addWidget(m)
        self.cw.addWidget(sched)
        
        self.cw.setCurrentWidget(m)
        
        self.grid = QtGui.QGridLayout()
        self.grid.addWidget(self.cw, 0, 0)
        self.setLayout(self.grid)
        
    def open_activity_screen(self):
         self.cw.setCurrentWidget(self.frames[1])
         
    def open_schedule_screen(self):
        self.cw.setCurrentWidget(self.frames[2])
        
    def read(self):
        '''read in a file of pickled objects or something'''
        pass
    def write(self):
        '''write all the variables to a file before closing'''
        pass
    


class MainFrame(BaseFrame):
    '''This is the main menu for the application'''
    def __init__(self, master=None, memories=[], width=0, height=0, parent=None):
        BaseFrame.__init__(self, width, height, parent)      
        
        self.master = master
        
        #create the scroll frame of elements
        self.scroll = ArrowScroll(memories, width=self.width, height=self.height*3/4)
        
        #create the mailbox icon
        self.mailbox = ButtonLabel(pic='mailbox.png', width=self.width/2, height=self.height/8)
        self.mailbox.clicked.connect(self.master.open_activity_screen)        
        
        #create the calendar icon
        self.calendar = ButtonLabel(pic='calendar.png', width=self.width/2, height=self.height/8)
        self.calendar.clicked.connect(self.master.open_schedule_screen) 
        
        #Add the widgets to the layout
        self.gridV.addWidget(self.scroll)
        self.gridV.addStretch(2)
        
        self.gridBot = QtGui.QHBoxLayout()
        self.gridBot.addWidget(self.mailbox)
        self.gridBot.addWidget(self.calendar)
        self.gridV.addLayout(self.gridBot)
                
        
class ArrowScroll(QtGui.QFrame):
    '''displays one widget from elements at a time. scroll through list with buttons'''
    
    def __init__(self, elements, width=0, height=0, parent=None): ##### Maybe make the width and height from the parent - like 3/4 the parent height
        '''elements is a list of widgets that are displayed'''
        QtGui.QFrame.__init__(self, parent)
        
        self.width = width
        self.height = height
        self.resize(self.width, self.height)         
        
        self.elements = elements
        self.n = len(self.elements)       
        
        #Create the layout manager
        self.grid = QtGui.QGridLayout()
        
        #The elements will be stored in a QStackedWidget so only one is available to view at a time
        self.cw = QtGui.QStackedWidget()
        for e in elements:
            self.cw.addWidget(e)
        
        #create a pointer of the currently displayed widget
        self.current = 0
        self.cw.setCurrentIndex(self.current)
            
        #Create the up and down buttons
        self.left = ButtonLabel(pic='left.png', width=self.width/2, height=self.height/8, flash=True, parent=self)
        self.left.clicked.connect(self.clicked_left)
        
        self.right = ButtonLabel(pic='right.png', width=self.width/2, height=self.height/8, flash=True, parent=self)
        self.right.clicked.connect(self.clicked_right)
        
        #add the widgets to the frame
        self.grid.addWidget(self.cw, 1, 0, 1, 2)
        self.grid.addWidget(self.left, 0, 0)
        self.grid.addWidget(self.right, 0, 1)
            
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

################## Make the buttons go horizontal - scroll horizontal ##################################
class ButtonLabel(QtGui.QLabel):
    '''A label with button-like behavior so you have clickable pictures'''
    
    clicked = QtCore.pyqtSignal()    
    
    def __init__(self, text=None, pic=None, flash=False, width=None, height=None, parent=None):
        '''text is a string, pic is a string to a filename, if flash is True then button will change color when clicked'''
        QtGui.QLabel.__init__(self, parent)
        
        self.flash = flash
        #self.palette = QtGui.QPalette()
        self.palette = self.palette()
        self.normal_color = self.palette.color(QtGui.QPalette.Background)
        
        font = QtGui.QFont()
        font.setPointSize(24)  
        
        self.setFont(font)
        
        #Add a border
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setFrameShadow(QtGui.QFrame.Raised)
        
        self.setAutoFillBackground(True) 
        self.palette.setColor(self.backgroundRole(), self.normal_color)
        self.setPalette(self.palette)

        if text != None:
            self.setText(text)
            
        if pic != None:
            self.pixmap = QtGui.QPixmap(pic)
            if width != None and height != None:
                self.pixmap = self.pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio)
            self.setPixmap(self.pixmap)

    def mousePressEvent(self, event):
        if self.flash:
            self.palette.setColor(self.backgroundRole(), QtCore.Qt.green)
            self.setPalette(self.palette)
     
    def mouseReleaseEvent(self, event):
        self.clicked.emit()
        
        if self.flash:
            self.palette.setColor(self.backgroundRole(), self.normal_color)
            self.setPalette(self.palette)


        
class ActivityFrame(BaseFrame):
    
    def __init__(self, activity, width=0, height=0, parent=None): #Instead of d, take in an activity object that makes the activity screen part
        '''d is a dictionary of activity attributes'''        
        
        BaseFrame.__init__(self, width, height, parent)
        
        self.activity = activity
        
        self.bigger_font = QtGui.QFont()
        self.bigger_font.setPointSize(36)
        
        #create a title
        self.title = QtGui.QLabel('Activity Suggestion')
        self.title.setFont(self.bigger_font)
        self.h1 = QtGui.QHBoxLayout()
        self.h1.addStretch(1)
        self.h1.addWidget(self.title)
        self.h1.addStretch(1)
        self.gridV.addLayout(self.h1)
        self.gridV.addStretch(1)
        
        #Create the main frame containing the information
        # self.frame = activity.get_frame()
        self.gridV.addWidget(self.frame)
        self.gridV.addStretch(15)
        

        
class ScheduleFrame(BaseFrame):

    def __init__(self, width=0, height=0, parent=None):
        BaseFrame.__init__(self, width, height, parent)
        
        self.cal = QtGui.QCalendarWidget()

        self.gridV.addWidget(self.cal)
        
        


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    
    m = Master()
    m.show()  
    
    sys.exit(app.exec_())
            
    
        