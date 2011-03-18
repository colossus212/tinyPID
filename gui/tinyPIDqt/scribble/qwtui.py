# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qwt.ui'
#
# Created: Thu Mar 17 16:48:34 2011
#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.Qwt5 import *

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(520, 418)
        self.qwtPlot = QwtPlot(Form)
        self.qwtPlot.setGeometry(QtCore.QRect(10, 10, 501, 401))
        self.qwtPlot.setObjectName("qwtPlot")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))

#from qwt_plot import QwtPlot

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

