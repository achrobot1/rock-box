#!/usr/bin/env python3

import sys
import os

from viewrock_widget_class import *
from select_file_dialog import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from lxml import etree

class Display_window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Collection View")
        
        
        self.showFullScreen()
             
        self.create_rockpages()
        self.create_main_widget()
        
                
        self.setup_stacked_widget()
        self.stacked_widget.setCurrentWidget(self.main_widget)
                       
        self.central_widget = self.stacked_widget

        self.setCentralWidget(self.central_widget)

      
    def create_main_widget(self):
        #create the 12 pushbuttons
        self.rock_buttons = []
        for each in range(12):
            self.rock_buttons.append(QPushButton(str(each+1)))
            self.rock_buttons[each].setMinimumSize(100, 50)
        
        #grid layout
        self.rock_button_grid = QGridLayout()
        for each in range(6):
            self.rock_button_grid.addWidget(self.rock_buttons[each], 0, each)
        for each in range(6):
            self.rock_button_grid.addWidget(self.rock_buttons[each+6], 1, each)
    
        
        #exit button
        self.exit_button = QPushButton("Exit")
        self.exit_button.setMinimumSize(60, 40)
        
        
        #layout for exit button
        self.exit_button_layout = QHBoxLayout()
        self.exit_button_layout.addWidget(self.exit_button)
        self.exit_button_layout.addStretch(1)

        #layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.rock_button_grid)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.exit_button_layout)
        
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        
        #connections
        self.exit_button.clicked.connect(exit)
        
               
        for each in range(12):
            self.rock_buttons[each].released.connect(lambda x=each: self.update_page(self.rockpages[x]))
          
        
    def create_rockpages(self):
        self.rockpages = []
                   
        for each in range(12):
            self.rockpages.append(ViewRockWidget())
            
        for each in range(12):
            self.rockpages[each].menu_button.clicked.connect(lambda: self.update_page(self.main_widget))
            
            
        self.read_xml()     
    
    def get_path(self):
        #return the path of the .xml file the user wants to display
        
        # self.usb_path = '/home/pi/mnt/usb0/'
        self.usb_path = '/pwd/'
        
        if len(os.listdir(self.usb_path)) == 0:
            #Error dialog, USB not found
            QMessageBox.warning(self, "Message", "USB drive missing. Unable to display your collection")
            exit()
            
        self.d = SelectFileDialog()
        for File in os.listdir(self.usb_path):
            if File.endswith('.xml'):
                self.d.text_list.addItem(str(File))
        #connections
        self.d.select_button.clicked.connect(self.get_file)
        self.d.exec_()
        return self.xml_file
        
    def get_file(self):
        #used to return the selected .xml file from self.d dialog in get_path()
        self.xml_file =  self.usb_path + self.d.text_list.currentItem().text()
        self.d.close()    
            
    def read_xml(self):
        #read xml file and insert text into textEdits and set date for calendars
        self.xml_path = self.get_path()
        root = etree.parse(self.xml_path).getroot()
        rocks = root.getchildren()

        for each in range(12):
            self.rockpages[each].name_label.setText(rocks[each][0].text)
            self.rockpages[each].info_label.setText(rocks[each][2].text)
            self.rockpages[each].source_label.setText(rocks[each][3].text)
            
            if rocks[each][1][0].text != None and rocks[each][1][1].text !=None and rocks[each][1][2].text != None and rocks[each][0].text != None:
                day = int(rocks[each][1][0].text)
                month = int(rocks[each][1][1].text)
                year = int(rocks[each][1][2].text)
                self.rockpages[each].date_label.setText(QDate(year, month, day).toString())
                
    def setup_stacked_widget(self):
        #create a stacked layout to hold widgets for the main menu and rock edit pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.main_widget)
        
        for each in range(12):
            self.stacked_widget.addWidget(self.rockpages[each])
        
    def update_page(self, widget):
        #display the proper edit rock page when a button is pressed        
        self.stacked_widget.setCurrentWidget(widget)
        if widget != self.main_widget:
            self.setStyleSheet("QMainWindow { border-image: url('../images/background2.png'); }")
        else:
            self.setStyleSheet("QMainWindow { border-image: url('../images/background.png'); }")

def main():  
    rock_display_application = QApplication(sys.argv)
    rock_display_application.setStyle('plastique')
    style_sheet = open('../style_sheets/turkoi_sheet.qss').read()
    rock_display_application.setStyleSheet(style_sheet)
    display_window = Display_window() #create new instance of main window
    display_window.show()
    display_window.raise_() # raise instance to top of window stack
    rock_display_application.exec_() #monitor application for events

if __name__ == "__main__":
    main()
