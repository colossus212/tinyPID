
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from graphtestui import *
import time
import numpy


redpen = QPen()
redpen.setBrush(Qt.red)
redpen.setWidth(2)
redpen.setJoinStyle(Qt.RoundJoin)
redpen.setCapStyle(Qt.RoundCap)

bluepen = QPen()
bluepen.setBrush(Qt.blue)
bluepen.setWidth(2)
bluepen.setJoinStyle(Qt.RoundJoin)
bluepen.setCapStyle(Qt.RoundCap)

greenpen = QPen()
greenpen.setBrush(Qt.green)
greenpen.setWidth(2)
greenpen.setJoinStyle(Qt.RoundJoin)
greenpen.setCapStyle(Qt.RoundCap)

blackpen = QPen()
blackpen.setWidth(3)
blackpen.setBrush(QColor(70,70,70))
blackpen.setJoinStyle(Qt.RoundJoin)
blackpen.setCapStyle(Qt.RoundCap)

thinpen = QPen()
thinpen.setWidth(0)
thinpen.setBrush(QColor(100,100,100))


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
		self.points = [p for p in self.points if p.x() > x]
			
	
	def cropRight(self, x):
		self.points = [p for p in self.points if p.x() < x]
		
	
	def count(self):
		return len(self.points)
	
	
	def length(self):
		return self.path().length()
		


class Plotter (QGraphicsScene):
	
	def __init__(self, update=500, stretch=1, *args, **kwargs):
		super(Plotter, self).__init__(*args, **kwargs)
		
		self.curves = {}
		self.dots = []
		self.stamps = []
		self.ylines = []
		
		self.t = 0
		self.time = 0
		self.t0 = time.time()
		self.stretch = stretch
		
		self.timer = QTimer()
		self.timer.setInterval(update)
		self.timer.start()
		
		self.stamptimer = QTimer()
		self.stamptimer.setInterval(1000)
		self.stamptimer.start()
		self.makeStamp()
		
		self.connect(self.timer, SIGNAL("timeout()"), self.__update)
		self.connect(self.stamptimer, SIGNAL("timeout()"), self.makeStamp)
	 
	 
	def __write(self, curve, y):
		curve.addPoint(QPointF(self.t, y))
		
	
	def __update(self):
		view = self.views()[0]
		corner = view.mapToScene(0,0)
		
		self.time = time.time() - self.t0
		self.t = self.time*self.stretch
				
		view.centerOn(self.t/2, 0)
				
		for curve in self.curves.values():
			if curve.points:
				last = curve.points[-1]
				#self.__write(curve, last.y())
				curve.cropLeft(corner.x())
				print len(curve.points),
				
		for i in range(len(self.dots)):
			if i < len(self.dots):
				if self.dots[i].boundingRect().x() < corner.x():
					self.removeItem(self.dots[i])
					del self.dots[i]
			else:
				break
		
		for i in range(len(self.stamps)):
			if i < len(self.stamps):
				x = self.stamps[i].x()
				w = self.stamps[i].boundingRect().width()
				if corner.x() > 0 and x+w < corner.x():
					self.removeItem(self.stamps[i])
					del self.stamps[i]
			else:
				break
		
		print len(self.dots), len(self.stamps)
		
	
	
	def setCleanupInterval(self, i):
		self.timer.setInterval(i)
	
	def setStampInterval(self, i):
		self.stamptimer.setInterval(i)
	
	def getTime(self):
		return self.time
		
		
	def makeDot(self, y, x=None, w=3, h=3, pen=blackpen):
		x = x or self.t
		d = self.addEllipse(x-w/2., y-h/2., w, h, pen)
		d.setZValue(-1)
		d.setOpacity(.6)
		self.dots.append(d)
		
		
	def makeStamp(self, y=0, x=None, z=0):
		x = x or self.t
		
		t = "%2.1e" % int(self.time)
		s = self.addText(t)
		w = s.boundingRect().width()
		
		s.setPos(x-w/2, y)
		s.adjustSize()
		s.setZValue(z)
		
		if s.isObscured():
			self.removeItem(s)
		else:
			self.stamps.append(s)
	
	
	def addCurve(self, name, pen, startpoint=QPointF(0,0), title=None):
		
		if self.curves.has_key(name):
			raise KeyError("Curve with that name already exists")
			return
			
		curve = Curve(name, pen)
		curve.addPoint(startpoint)
		
		self.addItem(curve)
		self.curves.update({name: curve})
		
	
	def updateCurve(self, name, y, dot=True):
		if self.curves.has_key(name):
			if dot is True:
				self.makeDot(y)
				
			self.__write(self.curves[name], y)
		
		
	

class graphtest (QMainWindow, Ui_Form):
	
	def __init__(self, parent=None):
		super(graphtest, self).__init__(parent)
		self.setupUi(self)
		
		self.scene = Plotter(stretch=10,update=50)
		self.graphicsView.setScene(self.scene)
		self.graphicsView.scale(.9, .9)
		
		self.scene.addCurve("green", greenpen)
		self.scene.addCurve("red", redpen)
		self.scene.setStampInterval(5000)
		
		self.timer = QTimer()
		self.timer.setInterval(500)
		self.timer.start()
		self.timer2 = QTimer()
		self.timer2.setInterval(1000)
		self.timer2.start()
		
		self.connect(self.timer, SIGNAL("timeout()"), self.genpoint)
		self.connect(self.timer2, SIGNAL("timeout()"), self.genpoint2)
		self.genpoint()
		self.genpoint2()
		
	def genpoint(self):
		yg = -(numpy.random.randint(128)+127)
		self.scene.updateCurve("green", yg)
	
	def genpoint2(self):
		yr = -(numpy.random.randint(128)+32)
		self.scene.updateCurve("red", yr, False)
		
		
	
		


if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	d = graphtest()
	d.show()
	app.exec_()