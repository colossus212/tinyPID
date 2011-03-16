
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
		
		
	def addPoint(self, x, y):
		self.points.append(QPointF(x, y))
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
	
	def __init__(self, *args, **kwargs):
		super(Plotter, self).__init__(*args, **kwargs)
		
		self.t = 0
		self.t0 = time.time()
		
		self.timer = QTimer()
		self.timer.setInterval(500)
		self.timer.start()
		
		self.connect(self.timer, SIGNAL("timeout()"), self.addpoint)
		self.connect(self.timer, SIGNAL("timeout()"), self.time)
	
		self.curves = {}
	
	
	def time(self):
		self.t = (time.time() - self.t0) * 50
	
	
	def addpoint(self):
	
		yg = -(numpy.random.randint(128)+127)
		yr = -(numpy.random.randint(128)+32)
		yb = -(numpy.random.randint(128)+16)
		
		self.updateCurve("green", yg)
		self.updateCurve("red", yr)
		self.updateCurve("blue", yb)
	
	
	def addCurve(self, name, pen, title=None):
		
		if self.curves.has_key(name):
			raise KeyError("Curve with that name already exists")
			return
		
		curve = Curve(name, pen)
		self.scene.addItem(curve)
		self.curves.update({name: curve})
		
	
	def updateCurve(self, name, y):
		if self.curves.has_key(name):
			self.curves[name].addPoint(self.t, y)
			self.curves[name].cropLeft(self.graphicsView.mapToScene(0,0).x())
			self.graphicsView.centerOn(self.t, y)
			print name, self.curves[name].count()



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
		
		
	
		


if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	d = graphtest()
	d.addCurve("green", greenpen)
	d.addCurve("blue", bluepen)
	d.addCurve("red", redpen)
	d.show()
	app.exec_()