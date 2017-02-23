# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 19:54:14 2017

@author: diana
"""

import sys, os
from PyQt4 import QtCore, QtGui

class BaseFrame(QtGui.QFrame):
    '''Creates a Frame widget that displays the current date and time'''
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        
        #Set the size of the frame
        self.screenShape = QtGui.QDesktopWidget().screenGeometry()
        self.width = self.screenShape.width()/3
        self.height = self.screenShape.height()-50
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


class MainWindow(QtGui.QMainWindow):
 
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        
        #Set the size of the window
        self.screenShape = QtGui.QDesktopWidget().screenGeometry()
        self.width = self.screenShape.width()/3
        self.height = self.screenShape.height()
        self.resize(self.width, self.height)         
        
        self.cw = QtGui.QStackedWidget(self)
        self.setCentralWidget(self.cw)  
        
        #Create all the frames here
        
        #main frame
        self.main_frame = MainFrame(self)
        
        #individual profile frames
        self.profile_info = {'profile 1': {'name':'Puppy Number 1', 'file':'dog.png'},
                             'profile 2': {'name':'Puppy Number 2', 'file':'dog.png'},
                             'profile 3': {'name':'Puppy Number 3', 'file':'dog.png'},
                             'profile 4': {'name':'Puppy Number 4', 'file':'dog.png'},
                             'profile 5': {'name':'Puppy Number 5', 'file':'dog.png'},
                             'profile 6': {'name':'Puppy Number 6', 'file':'dog.png'},
                             'profile 7': {'name':'Puppy Number 7', 'file':'dog.png'},
                             'profile 8': {'name':'Puppy Number 8', 'file':'dog.png'}
                             }
        for prof in self.profile_info.iterkeys():
            self.profile_info[prof]['memories'] = {}
            self.profile_info[prof]['memories']['Event 1'] = {'date_time':'Feb 1, 2017', 'descr':'A Description of the event. It can be really really long and blah blah blah', 'tagged_people':'Diana I, Diana II, Diana III', 'pic_filename':'dog.png'}
            self.profile_info[prof]['memories']['Event 2'] = {'date_time':'march 1, 2016', 'descr':'A Description of the event. It can be really really long and blah blah blah', 'tagged_people':'Diana I, Diana II, Diana III', 'pic_filename':'dog.png'}
            self.profile_info[prof]['memories']['Event 3'] = {'date_time':'Jan 14, 1994', 'descr':'A Description of the event. It can be really really long and blah blah blah', 'tagged_people':'Diana I, Diana II, Diana III', 'pic_filename':'dog.png'}
            self.profile_info[prof]['memories']['Event 4'] = {'date_time':'Aug 5, 1589', 'descr':'A Description of the event. It can be really really long and blah blah blah', 'tagged_people':'Diana I, Diana II, Diana III', 'pic_filename':'dog.png'}
            self.profile_info[prof]['memories']['Event 5'] = {'date_time':'May 6, 2019', 'descr':'A Description of the event. It can be really really long and blah blah blah', 'tagged_people':'Diana I, Diana II, Diana III', 'pic_filename':'dog.png'}
            self.profile_info[prof]['memories']['Event 6'] = {'date_time':'July 4, 1498', 'descr':'A Description of the event. It can be really really long and blah blah blah', 'tagged_people':'Diana I, Diana II, Diana III', 'pic_filename':'dog.png'}
        self.profile_list = 8*[None]
        self.full_profile_list = 8*[None]
        self.memories = 8*[None]
        i = 0
        for key, d in self.profile_info.iteritems():
            self.profile_list[i] = SmallProfileFrame(d['name'], d['file'])
            self.profile_list[i].clicked.connect(lambda name=i:self.go_to_individual_profile(name))
            temp_list = 6*[None]
            j = 0
            for mem, dic in d['memories'].iteritems():
                temp_list[j] = Memory(mem, dic['date_time'], dic['descr'], dic['tagged_people'], dic['pic_filename'])
                j += 1
            self.memories[i] = temp_list
            self.full_profile_list[i] = BigProfileFrame(self, d['name'], d['file'], self.memories[i])
            self.cw.addWidget(self.full_profile_list[i])
            i += 1
        
        #list of profiles frame
        self.profiles_frame = ProfilesFrame(self, self.profile_list)
        
        
    
        #add them to the stack widget
        self.cw.addWidget(self.main_frame)
        self.cw.addWidget(self.profiles_frame)
        
        self.change_screen(self.main_frame)
        self.change_screen(self.profiles_frame)
        self.change_screen(self.main_frame)
        
        self.show()
        
    def change_screen(self, frame):
        self.cw.setCurrentWidget(frame)
        
    def go_to_profiles_screen(self):
        self.change_screen(self.profiles_frame)
        
    def go_to_main_screen(self):
        self.change_screen(self.main_frame)
        
    def go_to_individual_profile(self, key):
        self.change_screen(self.full_profile_list[key])

class MainFrame(BaseFrame):
    '''This is the main menu for the application'''
    def __init__(self, mainwindow, parent=None):
        BaseFrame.__init__(self, parent)
        
        self.mainwindow = mainwindow        
        
        #Create a really big font so the buttons are bigger
        self.giant_font = QtGui.QFont()
        self.giant_font.setPointSize(44)        
        
        #Add the update frame
        self.update_frame = UpdateFrame(parent=self)
        self.gridV.addWidget(self.update_frame) 
        self.gridV.addStretch(3)
        
        #Create the buttons
        self.profile_but = QtGui.QPushButton('Profiles', self)
        self.profile_but.setFont(self.giant_font)
        self.activities_but = QtGui.QPushButton('Suggest an Activity', self)
        self.activities_but.setFont(self.giant_font)
        self.schedule_but = QtGui.QPushButton('Schedule', self)
        self.schedule_but.setFont(self.giant_font)
        
        #Place the buttons at the bottom of the screen
        self.gridV.addWidget(self.profile_but)
        self.gridV.addWidget(self.activities_but)
        self.gridV.addWidget(self.schedule_but)
        
        #Connect signals to the buttons
        self.profile_but.clicked.connect(self.mainwindow.go_to_profiles_screen)
        
        
class UpdateFrame(QtGui.QFrame):
    '''Used in the MainFrame to display updates -- either memories or suggested activities'''
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        
        self.setFrameShape(QtGui.QFrame.StyledPanel)        
        
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
               
        
        self.title_font = QtGui.QFont()
        self.title_font.setPointSize(36)        
        
        #Create two labels -- one for the top half and one for the bottom
        self.top_label = QtGui.QLabel(self)
        self.top_label.setFont(self.title_font)
        self.bottom_label = QtGui.QLabel(self)
        self.bottom_label.setFont(self.title_font)
        
        #Add the labels to the grid
        self.grid = QtGui.QGridLayout()
        
        self.grid.addWidget(self.top_label, 0, 0)
        self.grid.addWidget(self.bottom_label, 2, 0)        
        
        self.setLayout(self.grid)

        #Keep track of what widgets are in the top half and bottom half
        self.top_widget = None
        self.bottom_widget = None
        
        descr = 'This is a really really long descmvdkls mvdkslmvk dmksvmkdsl mvdksl mvkds mkvds mvklsjgnrnmmd vdl'
        mem = Memory('Memory Number 1', 'Feb 16, 2017', descr, 'Diana, Diana I', 'dog.png')
        act = Activity('Go Bowling', 'Feb 21, 2017', 'Go bowling with your nephew at Bowling Alley Name to celebrate his 5th birthday.')
        
        self.add_update(mem, 'Memory Update')
        self.add_update(act, 'Suggested Activity')
        
    ######################### Maybe be more specific like add_memory_update or activity_update
    def add_update(self, widget, label):
        if self.top_widget == None and self.bottom_widget == None: #If nothing is in the top add the new widget there
            self.top_widget = widget
            self.top_label.setText(label)
            self.grid.addWidget(widget, 1, 0)
        elif self.bottom_widget == None: 
            self.bottom_widget = widget
            self.bottom_label.setText(label)
            self.grid.addWidget(widget, 3, 0)
        else: #move the bottom widget to the top and add the new widget to the bottom
            self.top_widget = self.bottom_widget
            self.top_label.setText(self.bottom_label.text())
            self.grid.addWidget(self.top_widget, 1, 0)            
            self.bottom_widget = widget
            self.bottom_label.setText(label)
            self.grid.addWidget(widget, 3, 0)
                
class ProfilesFrame(BaseFrame):
    
    title_font = QtGui.QFont()
    title_font.setPointSize(24)    
    
    def __init__(self, mainwindow, profile_widgets, parent=None):
        BaseFrame.__init__(self, parent)

        self.mainwindow = mainwindow    
        self.profile_widgets = profile_widgets
        
        self.gridH2 = QtGui.QHBoxLayout()  
        self.grid = QtGui.QVBoxLayout()
        
        #Create the title label
        self.title = QtGui.QLabel('Profiles', self)
        self.title.setFont(ProfilesFrame.title_font)
        self.gridH2.addStretch(1)
        self.gridH2.addWidget(self.title)
        self.gridH2.addStretch(1)
        self.grid.addLayout(self.gridH2)
        
        #Make a scroll area        
        self.create_scroll_frame()
        self.scroll_area = QtGui.QScrollArea()
        self.scroll_area.setWidget(self.scroll_frame)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(self.height/3*2)
        self.grid.addWidget(self.scroll_area)     
        
        #Create Add new profile Button
        self.add_button = QtGui.QPushButton('Add New Profile')
        self.add_button.setFont(self.small_font)
        self.grid.addWidget(self.add_button)
        
        #Create main menu button
        self.main_menu_button = QtGui.QPushButton('Back to Main Menu')
        self.main_menu_button.setFont(self.small_font)
        self.main_menu_button.clicked.connect(self.mainwindow.go_to_main_screen)
        self.grid.addWidget(self.main_menu_button)
        
        self.gridV.addLayout(self.grid)
        self.gridV.addStretch(1)
         
    def create_scroll_frame(self):
        '''this is the frame that contains all the profiles, only partial is visible'''
        self.scroll_frame = QtGui.QFrame(self)
        self.scroll_grid = QtGui.QVBoxLayout()
        
        for w in self.profile_widgets:
            self.scroll_grid.addWidget(w)
        
        self.scroll_frame.setLayout(self.scroll_grid)
        
    
class SmallProfileFrame(QtGui.QFrame):
    
    font = QtGui.QFont()
    font.setPointSize(24)      
    
    clicked = QtCore.pyqtSignal()    
    
    def __init__(self, name, pic_filename, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.setFrameShape(QtGui.QFrame.Box)
        
        #Set the size
        self.screenShape = QtGui.QDesktopWidget().screenGeometry()
        self.width = self.screenShape.width()/3
        self.height = self.screenShape.height()/5
        self.resize(self.width, self.height) 
        
        self.grid = QtGui.QGridLayout()        
        
        #Add a label
        self.name = QtGui.QLabel(name, self)
        self.name.setFont(SmallProfileFrame.font)
        self.grid.addWidget(self.name, 0, 1)
        
        #Add the picture
        self.pic = QtGui.QLabel(self)
        self.pixmap = QtGui.QPixmap(pic_filename)
        new_pixmap = self.pixmap.scaled(self.width/4, self.height, QtCore.Qt.KeepAspectRatio)
        self.pic.setPixmap(new_pixmap)
        self.grid.addWidget(self.pic, 0, 0)
        
        self.setLayout(self.grid) 
        
    def mouseReleaseEvent(self, event):
        self.clicked.emit()
        
class BigProfileFrame(BaseFrame):
    
    def __init__(self, mainwindow, name, pic_filename, memories_list, parent=None):
        BaseFrame.__init__(self, parent)
        
        self.memories_list = memories_list   
        self.mainwindow = mainwindow
        
        self.setFrameShape(QtGui.QFrame.Box)    
        
        self.grid = QtGui.QFormLayout()        
        
        #Name label
        self.name = QtGui.QLabel(name, self)
        self.name.setFont(self.big_font)
        
        #Add the picture
        self.pic = QtGui.QLabel(self)
        self.pixmap = QtGui.QPixmap(pic_filename)
        new_pixmap = self.pixmap.scaled(self.width/4, self.height, QtCore.Qt.KeepAspectRatio)
        self.pic.setPixmap(new_pixmap)

        self.grid.addRow(self.name, self.pic)
        
        #Address
        self.address = QtGui.QLabel('Add Address', self)
        self.address.setFont(self.small_font)
        self.grid.addRow('Address', self.address)

        #Phone
        self.phone = QtGui.QLabel('Add Phone Number', self)
        self.phone.setFont(self.small_font)
        self.grid.addRow('Phone Number', self.phone)
        
        #Description
        self.description = QtGui.QLabel('Add Description', self)
        self.description.setFont(self.small_font)
        self.grid.addRow('Description', self.description)
        
        #Memory label
        self.memories_label = QtGui.QLabel('Memories', self)
        self.memories_label.setFont(self.big_font)
        self.grid.addRow(self.memories_label)
        
        #Make a scroll area        
        self.create_scroll_frame()
        self.scroll_area = QtGui.QScrollArea()
        self.scroll_area.setWidget(self.scroll_frame)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(self.height/2)
        self.grid.addRow(self.scroll_area) 

        self.main_menu_button = QtGui.QPushButton('Back to Main Menu')
        self.main_menu_button.setFont(self.small_font)
        self.main_menu_button.clicked.connect(self.mainwindow.go_to_main_screen)
        self.grid.addRow(self.main_menu_button)        
        
        self.gridV.addLayout(self.grid)
        self.gridV.addStretch(3)
 

    def create_scroll_frame(self):
        '''this is the frame that contains all the memories, only partial is visible'''
        self.scroll_frame = QtGui.QFrame(self)
        self.scroll_grid = QtGui.QGridLayout()
        
        i = 0
        for mem in self.memories_list:
            self.scroll_grid.addWidget(mem, i, 0)
            i += 1
        
        self.scroll_frame.setLayout(self.scroll_grid)

class Memory(QtGui.QFrame):
    
    big_font = QtGui.QFont()
    big_font.setPointSize(24)  
    
    small_font = QtGui.QFont()
    small_font.setPointSize(16) 
    
    def __init__(self, name, date_time, descr, tagged_people, pic_filename, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.setFrameShape(QtGui.QFrame.Box)         
        self.grid = QtGui.QGridLayout()        
        
        screenShape = QtGui.QDesktopWidget().screenGeometry()
        width = screenShape.width()/3
        height = screenShape.height()         
        
        #Add the picture
        self.pic = QtGui.QLabel(self)
        self.pixmap = QtGui.QPixmap(pic_filename)
        new_pixmap = self.pixmap.scaled(width/4, height, QtCore.Qt.KeepAspectRatio)
        self.pic.setPixmap(new_pixmap)
        self.grid.addWidget(self.pic, 0, 0, 3, 1)        
        
        #Add the labels
        self.name = QtGui.QLabel(name, self)
        self.name.setFont(Memory.big_font)
        self.grid.addWidget(self.name, 0, 1)
        
        self.datetime = QtGui.QLabel(date_time, self)
        self.datetime.setFont(Memory.big_font)
        self.grid.addWidget(self.datetime, 1, 1)
        
        self.tags = QtGui.QLabel(tagged_people, self) ############These need to be clickable labels
        self.tags.setFont(Memory.big_font)
        self.grid.addWidget(self.tags, 2, 1)
        
        #Add the description
        self.descr = QtGui.QLabel(descr, self)
        self.descr.setWordWrap(True)
        self.descr.setFont(Memory.small_font)
        self.grid.addWidget(self.descr, 3, 0, 1, 2)
        
        self.setLayout(self.grid) 
        
class Activity(QtGui.QFrame):
    
    big_font = QtGui.QFont()
    big_font.setPointSize(24)  
    
    small_font = QtGui.QFont()
    small_font.setPointSize(16) 
    
    def __init__(self, name, date_time, descr, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.setFrameShape(QtGui.QFrame.Box)         
        self.grid = QtGui.QGridLayout()        
        
        screenShape = QtGui.QDesktopWidget().screenGeometry()
        width = screenShape.width()/3
        height = screenShape.height()              
        
        #Add the labels
        self.name = QtGui.QLabel(name, self)
        self.name.setFont(Activity.big_font)
        self.grid.addWidget(self.name, 0, 0, 1, 2)
        
        self.datetime = QtGui.QLabel(date_time, self)
        self.datetime.setFont(Activity.small_font)
        self.grid.addWidget(self.datetime, 1, 0, 1, 2)
        
        #Add the description
        self.descr = QtGui.QLabel(descr, self)
        self.descr.setWordWrap(True)
        self.descr.setFont(Activity.small_font)
        self.grid.addWidget(self.descr, 2, 0, 1, 2)
        
        #Add the accept and decline buttons
        self.accept_button = QtGui.QPushButton('Accept')
        self.accept_button.setFont(Activity.small_font)
        self.grid.addWidget(self.accept_button, 3, 0)
        
        self.decline_button = QtGui.QPushButton('Decline')
        self.decline_button.setFont(Activity.small_font)
        self.grid.addWidget(self.decline_button, 3, 1)
        
        self.setLayout(self.grid) 

       
if __name__ == "__main__":
    #Date and Time displayed at the top of each frame
    #Add Memory Button
    #Edit on individual profiles so it turns into TextBoxes
    #Step-by-step activity screen once it it suggested
    #Main menu bottom half is used for Memory Updates, Activity Suggestions 
    #Third button on the home screen that says schedule and links
    #   to a list of Day of Activity-Details for each scheduled activity 

    app = QtGui.QApplication(sys.argv)

#    main_frame = MainMenu()
#    
#    profile_window = ProfilesMenu()
    
    window = MainWindow()
#    base = MainFrame()
#    base.show()
#    
#    descr = 'This is a really really long descmvdkls mvdkslmvk dmksvmkdsl mvdksl mvkds mkvds mvklsjgnrnmmd vdl'
#    mem = Memory('Memory', 'Sunday Feb 16', descr, 'Me, Myself, I', 'dog.png')
#    mem.show()
    
#    prof = ProfilesFrame()
#    prof.show()

 
    sys.exit(app.exec_())