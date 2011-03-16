
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from graphtestui import *
import time
import numpy

class graphtest (QMainWindow, Ui_Form):
	
	def __init__(self, parent=None):
		super(graphtest, self).__init__(parent)
		self.setupUi(self)
		
		self.timer = QTimer()
		self.timer.setInterval(1000)
		self.timer.start()
		
		self.connect(self.timer, SIGNAL("timeout()"), self.addpoint)
		self.t0 = time.time()
		
		self.scene = QGraphicsScene()
		self.graphicsView.setScene(self.scene)
		self.graphicsView.scale(.9, .9)
		
		
		self.linespen = QPen()
		self.linespen.setWidth(0)
		self.linespen.setBrush(Qt.gray)
		
	
		self.redpen = QPen()
		self.redpen.setBrush(Qt.red)
		self.redpen.setWidth(1)
		self.redpen.setJoinStyle(Qt.RoundJoin)
		self.redpen.setCapStyle(Qt.RoundCap)
		
		self.bluepen = QPen()
		self.bluepen.setBrush(Qt.blue)
		self.bluepen.setWidth(1)
		self.bluepen.setJoinStyle(Qt.RoundJoin)
		self.bluepen.setCapStyle(Qt.RoundCap)
		
		self.greenpen = QPen()
		self.greenpen.setBrush(Qt.green)
		self.greenpen.setWidth(1)
		self.greenpen.setJoinStyle(Qt.RoundJoin)
		self.greenpen.setCapStyle(Qt.RoundCap)
		
	
		greenpath = QPainterPath()
		greenpath.moveTo(0,0)
		redpath = QPainterPath()
		redpath.moveTo(0,0)
		bluepath = QPainterPath()
		bluepath.moveTo(0,0)
		
		self.greenpathitem = self.scene.addPath(greenpath)
		self.greenpathitem.setPath(greenpath)
		self.greenpathitem.setPen(self.greenpen)
		self.greenpathitem.setOpacity(.8)
		
		self.redpathitem = self.scene.addPath(redpath)
		self.redpathitem.setPath(redpath)
		self.redpathitem.setPen(self.redpen)
		self.redpathitem.setOpacity(.8)

		self.bluepathitem = self.scene.addPath(bluepath)
		self.bluepathitem.setPath(bluepath)
		self.bluepathitem.setPen(self.bluepen)
		self.bluepathitem.setOpacity(.8)

	
	
	
	def addpoint(self):
	
		greenpath = self.greenpathitem.path()
		redpath = self.redpathitem.path()
		bluepath = self.bluepathitem.path()
				
		yg = -(numpy.random.randint(128)+127)
		yr = -(numpy.random.randint(128)+32)
		yb = -(numpy.random.randint(128)+16)
		
		x = (time.time() - self.t0)*15
		
		greenpath.lineTo(x,yg)
		bluepath.lineTo(x,yb)
		redpath.lineTo(x,yr)
		
		self.greenpathitem.setPath(greenpath)
		self.bluepathitem.setPath(bluepath)
		self.redpathitem.setPath(redpath)
		
		self.graphicsView.centerOn(x+10, -128)
		if int(x)%100 == 0:
			self.scene.addLine(x,0,x,-255, self.linespen)
	


if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	d = graphtest()
	d.show()
	app.exec_()