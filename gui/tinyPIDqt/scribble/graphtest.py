
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from graphtestui import *
import time
import numpy


redpen = QPen()
redpen.setBrush(Qt.red)
redpen.setWidth(1)
redpen.setJoinStyle(Qt.RoundJoin)
redpen.setCapStyle(Qt.RoundCap)

bluepen = QPen()
bluepen.setBrush(Qt.blue)
bluepen.setWidth(1)
bluepen.setJoinStyle(Qt.RoundJoin)
bluepen.setCapStyle(Qt.RoundCap)

greenpen = QPen()
greenpen.setBrush(Qt.green)
greenpen.setWidth(1)
greenpen.setJoinStyle(Qt.RoundJoin)
greenpen.setCapStyle(Qt.RoundCap)

blackpen = QPen()
blackpen.setWidth(3)
blackpen.setBrush(Qt.black)
blackpen.setJoinStyle(Qt.RoundJoin)
blackpen.setCapStyle(Qt.RoundCap)


class Dot (QGraphicsEllipseItem):
	
	def __init__(self, x, y, w=2, h=2, *args, **kwargs):
		super(Dot, self).__init__(*args, **kwargs)
		
		
		b = QGraphicsBlurEffect()
		b.setBlurRadius(1)
		self.setGraphicsEffect(b)
	
	def center(self):
		x, y = self.x(), self.y()
		r = self.boundingRect()
		w, h = r.width(), r.height()
		self.setPos(x-w/2., y-w/2.)


class Curve (QGraphicsPathItem):
	
	def __init__(self, name, pen, *args, **kwargs):
		super(Curve, self).__init__(QPainterPath(), *args, **kwargs)
				
		self.name = name
		self.points = []
	
		self.setPen(pen)
		self.setOpacity(.8)
		
		self.drawPath()
	
	def drawPath(self):
		
		path = QPainterPath()
		for p in self.points:
			path.lineTo(p)
		
		self.setPath(path)
		
		
	def addPoint(self, p):
		self.points.append(p)
		self.drawPath()
	
	
	def cropLeft(self, x):
		if self.points[0].x() < x:
			self.points = self.points[1:]
	
	
	def cropRight(self, x):
		if self.points[0].x() > x:
			self.points = self.points[1:]
		
	
	def count(self):
		return len(self.points)
	
	
	def length(self):
		return self.path().length()
		


class Plotter (QGraphicsScene):
	
	def __init__(self, update=250, *args, **kwargs):
		super(Plotter, self).__init__(*args, **kwargs)
		
		self.t = 0
		self.t0 = time.time()
		
		self.timer = QTimer()
		self.timer.setInterval(update)
		self.timer.start()
		
		self.connect(self.timer, SIGNAL("timeout()"), self.__feed)
		self.connect(self.timer, SIGNAL("timeout()"), self.time)
	
		self.curves = {}
		self.point = (2,2,blackpen)
		
		
	def __write(self, curve, y):
		curve.addPoint(QPointF(self.t, y))
		curve.cropLeft(self.views()[0].mapToScene(0,0).x())
		self.views()[0].centerOn(self.t, y)
		
	
	def __feed(self):
		for v in self.curves.values():
			if v.points:
				last = v.points[-1].y()
				self.__write(v, last)
	
	
	def setInterval(self, i):
		self.timer.setInterval(i)
	
	
	def time(self):
		self.t = (time.time() - self.t0)*10
		return self.t
	
	
	def addCurve(self, name, pen, startpoint=QPointF(0,0), title=None):
		
		if self.curves.has_key(name):
			raise KeyError("Curve with that name already exists")
			return
			
		curve = Curve(name, pen)
		curve.addPoint(startpoint)
		
		self.addItem(curve)
		self.curves.update({name: curve})
		
	
	def updateCurve(self, name, y, point=True):
		if self.curves.has_key(name):
			if point is True:
				self.makeDot(self.t, y)
				
			self.__write(self.curves[name], y)
	
	def makeDot(self, x, y, w=2, h=2, pen=blackpen):
		e = self.addEllipse(x-w/2., y-h/2., w, h, pen)
		e.setZValue(-1)
		e.setOpacity(.2)
			

				



class graphtest (QMainWindow, Ui_Form):
	
	def __init__(self, parent=None):
		super(graphtest, self).__init__(parent)
		self.setupUi(self)
		
		self.scene = Plotter()
		self.graphicsView.setScene(self.scene)
		self.graphicsView.scale(.9, .9)
		
		self.linespen = QPen()
		self.linespen.setWidth(0)
		self.linespen.setBrush(Qt.gray)
		
		self.scene.addCurve("green", greenpen)
		self.scene.addCurve("blue", bluepen)
		self.scene.addCurve("red", redpen)
		
		self.timer = QTimer()
		self.timer.setInterval(1000)
		self.timer.start()
		self.timer2 = QTimer()
		self.timer2.setInterval(500)
		self.timer2.start()
		
		self.connect(self.timer, SIGNAL("timeout()"), self.genpoint)
		self.connect(self.timer2, SIGNAL("timeout()"), self.genpoint2)
		self.genpoint()
		self.genpoint2()
		
	def genpoint(self):

		yg = -(numpy.random.randint(128)+127)
		
		#yb = -(numpy.random.randint(128)+16)
		#yg = -128
		self.scene.updateCurve("green", yg)
	
	def genpoint2(self):
		#yr = -64
		yr = -(numpy.random.randint(128)+32)
		self.scene.updateCurve("red", yr)
		#self.scene.updateCurve("blue", yb)
		
		
	
		


if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	d = graphtest()
	d.show()
	app.exec_()