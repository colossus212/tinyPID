from PyQt4.QtCore import *
from PyQt4.QtGui import *
from tinyPID import *
from tinypidqtui import *
import time

class tinyPIDqt (QMainWindow, Ui_MainWindow):
	
	def __init__(self, parent=None):
		super(tinyPIDqt, self).__init__(parent)
		self.setupUi(self)
		
		self.settings = QSettings("moware", "tinyPIDqt")
		self.restoreGeometry(self.settings.value("ui/Geometry").toByteArray())
				
		self.timer = QTimer()
		self.timer.setInterval(self.settings.value("com/Update", 1).toDouble()[0]*1000)
		
		self.pid = None
		
		self.connect(self.timer, SIGNAL("timeout()"), self.update)

		self.connect(self.updateDoubleSpinBox, SIGNAL("valueChanged(double)"), \
			lambda x: self.timer.setInterval(x*1000))

		self.connect(self, SIGNAL("connected(bool)"), lambda x: x and self.timer.start())
		self.connect(self, SIGNAL("connected(bool)"), lambda x: x or self.timer.stop())
		self.connect(self, SIGNAL("connected(bool)"), lambda x: x and self.connectPidSignals())
		self.connect(self, SIGNAL("connected(bool)"), lambda x: x and self.resetParameters())	
		self.connect(self, SIGNAL("connected(bool)"), lambda x: x and self.resetScales())	
	
		self.connect(self.connectButton, SIGNAL("clicked()"), self.connectPID)
			
		self.connect(self.kpDoubleSpinBox, SIGNAL("valueChanged(double)"), \
			lambda x: self.tvDoubleSpinBox.setValue(Kd_to_Tv(self.kpDoubleSpinBox.value(), self.kdDoubleSpinBox.value())))
		self.connect(self.kpDoubleSpinBox, SIGNAL("valueChanged(double)"), \
			lambda x: self.tnDoubleSpinBox.setValue(Ki_to_Tn(self.kpDoubleSpinBox.value(), self.kiDoubleSpinBox.value())))
		self.connect(self.kdDoubleSpinBox, SIGNAL("valueChanged(double)"), \
			lambda x: self.tvDoubleSpinBox.setValue(Kd_to_Tv(self.kpDoubleSpinBox.value(), self.kdDoubleSpinBox.value())))
		self.connect(self.kiDoubleSpinBox, SIGNAL("valueChanged(double)"), \
			lambda x: self.tnDoubleSpinBox.setValue(Ki_to_Tn(self.kpDoubleSpinBox.value(), self.kiDoubleSpinBox.value())))
		   		
		self.connect(self.ScaleButtonBox, SIGNAL("accepted()"), lambda: self.setScales())
		self.connect(self.ParameterButtonBox, SIGNAL("accepted()"), lambda: self.setParameters())
		self.connect(self.ScaleButtonBox, SIGNAL("clicked(QAbstractButton*)"), \
			lambda x: x.text() == "Reset" and self.resetScales())
		self.connect(self.ParameterButtonBox, SIGNAL("clicked(QAbstractButton*)"), \
			lambda x: x.text() == "Reset" and self.resetParameters())
		
		
		self.connect(self.autoRadioButton, SIGNAL("toggled(bool)"), lambda x: x and self.dialSetpoint())
		self.connect(self.manRadioButton, SIGNAL("toggled(bool)"), lambda x: x and self.dialOutput())


		self.toolBox.setCurrentIndex(self.settings.value("ui/Toolbox", 0).toInt()[0])
		self.portLineEdit.setText(self.settings.value("com/Port", "/dev/ttyUSB0").toString())
		self.speedLineEdit.setText(self.settings.value("com/Baud", 19200).toString())
		self.updateDoubleSpinBox.setValue(self.settings.value("com/Update", 1).toDouble()[0])
		
		w = self.settings.value("pid/SP", 0).toInt()[0]
		x = self.settings.value("pid/PV", 0).toInt()[0]
		y = self.settings.value("pid/Output", 0).toInt()[0]
		m = self.settings.value("pid/Opmode", 'm').toString()
		self.initValues(w, x, y, m)
		
		if self.settings.value("com/Auto", False).toBool():
			self.connectCheckBox.toggle()
			self.connectPID()
	
	
	def connectPidSignals(self):
		self.connect(self.eepromButton, SIGNAL("toggled(bool)"), lambda x: x and self.pid.save())
		self.connect(self.autoRadioButton, SIGNAL("toggled(bool)"), lambda x: x and self.pid.auto())
		self.connect(self.manRadioButton, SIGNAL("toggled(bool)"), lambda x: x and self.pid.manual())
		
		self.connect(self.setpoint, SIGNAL("valueChanged(int)"), self.updateSP)

		
	def connectPID(self):
		try:
			if self.sender() == self.connectButton:
				port = self.portLineEdit.text()
				baud = self.speedLineEdit.text().toInt()[0]
			else:
				port = self.settings.value("com/Port", "/dev/ttyUSB0").toString()
				baud = self.settings.value("com/Baud", 19200).toInt()[0]
			
			self.pid = tinyPID(port=str(port), baudrate=baud)
			
		except:
			self.pid = None
			self.connectionLabel.setText("not connected.")
			self.emit(SIGNAL("connected(bool)"), False)
		else:
			self.emit(SIGNAL("connected(bool)"), True)
			self.connectionLabel.setText("connected.")
			w = self.pid.w
			x = self.pid.x
			y = self.pid.y
			m = self.pid.opmode
			self.initValues(w, x, y, m)
	
	
	def initValues(self, w=0, x=0, y=0, m='m'):
		
		self.setpoint.setValue(w)
		self.setpointLabel.setText(str(self.setpoint.value()))
		self.output.setValue(y)
		self.outputLabel.setText(str(self.output.value()))
		self.pvLabel.setText(str(x))
		self.errorLabel.setText(str(w-x))
		
		self.resetScales()
		self.resetParameters()
		
		if m == 'a':
			self.autoRadioButton.toggle()
			self.dial.setValue(self.setpoint.value())
		else:
			self.manRadioButton.toggle()
			self.dial.setValue(self.output.value())
		
		
	def update(self):
		if self.pid is None:
			return
			
		opmode = self.pid.opmode
		
		self.pvLabel.setText(str(self.pid.x))
		self.errorLabel.setText(str(self.pid.e))
		
		if opmode == 'a':
			self.autoRadioButton.toggle()
			self.output.setValue(self.pid.y)
		elif opmode == 'm':
			self.manRadioButton.toggle()
			self.pid.y = self.output.value()

	
	def updateSP(self, w):
		if self.pid is None:
			return
		
		self.pid.w = self.setpoint.value()
	
	
	def dialSetpoint(self):
		self.dialLabel.setText("setpoint")
		self.disconnect(self.dial, SIGNAL("valueChanged(int)"), self.output.setValue)
		self.disconnect(self.output, SIGNAL("valueChanged(int)"), self.dial.setValue)
		self.connect(self.dial, SIGNAL("valueChanged(int)"), self.setpoint.setValue)
		self.connect(self.setpoint, SIGNAL("valueChanged(int)"), self.dial.setValue)
	
	
	def dialOutput(self):
		self.dialLabel.setText("output")
		self.disconnect(self.dial, SIGNAL("valueChanged(int)"), self.setpoint.setValue)
		self.disconnect(self.setpoint, SIGNAL("valueChanged(int)"), self.dial.setValue)
		self.connect(self.dial, SIGNAL("valueChanged(int)"), self.output.setValue)
		self.connect(self.output, SIGNAL("valueChanged(int)"), self.dial.setValue)
		
		
	def resetParameters(self):
		if self.pid is None:
			return
			
		self.kpDoubleSpinBox.setValue(self.pid.Kp)
		self.kiDoubleSpinBox.setValue(self.pid.Ki)
		self.kdDoubleSpinBox.setValue(self.pid.Kd)
	
	
	def setParameters(self):
		if self.pid is None:
			return
			
		self.pid.set_Kp(self.kpDoubleSpinBox.value())
		self.pid.set_Ki(self.kiDoubleSpinBox.value())
		self.pid.set_Kd(self.kdDoubleSpinBox.value())
		self.resetParameters()
	
	
	def resetScales(self):
		if self.pid is None:
			return
			
		xmin, xmax = self.pid.get_scale()
		ymin, ymax = self.pid.get_limits()
		self.xminSpinBox.setValue(xmin)
		self.xmaxSpinBox.setValue(xmax)
		self.yminSpinBox.setValue(ymin)
		self.ymaxSpinBox.setValue(ymax)
	
	
	def setScales(self):
		if self.pid is None:
			return
			
		self.pid.set_scale(self.xminSpinBox.value(), self.xmaxSpinBox.value())
		self.pid.set_limits(self.yminSpinBox.value(), self.ymaxSpinBox.value())
	
	
	def closeEvent(self, event):
		self.settings.setValue("com/Port", self.portLineEdit.text())
		self.settings.setValue("com/Baud", self.speedLineEdit.text().toInt()[0])
		self.settings.setValue("com/Auto", self.connectCheckBox.isChecked())
		self.settings.setValue("com/Update", self.updateDoubleSpinBox.value())
		
		self.settings.setValue("pid/SP", self.setpoint.value())
		self.settings.setValue("pid/PV", self.pvLabel.text().toInt()[0])
		self.settings.setValue("pid/Output", self.output.value())
		if self.autoRadioButton.isChecked():
			self.settings.setValue("pid/Opmode", "a")
		else:
			self.settings.setValue("pid/Opmode", "m")
			
		self.settings.setValue("ui/Toolbox", self.toolBox.currentIndex())
		self.settings.setValue("ui/Geometry", self.saveGeometry())
			


if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	d = tinyPIDqt()
	d.show()
	app.exec_()
