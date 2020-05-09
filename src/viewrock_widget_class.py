from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ViewRockWidget(QWidget):

    def __init__(self):
        super().__init__()
        
        #data
        self.name = ''
        self.info = ''
        self.source = ''
        self.date = ''
        
        #labels
        self.name_label = QLabel(self.name)
        self.info_label = QLabel(self.info)
        self.source_label = QLabel(self.source)
        self.date_label = QLabel(self.date)
        
        self.name_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)
        
        #label stylesheet adjustments
        self.name_label.setStyleSheet("QLabel { font: 40px bold; color: gray; }")
        self.info_label.setStyleSheet("QLabel { color: gray; }")
        self.source_label.setStyleSheet("QLabel { color: gray; }")
        self.date_label.setStyleSheet("QLabel { color: gray; }")
        
        #menu button
        self.menu_button = QPushButton("Main\n Menu", self)
        self.menu_button.setMaximumSize(70, 50)
        
        #layout
        self.main_layout = QGridLayout()
        
        self.main_layout.addWidget(QLabel('Info: '), 1, 0)
        self.main_layout.addWidget(QLabel('Source: '), 2, 0)
        self.main_layout.addWidget(QLabel('Date: '), 3, 0)
        self.main_layout.addWidget(self.menu_button, 4, 0)
        
        self.main_layout.addWidget(self.name_label, 0, 1)
        self.main_layout.addWidget(self.info_label, 1, 1)
        self.main_layout.addWidget(self.source_label, 2, 1)
        self.main_layout.addWidget(self.date_label, 3, 1)
        
        
        '''
        self.left_column = QVBoxLayout()
        self.left_column.addSpacing(80)
        self.left_column.addWidget(QLabel('Info: '))
        self.left_column.addWidget(QLabel('Source: '))
        self.left_column.addWidget(QLabel('Date added \nto collection: '))
        #self.left_column.addWidget(self.menu_button)
        
        self.right_column = QVBoxLayout()
        self.right_column.addWidget(self.name_label)
        self.right_column.addWidget(self.info_label)
        self.right_column.addWidget(self.source_label)
        self.right_column.addWidget(self.date_label)
        
        self.main_layout = QGridLayout()
        self.main_layout.addLayout(self.left_column, 0, 0)
        self.main_layout.addLayout(self.right_column, 0, 1)
        self.main_layout.addWidget(self.menu_button, 1, 0)
       '''
        self.setLayout(self.main_layout)
        
    def set_data(self, name, info, source, date):
        self.name = name
        self.info = info
        self.source = source
        self.date = date
