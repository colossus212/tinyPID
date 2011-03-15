from PyQt4.QtCore import *
from PyQt4.QtGui import *
from tinyPID import *
from tinypidqtui import *
import time, json, os.path

class tinyPIDqt (QMainWindow, Ui_MainWindow):
	
	def __init__(self, parent=None):
		super(tinyPIDqt, self).__init__(parent)
		self.setupUi(self)
		
		self.pid = None
		self.newparameters = False
		self.lastsetpoint = None
		self.lastoutput = None
		self.settings = QSettings("moware", "tinyPIDqt")
		
		
		### Timers 
		self.sendtimer    = QTimer()
		self.sendtimer.setInterval(1000)
		self.updatetimer = QTimer()
		self.updatetimer.setInterval(self.settings.value("com/Update", 1).toDouble()[0]*1000)
		
		
		### Qt Signals
		self.connect(self.sendtimer, SIGNAL("timeout()"), self.sendValues)
		self.connect(self.updatetimer, SIGNAL("timeout()"), self.update)

		self.connect(self.updateDoubleSpinBox, SIGNAL("valueChanged(double)"), \
			lambda x: self.updatetimer.setInterval(x*1000))

		self.connect(self, SIGNAL("connected(bool)"), lambda x: x and self.updatetimer.start())
		self.connect(self, SIGNAL("connected(bool)"), lambda x: x  or self.updatetimer.stop())
		self.connect(self, SIGNAL("connected(bool)"), lambda x: x and self.sendtimer.start())
		self.connect(self, SIGNAL("connected(bool)"), lambda x: x  or self.sendtimer.stop())
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

		self.connect(self.fileButton, SIGNAL("clicked()"), self.saveParametersToFile)
		self.connect(self.loadButton, SIGNAL("clicked()"), self.loadParametersFromFile)
		
		### Restore settings and populate widgets
		self.restoreGeometry(self.settings.value("ui/Geometry").toByteArray())
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
		"""
		Qt signals to connect only when there's communication with the controller.
		"""
		
		self.connect(self.eepromButton, SIGNAL("clicked()"), self.saveEEPROM)
		self.connect(self.autoRadioButton, SIGNAL("toggled(bool)"), lambda x: x and self.pid.auto())
		self.connect(self.manRadioButton, SIGNAL("toggled(bool)"), lambda x: x and self.pid.manual())
		
		
	def connectPID(self):
		"""
		Setup communication with the controller.
		"""
		
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
			self.pid.com.readlines()
			w = self.pid.w
			x = self.pid.x
			y = self.pid.y
			m = self.pid.opmode
			self.initValues(w, x, y, m)
			
			# loaded parameters before, now set them
			if self.newparameters == True:
				self.setScales()
				self.setParameters()
				self.newparameters = False
	
	
	def initValues(self, w=0, x=0, y=0, m='m'):
		"""
		Initialize widgets with some values.
		"""
		
		self.lastsetpoint = w
		self.lastoutput = y
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
		""" 
		Updates mode, process value etc. with data from device.
		Called by self.updatetimer.
		"""
		
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

	
	def sendValues(self):
		""" 
		Send output or setpoint to device, if changed. 
		Called by self.sendtimer every second.
		"""
		
		if self.pid is None:
			return
			
		if self.autoRadioButton.isChecked():
			if self.setpoint.value() != self.lastsetpoint:
				self.pid.w = self.setpoint.value()
				self.lastsetpoint = self.pid.w
				print "Set setpoint to", self.lastsetpoint
		else:
			if self.output.value() != self.lastoutput:
				self.pid.y = self.output.value()
				self.lastoutput = self.pid.y
				print "Set output to", self.lastoutput
				
	
	def dialSetpoint(self):
		"""
		Setup the Dial to set the setpoint. Change label and signals accordingly.
		"""
		
		self.dialLabel.setText("setpoint")
		self.disconnect(self.dial, SIGNAL("valueChanged(int)"), self.output.setValue)
		self.disconnect(self.output, SIGNAL("valueChanged(int)"), self.dial.setValue)
		self.connect(self.dial, SIGNAL("valueChanged(int)"), self.setpoint.setValue)
		self.connect(self.setpoint, SIGNAL("valueChanged(int)"), self.dial.setValue)
	
	
	def dialOutput(self):
		"""
		Setup the Dial to set the output. Change label and signals accordingly.
		"""
		
		self.dialLabel.setText("output")
		self.disconnect(self.dial, SIGNAL("valueChanged(int)"), self.setpoint.setValue)
		self.disconnect(self.setpoint, SIGNAL("valueChanged(int)"), self.dial.setValue)
		self.connect(self.dial, SIGNAL("valueChanged(int)"), self.output.setValue)
		self.connect(self.output, SIGNAL("valueChanged(int)"), self.dial.setValue)
		
		
	def resetParameters(self):
		"""
		Reset the display of controller parameters to those on the device.
		"""
		
		if self.pid is None:
			return
			
		self.kpDoubleSpinBox.setValue(self.pid.Kp)
		self.kiDoubleSpinBox.setValue(self.pid.Ki)
		self.kdDoubleSpinBox.setValue(self.pid.Kd)
	
	
	def setParameters(self):
		"""
		Set new controller parameters.
		"""
		
		if self.pid is None:
			return
			
		self.pid.set_Kp(self.kpDoubleSpinBox.value())
		self.pid.set_Ki(self.kiDoubleSpinBox.value())
		self.pid.set_Kd(self.kdDoubleSpinBox.value())
		self.resetParameters()
	
	
	def resetScales(self):
		"""
		Reset display of PV scale and output limits to those on the device.
		"""
		
		if self.pid is None:
			return
			
		xmin, xmax = self.pid.get_scale()
		ymin, ymax = self.pid.get_limits()
		self.xminSpinBox.setValue(xmin)
		self.xmaxSpinBox.setValue(xmax)
		self.yminSpinBox.setValue(ymin)
		self.ymaxSpinBox.setValue(ymax)
	
	
	def setScales(self):
		"""
		Set new PV scale and output limits.
		"""
		
		if self.pid is None:
			return
			
		self.pid.set_scale(self.xminSpinBox.value(), self.xmaxSpinBox.value())
		self.pid.set_limits(self.yminSpinBox.value(), self.ymaxSpinBox.value())
	
	
	def saveEEPROM(self):
		"""
		Call the device's save-to-eeprom command.
		"""
		if self.pid is None:
			return
			
		self.pid.save()
		self.fileLabel.setText("EEPROM")
	
	
	def saveParametersToFile(self):
		"""
		Save controller parameters to a file.
		"""
		dn = self.settings.value("ui/Last Directory", os.path.expanduser("~")).toString()
		fn = QFileDialog.getSaveFileName(self, "Speichern", dn)
		if not fn:
			return
			
		fp = open(str(fn),'w')
		
		par = {
			"Kp": self.kpDoubleSpinBox.value(),
			"Ki": self.kiDoubleSpinBox.value(),
			"Kd": self.kdDoubleSpinBox.value(),
			"Out": self.output.value(),
			"SP": self.setpoint.value(),
			"xmin": self.xminSpinBox.value(),
			"xmax": self.xmaxSpinBox.value(),
			"ymin": self.yminSpinBox.value(),
			"ymax": self.ymaxSpinBox.value(),
			"mode": self.autoRadioButton.isChecked() and "a" or "m",
			"com": {
				"port": str(self.portLineEdit.text()),
				"speed": self.speedLineEdit.text().toInt()[0],
				"update": self.updateDoubleSpinBox.value()
				}
			}
		
		json.dump(par, fp)
		fp.close()
		self.fileLabel.setText(os.path.basename(str(fn)))
		if os.path.dirname(str(fn)) != dn:
			self.settings.setValue("ui/Last Directory", os.path.basename(str(fn)))
	
	
	def loadParametersFromFile(self):
		"""
		Load controller parameters from a file.
		"""
		dn = self.settings.value("ui/Last Directory", os.path.expanduser("~")).toString()
		fn = QFileDialog.getOpenFileName(self, "Laden", dn)
		if not fn:
			return
		
		fp = open(str(fn), 'r')
		par = json.load(fp)
		com = par['com']
		
		print par
		
		fp.close()

		self.fileLabel.setText(os.path.basename(str(fn)))
		if os.path.dirname(str(fn)) != dn:
			self.settings.setValue("ui/Last Directory", os.path.basename(str(fn)))
		
		self.portLineEdit.setText(com['port'])
		self.speedLineEdit.setText(str(com['speed']))
		self.updateDoubleSpinBox.setValue(com['update'])
		
		self.setpoint.setValue(par['SP'])
		self.kpDoubleSpinBox.setValue(par['Kp'])
		self.kiDoubleSpinBox.setValue(par['Ki'])
		self.kdDoubleSpinBox.setValue(par['Kd'])
		
		self.xminSpinBox.setValue(par['xmin'])
		self.xmaxSpinBox.setValue(par['xmax'])
		self.yminSpinBox.setValue(par['ymin'])
		self.ymaxSpinBox.setValue(par['ymax'])
		
		if par['mode'] == 'a':
			self.autoRadioButton.toggle()
		else:
			self.manRadioButton.toggle()
			self.output.setValue(par['Out'])
		
		self.newparameters = True
		
		self.setScales()
		self.setParameters()
		
	
	
	def closeEvent(self, event):
		"""
		Before closing the main window, save some settings and last controller
		values.
		"""
		
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
