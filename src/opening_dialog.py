from PyQt4.QtCore import *
from PyQt4.QtGui import *


class OpeningDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setMinimumSize(300, 200)
        
        #buttons
        self.new_file_button = QPushButton("New File")
        self.select_button = QPushButton("Select File")
        
        #labels
        self.choose_label = QLabel('Choose a file: ')
        
        #text list
        self.text_list = QListWidget()
            
        
        #layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.choose_label)
        self.layout.addWidget(self.text_list)
        self.layout.addWidget(self.select_button)
        self.layout.addWidget(self.new_file_button)
        
        self.setLayout(self.layout)	
	    
	    
