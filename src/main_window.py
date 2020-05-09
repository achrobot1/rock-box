import sys
import os

from editrock_widget_class import *
from opening_dialog import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *


from lxml import etree

class MainWindow(QMainWindow):
    """This class creates a main window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rock Box Management")
        self.resize(1400, 800)
        
        if sys.platform == "linux" or sys.platform == "linux2":
            self.home_path = "/home/"
        elif sys.platform == "darwin":
            self.home_path = "/home/"
        elif sys.platform == "win32":
            self.home_path = "C:\\"

        self.load_file()
                 
        self.create_editrock_widgets()
        self.create_main_widget()       
                             
        self.setup_stacked_widget()
        self.stacked_widget.setCurrentWidget(self.main_widget)
                       
        self.central_widget = self.stacked_widget
        #self.central_widget.setLayout(self.stacked_layout)

        self.setCentralWidget(self.central_widget)
    
    #create the main layout; two rows of buttons 1-12    
    def create_main_widget(self):
        #create the 12 pushbuttons
        self.rock_buttons = []
        for each in range(12):
            self.rock_buttons.append(QPushButton(str(each+1)))
            self.rock_buttons[each].setMinimumHeight(55) 
        
        #grid layout
        self.rock_button_grid = QGridLayout()
        for each in range(6):
            self.rock_button_grid.addWidget(self.rock_buttons[each], 0, each)
        for each in range(6):
            self.rock_button_grid.addWidget(self.rock_buttons[each+6], 1, each)
        
        #buttons
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet("QPushButton{ padding: 6px; }")
        
        self.exit_button = QPushButton("Exit")
        self.exit_button.setStyleSheet("QPushButton{ padding: 6px; }")

        #confirmation label
        self.save_confirm_label = QLabel("Save Successful!")
        self.save_confirm_label.setVisible(False)
        
        #icons
        self.exit_icon = QIcon.fromTheme("application-exit")
        self.exit_button.setIcon(self.exit_icon)
        
        self.save_icon = QIcon.fromTheme("document-save")
        self.save_button.setIcon(self.save_icon)

        
        #button layout
        self.icon_layout = QHBoxLayout()
        self.icon_layout.addWidget(self.save_button)
        self.icon_layout.addWidget(self.exit_button)
        self.icon_layout.insertStretch(-1)
        
        #layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.icon_layout)
        self.main_layout.addSpacing(30)
        self.main_layout.addWidget(self.save_confirm_label) 
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.rock_button_grid)
        self.main_layout.addStretch()
           
        self.main_layout.addStretch()
        
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        
        #connections
        self.exit_button.clicked.connect(exit)
        self.save_button.clicked.connect(self.write_xml)

                
        for each in range(12):
            self.rock_buttons[each].released.connect(lambda x=each: self.update_page(self.editrock_widgets[x]))
        
    def create_editrock_widgets(self):
        #create 12 instances of EditRockWidget
        self.editrock_widgets = []
        
        for each in range(12):
            self.editrock_widgets.append(EditRockWidget(each))
        
        
        #read xml file and insert text into textEdits and set date for calendars
        root = etree.parse(self.xml_file).getroot()
        rocks = root.getchildren()

        for each in range(12):
            self.editrock_widgets[each].name_edit.setPlainText(rocks[each][0].text)
            self.editrock_widgets[each].info_edit.setPlainText(rocks[each][2].text)
            self.editrock_widgets[each].source_edit.setPlainText(rocks[each][3].text)
            
            if rocks[each][1][0].text != None and rocks[each][1][1].text !=None and rocks[each][1][2].text != None:
                day = int(rocks[each][1][0].text)
                month = int(rocks[each][1][1].text)
                year = int(rocks[each][1][2].text)
                self.editrock_widgets[each].calendar.setSelectedDate(QDate(year, month, day))
            
        #connections  
        for each in range(12):
            self.editrock_widgets[each].menu_button.clicked.connect(lambda: self.update_page(self.main_widget))
       
        #icon
        self.menu_icon = QIcon.fromTheme("go-home")
       
   
    def setup_stacked_widget(self):
        #create a stacked layout to hold widgets for the main menu and rock edit pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.main_widget)
        
        for each in range(12):
            self.stacked_widget.addWidget(self.editrock_widgets[each])
        
    def update_page(self, widget):
        #display the proper edit rock page when a button is pressed        
        self.stacked_widget.setCurrentWidget(widget)
        
    def write_xml(self):
        root = etree.parse(self.xml_file).getroot()
        rocks = root.getchildren()
        for each in range(12):
            rocks[each][0].text = self.editrock_widgets[each].name_edit.toPlainText()
            rocks[each][2].text = self.editrock_widgets[each].info_edit.toPlainText()
            rocks[each][3].text = self.editrock_widgets[each].source_edit.toPlainText()
            
            rocks[each][1][0].text = str(self.editrock_widgets[each].calendar.selectedDate().day())
            rocks[each][1][1].text = str(self.editrock_widgets[each].calendar.selectedDate().month())
            rocks[each][1][2].text = str(self.editrock_widgets[each].calendar.selectedDate().year())   
        
        f = open(self.xml_file, 'w')
        f.write(etree.tounicode(root, pretty_print=True))
        f.close()
        
        self.save_confirm_label.setVisible(True)
        
    def load_file(self):
        #Prompt user for USB drive directory
        self.dir_path = QFileDialog.getExistingDirectory(self,"Choose folder", self.home_path) 
        
        #Prompt user to load or create new file
        self.d = OpeningDialog()
        for File in os.listdir(self.dir_path):
            if File.endswith('.xml'):
                self.d.text_list.addItem(str(File))
        #connections
        self.d.new_file_button.clicked.connect(self.new_file)
        self.d.select_button.clicked.connect(self.get_file)
        self.d.exec_()
        
    def get_file(self):
        self.xml_file = self.dir_path + '/' + self.d.text_list.currentItem().text()
        self.d.close()
                
    def new_file(self):
        f, ok = QInputDialog.getText(self, 'File Name', 'Enter File Name')
        f = str(f) + '.xml'
        self.xml_file = self.dir_path + '/' + f
        create_xml(self.xml_file)
        self.d.close()

        
def create_xml(fp):
    root = etree.Element("root")
    rock_tags = []
    for each in range(12):
        rock_tags.append(etree.SubElement(root, "Rock", id=str(each)))
    for rock_tag in rock_tags:
        rock_tag.append(etree.Element("Name"))
        rock_tag.append(etree.Element("Date"))
        rock_tag.append(etree.Element("Info"))
        rock_tag.append(etree.Element("Source"))
        
        rock_tag[1].append(etree.Element("Day"))
        rock_tag[1].append(etree.Element("Month"))
        rock_tag[1].append(etree.Element("Year"))
        
    f = open(fp, 'w')
    f.write(etree.tounicode(root, pretty_print=True))
    f.close()
             
def main():
    rock_application = QApplication(sys.argv)
    rock_application.setStyle('plastique')
    style_sheet = open('../style_sheets/turkoi_sheet.qss').read()
    rock_application.setStyleSheet(style_sheet)
    #rock_application.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    main_window = MainWindow() #create new instance of main window
    main_window.show()
    main_window.raise_() # raise instance to top of window stack
    rock_application.exec_() #monitor application for events
    
if __name__ == "__main__":
    main()
    

