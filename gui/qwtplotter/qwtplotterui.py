# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qwt.ui'
#
# Created: Fri Mar 18 00:45:27 2011
#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.Qwt5 import *


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 520)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(600, 520))
        Form.setMaximumSize(QtCore.QSize(600, 520))
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(11, 11, 571, 491))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridCheckBox = QtGui.QCheckBox(self.widget)
        self.gridCheckBox.setObjectName("gridCheckBox")
        self.horizontalLayout.addWidget(self.gridCheckBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.autoscaleCheckBox = QtGui.QCheckBox(self.widget)
        self.autoscaleCheckBox.setChecked(False)
        self.autoscaleCheckBox.setObjectName("autoscaleCheckBox")
        self.horizontalLayout.addWidget(self.autoscaleCheckBox)
        self.yminSpinBox = QtGui.QSpinBox(self.widget)
        self.yminSpinBox.setAccelerated(True)
        self.yminSpinBox.setMinimum(-9999)
        self.yminSpinBox.setMaximum(9999)
        self.yminSpinBox.setObjectName("yminSpinBox")
        self.horizontalLayout.addWidget(self.yminSpinBox)
        self.ymaxSpinBox = QtGui.QSpinBox(self.widget)
        self.ymaxSpinBox.setMinimum(-9999)
        self.ymaxSpinBox.setMaximum(9999)
        self.ymaxSpinBox.setProperty("value", QtCore.QVariant(300))
        self.ymaxSpinBox.setObjectName("ymaxSpinBox")
        self.horizontalLayout.addWidget(self.ymaxSpinBox)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.viewLabel = QtGui.QLabel(self.widget)
        self.viewLabel.setObjectName("viewLabel")
        self.horizontalLayout.addWidget(self.viewLabel)
        self.viewSpinBox = QtGui.QSpinBox(self.widget)
        self.viewSpinBox.setMinimum(1)
        self.viewSpinBox.setMaximum(120)
        self.viewSpinBox.setProperty("value", QtCore.QVariant(10))
        self.viewSpinBox.setObjectName("viewSpinBox")
        self.horizontalLayout.addWidget(self.viewSpinBox)
        self.stepLabel = QtGui.QLabel(self.widget)
        self.stepLabel.setObjectName("stepLabel")
        self.horizontalLayout.addWidget(self.stepLabel)
        self.scrollSpinBox = QtGui.QSpinBox(self.widget)
        self.scrollSpinBox.setAccelerated(True)
        self.scrollSpinBox.setMaximum(100)
        self.scrollSpinBox.setObjectName("scrollSpinBox")
        self.horizontalLayout.addWidget(self.scrollSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.qwtPlot = QwtPlot(self.widget)
        self.qwtPlot.setObjectName("qwtPlot")
        self.verticalLayout.addWidget(self.qwtPlot)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.gridCheckBox, QtCore.SIGNAL("toggled(bool)"), Form.gridEnable)
        QtCore.QObject.connect(self.scrollSpinBox, QtCore.SIGNAL("valueChanged(int)"), Form.setScroll)
        QtCore.QObject.connect(self.viewSpinBox, QtCore.SIGNAL("valueChanged(int)"), Form.setView)
        QtCore.QObject.connect(self.autoscaleCheckBox, QtCore.SIGNAL("toggled(bool)"), self.yminSpinBox.setHidden)
        QtCore.QObject.connect(self.autoscaleCheckBox, QtCore.SIGNAL("toggled(bool)"), self.ymaxSpinBox.setHidden)
        QtCore.QObject.connect(self.autoscaleCheckBox, QtCore.SIGNAL("toggled(bool)"), Form.setAutoscale)
        QtCore.QObject.connect(self.yminSpinBox, QtCore.SIGNAL("valueChanged(int)"), Form.setYmin)
        QtCore.QObject.connect(self.ymaxSpinBox, QtCore.SIGNAL("valueChanged(int)"), Form.setYmax)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "QWT Plotter", None, QtGui.QApplication.UnicodeUTF8))
        self.gridCheckBox.setText(QtGui.QApplication.translate("Form", "Grid", None, QtGui.QApplication.UnicodeUTF8))
        self.autoscaleCheckBox.setText(QtGui.QApplication.translate("Form", "Autoscale", None, QtGui.QApplication.UnicodeUTF8))
        self.viewLabel.setText(QtGui.QApplication.translate("Form", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.viewSpinBox.setSuffix(QtGui.QApplication.translate("Form", "s", None, QtGui.QApplication.UnicodeUTF8))
        self.stepLabel.setText(QtGui.QApplication.translate("Form", "Scroll", None, QtGui.QApplication.UnicodeUTF8))
        self.scrollSpinBox.setSuffix(QtGui.QApplication.translate("Form", "%", None, QtGui.QApplication.UnicodeUTF8))

#from qwt_plot import QwtPlot

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

