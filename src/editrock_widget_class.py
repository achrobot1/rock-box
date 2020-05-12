from PyQt4.QtCore import *
from PyQt4.QtGui import *

import wikipedia

class EditRockWidget(QWidget):
    """Widget holding layout of the edit rock pages"""
    
    def __init__(self, index):
    
        super().__init__()
        self.index = index
        self.test_label = QLabel(str(index+1))
        
        #labels
        self.name_label = QLabel("Name: ")
        self.info_label = QLabel("Information: ")
        self.source_label = QLabel("Source: ")
        self.date_label = QLabel("Date added: ")
        
        #text edits
        self.name_edit = QPlainTextEdit()       
        self.info_edit = QPlainTextEdit()
        self.source_edit = QPlainTextEdit()
        
        self.name_edit.setMaximumHeight(40)
        self.source_edit.setMaximumHeight(70)

        self.name_edit.setTabChangesFocus(True)
        self.info_edit.setTabChangesFocus(True)
        self.source_edit.setTabChangesFocus(True)
        
        #buttons
        self.menu_button = QPushButton("Main Menu")
        self.menu_button.setMinimumHeight(40)

        self.wiki_button = QPushButton("")
        self.wiki_button.setMinimumSize(30, 30)  
        #icons
        self.home_icon = QIcon.fromTheme("go-home")
        self.menu_button.setIcon(self.home_icon)
        
        self.wiki_icon = QIcon("/home/pi/Documents/rock-box/images/wikipedia.png")
        self.wiki_button.setIcon(self.wiki_icon)
                        
        #connections
        self.wiki_button.clicked.connect(self.insert_wiki_text)
                
        #calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setMaximumWidth(500)

        #menu button layout
        self.menu_button_layout = QHBoxLayout()
        self.menu_button_layout.addWidget(self.menu_button)
        self.menu_button_layout.addStretch()
        
        #grid layout
        self.editrock_layout = QGridLayout()
        self.editrock_layout.setSpacing(30)
        
        self.editrock_layout.addWidget(self.name_label, 0, 0)
        self.editrock_layout.addWidget(self.info_label, 1, 0)
        self.editrock_layout.addWidget(self.source_label, 2, 0)
        self.editrock_layout.addWidget(self.date_label, 3, 0)
        self.editrock_layout.addWidget(self.test_label, 4, 0)
        
        self.editrock_layout.addWidget(self.name_edit, 0, 1)
        self.editrock_layout.addWidget(self.info_edit, 1, 1)
        self.editrock_layout.addWidget(self.source_edit, 2, 1)
        self.editrock_layout.addWidget(self.calendar, 3, 1)
        self.editrock_layout.addWidget(self.menu_button, 4, 1)
        
        self.editrock_layout.addWidget(self.wiki_button, 1, 2)
        
        self.complete_layout = QVBoxLayout()
        self.complete_layout.addLayout(self.menu_button_layout)
        self.complete_layout.addSpacing(40)
        self.complete_layout.addLayout(self.editrock_layout)
        
        self.setLayout(self.complete_layout)
        
    def insert_wiki_text(self):
        #dialog to prompt which wiki page to use
        if not self.name_edit.toPlainText() == "":
            dialog = QDialog()
            dialog.setWindowTitle("Dialog")
            dialog.setWindowModality(Qt.ApplicationModal)
            
            choose_label = QLabel("Choose a page:")
            select_button = QPushButton("Select")
            
            text_list = QListWidget()
            for each in wikipedia.search(self.name_edit.toPlainText()):
                text_list.addItem(each)
            
            dialog_layout = QVBoxLayout()
            dialog_layout.addWidget(choose_label)
            dialog_layout.addWidget(text_list)
            dialog_layout.addWidget(select_button)
            dialog.setLayout(dialog_layout)
            
            def set_text():
                self.info_edit.setPlainText(wikipedia.summary(text_list.currentItem().text()))
                dialog.close()
            
            select_button.clicked.connect(set_text)
            #select_button.clicked.connect(lambda: self.info_edit.setPlainText(wikipedia.summary(text_list.currentItem().text())))
            
            dialog.exec_()
        
        #self.info_edit.setPlainText(wikipedia.summary(self.name_edit.toPlainText()))
                
