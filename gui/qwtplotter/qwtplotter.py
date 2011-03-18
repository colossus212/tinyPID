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
		
		self.pid = tinyPID(port="/dev/ttyUSB2", baudrate=19200)
		
		
		self.legend = QwtLegend(self.qwtPlot)
		self.legend.setGeometry(QRect(10, 10, 501, 401))
		
		gpen = QPen()
		gpen.setBrush(QColor(150,150,150))
		
		wpen = QPen()
		wpen.setBrush(QColor(0,180,0))
		wpen.setWidth(2)
		
		xpen = QPen()
		xpen.setBrush(QColor(180,0,0))
		xpen.setWidth(2)
		
		ypen = QPen()
		ypen.setBrush(QColor(0,0,180))
		ypen.setWidth(2)
		
		
		self.grid = QwtPlotGrid()
		self.grid.setMajPen(gpen)
		self.grid.attach(self.qwtPlot)
		self.gridEnable(False)
		
		self.curve_w = QwtPlotCurve("Setpoint")
		self.curve_w.attach(self.qwtPlot)
		self.curve_w.setPen(wpen)
		self.curve_w.updateLegend(self.legend)
		
		self.curve_y = QwtPlotCurve("Output")
		self.curve_y.attach(self.qwtPlot)
		self.curve_y.setPen(ypen)
		self.curve_y.updateLegend(self.legend)
		
		self.curve_x = QwtPlotCurve("Process Value")
		self.curve_x.attach(self.qwtPlot)
		self.curve_x.setPen(xpen)
		self.curve_x.updateLegend(self.legend)
		
		self.qwtPlot.setAxisScale(QwtPlot.yLeft, 0, 300)
		self.qwtPlot.setAxisTitle(QwtPlot.yLeft, "")
		self.qwtPlot.setAxisTitle(QwtPlot.xBottom, "t/s")
		self.qwtPlot.replot()
		
		self.t0 = time.time()
		self.t = []
		self.y = []
		self.w = []
		self.x = []
		
		self.view = 10
		self.axmin = 0
		self.axmax = self.view
		self.step = 0
		
		self.timer = QTimer()
		self.timer.setInterval(150)
		self.timer.start()
		
		self.connect(self.timer, SIGNAL("timeout()"), self.genpoint)
		self.genpoint()
		
	def gridEnable(self, enable):
		self.grid.enableX(enable)
		self.grid.enableY(enable)
	
	
	def setView(self, length):
		if length > self.view:
			self.axmax = self.axmin + length
			self.view = length
		elif length < self.view:
			self.axmin = self.t[-2]
			self.axmax = length + self.axmin
			self.view = length
		else:
			return
		
		self.qwtPlot.setAxisScale(QwtPlot.xBottom, self.axmin, self.axmax)


	def setScroll(self, percent):
		self.step = percent/100.


	def setYmin(self, ymin):
		ymax = self.ymaxSpinBox.value()
		self.qwtPlot.setAxisScale(QwtPlot.yLeft, ymin, ymax)


	def setYmax(self, ymax):
		ymin = self.yminSpinBox.value()
		self.qwtPlot.setAxisScale(QwtPlot.yLeft, ymin, ymax)
	
	
	def setAutoscale(self, enable):
		if enable:
			self.qwtPlot.setAxisAutoScale(QwtPlot.yLeft)
		else:
			ymin, ymax = self.yminSpinBox.value(), self.ymaxSpinBox.value()
			self.qwtPlot.setAxisScale(QwtPlot.yLeft, ymin, ymax)
			
		
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
		
		if self.t[-1] > self.axmax and self.step > 0:
			self.axmin = self.axmin + self.view*self.step
			self.axmax = self.axmax + self.view*self.step
			self.qwtPlot.setAxisScale(QwtPlot.xBottom, self.axmin, self.axmax)
			
		print "Points:", len(self.t)+len(self.w,)+len(self.x)+len(self.y)
		print "AxBounds:", self.axmin, self.axmax
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