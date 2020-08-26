import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QPushButton
from PyQt5.QtWidgets import QCheckBox, QProgressBar, QLabel, QComboBox, QMessageBox

class Window(QMainWindow):

	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50, 50, 500, 500)
		self.setWindowTitle("Tortoise Finance")
		self.setWindowIcon(QtGui.QIcon('logo.png'))
		
		# main menu
		extractAction = QAction("&GET TO THE CHOPPER", self)
		#extractAction.setShortCut("Ctrl+Q")
		extractAction.setStatusTip('Leave the app')
		extractAction.triggered.connect(self.close_application)
		#self.statusBar()
		
		# to modify create a mainMenu object
		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('&File')
		fileMenu.addAction(extractAction)
		
		self.home()
		
	def home(self):
		btn = QPushButton("Quit", self)
		#btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
		btn.clicked.connect(self.close_application)
		#btn.resize(100, 100)
		btn.resize(btn.sizeHint())
		btn.move(100, 100)
		
		# Toolbar
		extractAction = QAction(QtGui.QIcon('icon.png'), 'Flee the scene', self)
		extractAction.triggered.connect(self.close_application)
		self.toolBar = self.addToolBar("Extraction")
		self.toolBar.addAction(extractAction)
		
		# Checkbox
		checkBox = QCheckBox('Enlarge the window', self)
		checkBox.move(100, 25)
		checkBox.toggle() # automatically checked by default
		checkBox.stateChanged.connect(self.enlarge_window)
		
		# Progress Bar
		self.progress = QProgressBar(self)
		self.progress.setGeometry(200, 80, 250, 20)
		self.btn = QPushButton("Download", self)
		self.btn.move(200, 120)
		self.btn.clicked.connect(self.download)
		
		# drop down button
		print(self.style().objectName())
		self.styleChoice = QLabel("Windows", self)
		
		comboBox = QComboBox(self)
		comboBox.addItem("motif")
		comboBox.addItem("Windows")
		comboBox.addItem("cde")
		comboBox.addItem("Plastique")
		comboBox.addItem("Cleanlooks")
		comboBox.addItem("WindowsVista")
		comboBox.move(50, 250)
		self.styleChoice.move(50, 150)
		#comboBox.activate[str].connect(self.style_choice)
		#comboBox.connect(self.style_choice)
		
		self.show()
	
	def style_choice(self, text):
		self.styleChoice.setText(text)
		QApplication.setStyle(QtGui.QStyleFactory.create(text))
		
	def download(self):
		self.completed = 0
		while (self.completed < 100):
			self.completed += 0.0001
			self.progress.setValue(self.completed)
		
	def enlarge_window(self, state):
		if state == QtCore.Qt.Checked:
			self.setGeometry(50, 50, 1000, 1000)
		else:
			self.setGeometry(50, 50, 500 , 300)
		
	def close_application(self):
		#print("what ever custom")
		#sys.exit()
		# Pop up question
		choice = QMessageBox.question(self, 'Extract!', "Get into the chopper?", QtGui.QtMessageBox.Yes|QtGui.QtMessageBox.No)
		if choice == QMessageBox.Yes:
			print("Extracting now... ")
			sys.exit()
		else:
			pass
def run():
	app = QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())
	
run()