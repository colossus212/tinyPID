from PyQt4.QtCore import *
from PyQt4.QtGui import *
from tinyPID import *
from mainwindow import *
import time

class tinyPIDqt (QMainWindow, Ui_MainWindow):
	
	def __init__(self, parent=None, timeout=1):
		super(tinyPIDqt, self).__init__(parent)
		self.setupUi(self)
		
		self.timer = QTimer()
		self.timer.setInterval(timeout*1000)
		self.connect(self.timer, SIGNAL("timeout()"), self.update)
		self.timer.start()
	
		self.pid = tinyPID(port="/dev/ttyUSB0",baudrate=19200)
		self.setvalueSpinBox.setValue(self.pid.w)
		self.outputvalueSpinBox.setValue(self.pid.y)
		if self.pid.opmode == 'a':
			self.autoRadioButton.toggle()
		else:
			self.manualRadioButton.toggle()
			
		self.connect(self.setvalueSpinBox, SIGNAL("valueChanged(int)"), self.updateSP)
		self.connect(self.autoRadioButton, SIGNAL("toggled(bool)"), lambda x: x and self.pid.auto())
		self.connect(self.manualRadioButton, SIGNAL("toggled(bool)"), lambda x: x and self.pid.manual())
		

	def update(self):
		opmode = self.pid.opmode
		
		self.processvalueSpinBox.setValue(self.pid.x)
		
		if opmode == 'a':
			self.autoRadioButton.toggle()
			self.outputvalueSpinBox.setValue(self.pid.y)
		elif opmode == 'm':
			self.manualRadioButton.toggle()
			self.pid.y = self.outputvalueSpinBox.value()

	
	def updateSP(self, w):
		self.pid.w = self.setvalueSpinBox.value()
	

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	d = tinyPIDqt()
	d.show()
	app.exec_()