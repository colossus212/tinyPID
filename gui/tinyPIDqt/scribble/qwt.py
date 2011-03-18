from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qwt5 import *

from qwtui import *
import time
import numpy
from tinyPID import *
	

class qwttest (QMainWindow, Ui_Form):
	
	def __init__(self, parent=None):
		super(qwttest, self).__init__(parent)
		self.setupUi(self)
		
		self.pid = tinyPID(port="/dev/ttyUSB1", baudrate=19200)
		
		
		self.legend = QwtLegend(self.qwtPlot)
		self.legend.setGeometry(self.qwtPlot.geometry())#QRect(10, 10, 501, 401))
		
		self.curve_w = QwtPlotCurve("Setpoint")
		self.curve_w.attach(self.qwtPlot)
		self.curve_w.setPen(Qt.green)
		self.curve_w.updateLegend(self.legend)
		
		self.curve_y = QwtPlotCurve("Output")
		self.curve_y.attach(self.qwtPlot)
		self.curve_y.setPen(Qt.blue)
		self.curve_y.updateLegend(self.legend)
		
		self.curve_x = QwtPlotCurve("Process Value")
		self.curve_x.attach(self.qwtPlot)
		self.curve_x.setPen(Qt.red)
		self.curve_x.updateLegend(self.legend)
		
		self.qwtPlot.setAxisTitle(QwtPlot.yLeft, "")
		self.qwtPlot.setAxisTitle(QwtPlot.xBottom, "t/s")
		self.qwtPlot.setAxisScale(QwtPlot.yLeft, 0, 255)
		self.qwtPlot.replot()
		
		self.t0 = time.time()
		self.t = []
		self.y = []
		self.w = []
		self.x = []
		self.hist = 5
		
		self.axmin = 0
		self.axmax = self.hist
		self.step = 0.3
		
		self.timer = QTimer()
		self.timer.setInterval(50)
		self.timer.start()
		#self.timer2 = QTimer()
		#self.timer2.setInterval(1000)
		#self.timer2.start()
		
		self.connect(self.timer, SIGNAL("timeout()"), self.genpoint)
		#self.connect(self.timer2, SIGNAL("timeout()"), self.genpoint2)
		self.genpoint()
		#self.genpoint2()
		
	def genpoint(self):
		self.t.append(time.time()-self.t0)
		self.x.append(self.pid.x)
		self.y.append(self.pid.y)
		self.w.append(self.pid.w)
		
		self.curve_w.setData(self.t, self.w)
		self.curve_y.setData(self.t, self.y)
		self.curve_x.setData(self.t, self.x)
		
		for i in range(len(self.t)):
			if self.t[i] < self.axmin:
				del self.t[i]
				del self.x[i]
				del self.w[i]
				del self.y[i]
			else:
				break
		
		if self.t[-1] > self.axmax:
			self.axmin = self.axmin + self.hist*self.step
			self.axmax = self.axmax + self.hist*self.step
			self.qwtPlot.setAxisScale(QwtPlot.xBottom, self.axmin, self.axmax)
			
		print "Points:", len(self.t), len(self.w,), len(self.x), len(self.y)
		self.qwtPlot.replot()
	
	def genpoint2(self):
		#self.y.append(numpy.random.randint(3))
		#self.t.append(time.time()-self.t0)
		
		#self.curve_y.setData(self.t, self.y)
		#self.qwtPlot.replot()
		pass
		
		
		
	
		


if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	d = qwttest()
	d.show()
	app.exec_()