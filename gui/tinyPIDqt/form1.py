# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form1.ui'
#
# Created: Mon Mar 14 16:44:00 2011
#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(562, 591)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(562, 591))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 290, 561, 271))
        self.graphicsView.setObjectName("graphicsView")
        self.radioButton = QtGui.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(40, 50, 71, 21))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtGui.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(40, 90, 61, 21))
        self.radioButton_2.setObjectName("radioButton_2")
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(130, 10, 239, 261))
        self.widget.setObjectName("widget")
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.spSlider = QtGui.QSlider(self.widget)
        self.spSlider.setMaximum(255)
        self.spSlider.setOrientation(QtCore.Qt.Vertical)
        self.spSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.spSlider.setTickInterval(32)
        self.spSlider.setObjectName("spSlider")
        self.gridLayout.addWidget(self.spSlider, 0, 0, 1, 1)
        self.outSlider = QtGui.QSlider(self.widget)
        self.outSlider.setMaximum(255)
        self.outSlider.setOrientation(QtCore.Qt.Vertical)
        self.outSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.outSlider.setTickInterval(32)
        self.outSlider.setObjectName("outSlider")
        self.gridLayout.addWidget(self.outSlider, 0, 1, 1, 1)
        self.pvSlider = QtGui.QSlider(self.widget)
        self.pvSlider.setEnabled(False)
        self.pvSlider.setMaximum(255)
        self.pvSlider.setOrientation(QtCore.Qt.Vertical)
        self.pvSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.pvSlider.setTickInterval(32)
        self.pvSlider.setObjectName("pvSlider")
        self.gridLayout.addWidget(self.pvSlider, 0, 2, 1, 1)
        self.spSpinBox = QtGui.QSpinBox(self.widget)
        self.spSpinBox.setAccelerated(True)
        self.spSpinBox.setMaximum(255)
        self.spSpinBox.setObjectName("spSpinBox")
        self.gridLayout.addWidget(self.spSpinBox, 1, 0, 1, 1)
        self.outSpinBox = QtGui.QSpinBox(self.widget)
        self.outSpinBox.setAccelerated(True)
        self.outSpinBox.setMaximum(255)
        self.outSpinBox.setObjectName("outSpinBox")
        self.gridLayout.addWidget(self.outSpinBox, 1, 1, 1, 1)
        self.pvSpinBox = QtGui.QSpinBox(self.widget)
        self.pvSpinBox.setEnabled(False)
        self.pvSpinBox.setAccelerated(True)
        self.pvSpinBox.setMaximum(255)
        self.pvSpinBox.setObjectName("pvSpinBox")
        self.gridLayout.addWidget(self.pvSpinBox, 1, 2, 1, 1)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 562, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.outSlider, QtCore.SIGNAL("valueChanged(int)"), self.outSpinBox.setValue)
        QtCore.QObject.connect(self.pvSlider, QtCore.SIGNAL("valueChanged(int)"), self.pvSpinBox.setValue)
        QtCore.QObject.connect(self.outSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.outSlider.setValue)
        QtCore.QObject.connect(self.pvSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.pvSlider.setValue)
        QtCore.QObject.connect(self.spSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.spSlider.setValue)
        QtCore.QObject.connect(self.spSlider, QtCore.SIGNAL("valueChanged(int)"), self.spSpinBox.setValue)
        QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL("toggled(bool)"), self.outSlider.setDisabled)
        QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL("toggled(bool)"), self.outSpinBox.setDisabled)
        QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL("toggled(bool)"), self.outSpinBox.setEnabled)
        QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL("toggled(bool)"), self.outSlider.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "tinyPIDqt", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("MainWindow", "manual", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_2.setText(QtGui.QApplication.translate("MainWindow", "auto", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">setpoint</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">output</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">process</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

