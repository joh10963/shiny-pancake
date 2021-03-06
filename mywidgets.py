# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 20:43:25 2017

@author: diana
"""
from PyQt4 import QtCore, QtGui

#Create some font sizes
font_24 = QtGui.QFont()
font_24.setPointSize(24)

font_18 = QtGui.QFont()
font_18.setPointSize(18)

class EntryAndButton(QtGui.QGridLayout):
    
    def __init__(self, parent=None):
        QtGui.QGridLayout.__init__(self, parent)
        
        self.entry = QtGui.QLineEdit()
        self.button = QtGui.QPushButton('Browse')

        self.addWidget(self.entry, 0, 0)
        self.addWidget(self.button, 0, 1)

        self.button.clicked.connect(self.browse_files)
        
    def browse_files(self):
        print 'entered browse files'
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Select Picture')
        self.entry.setText(filename)
        
    def text(self):
        return self.entry.text()
        
    def clear(self):
        self.entry.clear()
        
class EntryAndLabel(QtGui.QGridLayout):
    
    def __init__(self, parent=None):
        QtGui.QGridLayout.__init__(self, parent)
        
        self.tags = []
        
        self.label = QtGui.QLabel()
        #self.label.setWordWrap(True)
        self.entry = QtGui.QLineEdit()
        self.button = QtGui.QPushButton('Tag')
        
        self.addWidget(self.label, 0, 0, 1, 2)
        self.addWidget(self.entry, 1, 0)
        self.addWidget(self.button, 1, 1)
        
        self.button.clicked.connect(self.add_tag)
        self.entry.returnPressed.connect(self.add_tag)
        
    def add_tag(self):
        self.tags.append(self.entry.text())
        self.entry.clear()
        line = ''
        for tag in self.tags:
            line += tag + ', '
        line = line[0:-2]
        self.label.setText(line)
        
    def clear(self):
        self.entry.clear()
        self.label.setText('')
    
    def get_tags(self):
        return self.tags
        
class ChooseDate(QtGui.QGridLayout):
    
    dateChanged = QtCore.pyqtSignal()
    
    def __init__(self, parent=None, date=None):
        QtGui.QGridLayout.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)
        
        self.date = date
        
        self.label = QtGui.QLabel()
        self.label.setText('              ')
        self.button = QtGui.QPushButton('Browse Dates')
        self.calendar = QtGui.QCalendarWidget()
        self.calendar.setGeometry(self.button.x(), self.button.y(), 300, 300)
        self.calendar.clicked.connect(self.select_date)
        
        self.addWidget(self.label, 0, 0)
        self.addWidget(self.button, 0, 1)
        
        self.button.clicked.connect(self.browse_dates)
        
    def changed(self):
        self.dateChanged.emit()
        
    def browse_dates(self):
        self.calendar.show()
        
    def select_date(self):
        self.calendar.hide()
        self.date = self.calendar.selectedDate()
        self.label.setText(self.date.toString())
        self.dateChanged.emit()
        
    def setDate(self, date):
        self.date = date
        self.label.setText(self.date.toString())
        self.dateChanged.emit()
        
    def clear(self):
        self.label.setText('          ')
        
    def setText(self, text):
        self.label.setText(text)
    
    def toString(self):
        if self.date == None:
            return ''
        else:
            return self.date.toString()
        
    def get_date(self):
        print 'entered date'
        return self.date
        
        
class ChooseTime(QtGui.QGridLayout): ###########make it curcle around, start at 12, do 00 01....
    
    timeChanged = QtCore.pyqtSignal()
    
    def __init__(self, parent=None, time=None):
        QtGui.QGridLayout.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)

        self.hour = QtGui.QSpinBox()
        self.minute = QtGui.QSpinBox()
        self.second = QtGui.QSpinBox()
        self.ampm = QtGui.QComboBox()
        self.label = QtGui.QLabel(':')
        
        self.hour.setRange(1, 12)
        self.hour.setValue(12)
        self.hour.valueChanged.connect(self.changed)
        self.minute.setRange(0, 59)
        self.minute.setValue(0)
        self.minute.valueChanged.connect(self.changed)
        self.second.setRange(0, 59)
        self.second.setValue(0)
        self.second.valueChanged.connect(self.changed)
        self.ampm.addItem('AM')
        self.ampm.addItem('PM')
        self.ampm.currentIndexChanged.connect(self.changed)
        
        self.addWidget(self.hour, 0, 0)
        self.addWidget(self.label, 0, 1)
        self.addWidget(self.minute, 0, 2)
        self.addWidget(self.second, 0, 3)
        self.addWidget(self.ampm, 0, 4)
        
        if time != None:
            self.setText(time)
    
    def changed(self):
        self.timeChanged.emit()
    
    def setText(self, time):
        '''time is a QTime object'''
        if time.hour() > 12:
            self.hour.setValue(time.hour()-12)
            self.ampm.setCurrentIndex(1) #set it to pm
        else:
            self.hour.setValue(time.hour())
        self.minute.setValue(time.minute())
        self.second.setValue(time.second())
        
    def time(self):
        '''return a QTime object'''
        hour = self.hour.value()
        minute = self.minute.value()
        second = self.second.value()
        ampm = self.ampm.currentText()
        
        if ampm == 'PM':
            hour = hour + 12
            
        return QtCore.QTime(hour, minute, second)
        
    def toString(self):
        time = self.time()
        return time.toString()
        
    def text(self):
        hour = self.hour.value()
        minute = self.minute.value()
        if hour < 10:
            hour = '0' + str(hour)
        else:
            hour = str(hour)
        if minute < 10:
            minute = '0' + str(minute)
        else:
            minute = str(minute)
        return hour + ':' + minute + ' ' + self.ampm.currentText()

class BaseFrame(QtGui.QFrame):
    '''Creates a Frame widget that displays the current date and time'''
    def __init__(self, width=0, height=0, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.master_grid = QtGui.QVBoxLayout()

        self.width = width
        self.height = height
        self.resize(self.width, self.height) 
        
        self.screen = QtGui.QFrame()
        self.screen.resize(self.width, self.height)
        #self.screen.setGeometry(self.width-120, self.height-120, self.width-240, self.height-240)
        self.screen.setFrameShape(QtGui.QFrame.Panel)
        self.screen.setFrameShadow(QtGui.QFrame.Plain)
        self.screen.setLineWidth(5)
        self.screen.setContentsMargins(30, 40, 30, 30)
        #self.screen.setContentsMargins(0, 0, 0, 0)
        
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
        
        self.frame = QtGui.QFrame()
        self.grid = QtGui.QGridLayout()
        self.frame.setLayout(self.grid)
        
        self.gridV.addWidget(self.frame)
    
        self.screen.setLayout(self.gridV)
        
        self.master_grid.addWidget(self.screen)
        self.setLayout(self.master_grid)
        
        
        #Set a timer to update the date and time periodically
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_display)
        self.update_display()
        self.timer.start()
        
    def update_display(self):
        self.time_label.setText(QtCore.QDateTime.currentDateTime().time().toString())
        self.date_label.setText(QtCore.QDateTime.currentDateTime().date().toString())
        
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        
        #draw the outside
        qp.setPen(QtGui.QColor(QtCore.Qt.black))
        qp.drawRoundRect(10, 10, self.width-20, self.height-15, 15, 15)
        
        #draw the line on top
        qp.drawRect(self.width/2-20, 30, 40, 10)
        
        #draw the circle on the bottom
        qp.drawEllipse(self.width/2-20, self.height-50, 40, 40)
        		
        qp.end()
        
class Calendar(QtGui.QCalendarWidget):
    '''calendar that fills in each day with a color corresponding to caregivers availabilities'''
    def __init__(self, parent=None, caregivers=None, colors=None, width=400, height=475):
        QtGui.QCalendarWidget.__init__(self, parent)
        
        self.setNavigationBarVisible(False)
        self.setHorizontalHeaderFormat(QtGui.QCalendarWidget.SingleLetterDayNames)
        
        self.width = width
        self.height = height
        self.setMaximumSize(self.width, self.height)
        
        self.caregiver_list = caregivers
        self.color_list = colors
        
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
        for caregiver in self.caregiver_list:
            if caregiver.get_availability()[day%7] == 1:
                fill = True
                color = self.color_list[self.caregiver_list.index(caregiver)]
                
        return fill, color
        
class AvailabilityCalendar(QtGui.QGridLayout):
    
    def __init__(self, parent=None, caregivers=None, colors=None):
        QtGui.QGridLayout.__init__(self, parent)
        
        self.caregivers = caregivers
        self.colors = colors        
        self.n = len(self.caregivers)
        
        self.calendar = Calendar(caregivers=self.caregivers, colors=self.colors)
        self.calendar.updateCells()
        self.addWidget(self.calendar, 0, 0, 1, self.n)
        
        self.keys = []
        for i in range(self.n):
            l = QtGui.QLabel()
            l.setText(self.caregivers[i].get_name())
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Foreground, self.colors[i])
            l.setPalette(palette)
            self.keys.append(l)
            self.addWidget(l, 1, i)
            
    def update(self):
        self.calendar.updateCells()
        
        
        
class MemoryBrowse(QtGui.QFrame):
    '''displays one widget from elements at a time. scroll through list with buttons'''   
    
    def __init__(self, parent=None, elements=None, tags=None, locs=None, account=None, small=False): 
        QtGui.QFrame.__init__(self, parent)        
        
        self.account = account
        self.elements = elements
        self.tags = tags
        self.locs = locs
        self.elements.reverse()
        self.n = len(self.elements)       
        
        #Create the layout manager
        self.grid = QtGui.QGridLayout()
        
        #The elements will be stored in a QStackedWidget so only one is available to view at a time
        self.cw = QtGui.QStackedWidget()
        for e in self.elements:
            self.cw.addWidget(e)
        
        #create a pointer of the currently displayed widget
        self.current = 0
        self.cw.setCurrentIndex(self.current)
            
        #Create the up and down buttons
        self.left = QtGui.QPushButton('Previous')
        self.left.clicked.connect(self.clicked_left)
        
        self.right = QtGui.QPushButton('Next')
        self.right.clicked.connect(self.clicked_right)
        
        #Return to home button
        self.home_button = QtGui.QPushButton('Main Menu')
        self.home_button.clicked.connect(self.account.goto_home_screen)
        
        
        #add the widgets to the frame
        if not small:
            self.grid.addWidget(self.home_button, 0, 0)
        self.grid.addWidget(self.cw, 1, 0, 1, 2)
        self.grid.addWidget(self.left, 2, 0)
        self.grid.addWidget(self.right, 2, 1)
        
        #Add the searching tools
        self.search_layout = QtGui.QFormLayout()
        
        self.tags_search = QtGui.QComboBox()
        self.tags_search.addItems(self.tags)
        self.loc_search = QtGui.QComboBox()
        self.loc_search.addItems(self.locs)
        self.date_search = ChooseDate()
        self.search_button = QtGui.QPushButton('Search')
        self.search_button.clicked.connect(self.search)
        
        self.search_layout.addRow('Tags', self.tags_search)
        self.search_layout.addRow('Location', self.loc_search)
        self.search_layout.addRow('Date', self.date_search)
        self.search_layout.addRow(self.search_button)
        
        if not small:
            self.grid.addLayout(self.search_layout, 3, 0, 1, 2)
            
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
            
    def add_element(self, element, tags, locs):
        '''add the element to the front of the list, set as current widget'''
        self.tags = tags
        self.locs = locs
        self.elements.insert(0, element)
        self.cw.insertWidget(0, element)
        
        self.current = 0
        self.cw.setCurrentIndex(self.current)
        #Uodate other things
        self.tags_search.clear()
        self.tags_search.addItems(self.tags)
        self.loc_search.clear()
        self.loc_search.addItems(self.locs)

        
    def search(self):
        tag = self.tags_search.currentText()
        loc = self.loc_search.currentText()
        date = self.date_search.toString()
        
        self.elements = self.account.search(tag=tag, loc=loc, date=date) #returns the memories in search order
        
        #remove all the widgets in the stack
        for i in range(self.cw.count()):
            widget = self.cw.widget(i)            
            self.cw.removeWidget(widget)
            
        #add in the new order
        for e in self.elements:
            self.cw.addWidget(e)
            
        self.cw.setCurrentIndex(0)

class Example(QtGui.QFrame):

   def __init__(self):
      super(Example, self).__init__()
      self.initUI()
		
   def initUI(self):
      self.text = "hello world"
      self.setGeometry(100,100, 400,300)
      self.setWindowTitle('Draw Demo')
      self.show()
		
   def paintEvent(self, event):
      qp = QtGui.QPainter()
      qp.begin(self)
      qp.setPen(QtGui.QColor(QtCore.Qt.red))
      qp.setFont(QtGui.QFont('Arial', 20))
		
      qp.drawText(10,50, "hello Python")
      qp.setPen(QtGui.QColor(QtCore.Qt.blue))
      qp.drawLine(10,100,100,100)
      qp.drawRect(10,150,150,100)
		
      qp.setPen(QtGui.QColor(QtCore.Qt.yellow))
      qp.drawEllipse(100,50,100,50)
      qp.fillRect(200,175,150,100, QtGui.QBrush(QtCore.Qt.SolidPattern))
      qp.end()
        
if __name__ == "__main__":
    import os
    import sys

    app = QtGui.QApplication(sys.argv)
    
    screenShape = QtGui.QDesktopWidget().screenGeometry()
    width = screenShape.width()/3
    height = screenShape.height() - 80   
    
    b = BaseFrame(width=width, height=height)
    b.show()
    
#    e = Example()
#    e.show()
    
    sys.exit(app.exec_())       
        
        
        
        
        
        
        
        
        
        
        
        
        
        