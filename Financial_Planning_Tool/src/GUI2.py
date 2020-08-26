from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setGeometry(50, 50, 500, 500)
		self.setWindowTitle("Tortoise Finance")
		self.widgets()
		self.toolbar()
		
	def widgets(self):
		#layout = QHBoxLayout()
		layout = QGridLayout()
		
		label = QLabel("Welcome to Tortoise Financial")
		font = label.font()
		font.setPointSize(30)
		#label.setFont(font)
		label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
		#self.setCentralWidget(label)
		layout.addWidget(label, 0, 0)
		
		currency = QComboBox()
		currency.addItems(["INR", "USD"])
		currency.currentIndexChanged[str].connect(self.set_currency)
		#comboBox.setAlignment(Qt.AlignLeft)
		layout.addWidget(currency, 1, 0)
		
		name = QLineEdit()
		name.setMaxLength(50)
		name.setPlaceholderText("Enter your name")
		name.textChanged.connect(self.set_name)
		name.textEdited.connect(self.set_name)
		name.returnPressed.connect(self.got_name)
		name.selectionChanged.connect(self.got_name)
		layout.addWidget(name, 2, 0)
		
		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)
		
	def toolbar(self):
		toolbar = QToolBar("This is your financial analysis toolbar")
		toolbar.setIconSize(QSize(16, 16))
		self.addToolBar(toolbar)
		
		button = QAction(QIcon("pied_piper.jpg"), "Start", self)
		button.setStatusTip("Start here for financial analysis..")
		button.triggered.connect(self.start_analysis)
		button.setCheckable(True)
		toolbar.addAction(button)
		
		toolbar.addWidget(QLabel("Hello"))
		toolbar.addWidget(QCheckBox())
		
		self.setStatusBar(QStatusBar(self))
		
	def start_analysis(self, s):
		print("Analyzing..", s)
		
	def set_currency(self, s):
		print("Currency set to: %s" % (s))
		
	def set_name(self, s):
		self.name = s
	def got_name(self):
		print("Your name is: ", self.name)
	
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()