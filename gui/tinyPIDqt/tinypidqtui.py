# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tinypidqt.ui'
#
# Created: Tue Mar 15 01:57:28 2011
#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(520, 360)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(520, 360))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.toolBox = QtGui.QToolBox(self.centralwidget)
        self.toolBox.setGeometry(QtCore.QRect(310, 10, 201, 321))
        self.toolBox.setFrameShape(QtGui.QFrame.NoFrame)
        self.toolBox.setFrameShadow(QtGui.QFrame.Raised)
        self.toolBox.setObjectName("toolBox")
        self.page_6 = QtGui.QWidget()
        self.page_6.setGeometry(QtCore.QRect(0, 0, 191, 155))
        self.page_6.setObjectName("page_6")
        self.toolBox.addItem(self.page_6, "")
        self.page_5 = QtGui.QWidget()
        self.page_5.setGeometry(QtCore.QRect(0, 0, 191, 155))
        self.page_5.setObjectName("page_5")
        self.layoutWidget = QtGui.QWidget(self.page_5)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 70, 141, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.autoRadioButton = QtGui.QRadioButton(self.layoutWidget)
        self.autoRadioButton.setObjectName("autoRadioButton")
        self.horizontalLayout.addWidget(self.autoRadioButton)
        self.manRadioButton = QtGui.QRadioButton(self.layoutWidget)
        self.manRadioButton.setObjectName("manRadioButton")
        self.horizontalLayout.addWidget(self.manRadioButton)
        self.layoutWidget1 = QtGui.QWidget(self.page_5)
        self.layoutWidget1.setGeometry(QtCore.QRect(2, 0, 141, 50))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.formLayout_6 = QtGui.QFormLayout(self.layoutWidget1)
        self.formLayout_6.setObjectName("formLayout_6")
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.setpoint = QtGui.QSpinBox(self.layoutWidget1)
        self.setpoint.setFrame(True)
        self.setpoint.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.setpoint.setAccelerated(True)
        self.setpoint.setMaximum(255)
        self.setpoint.setObjectName("setpoint")
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.FieldRole, self.setpoint)
        self.label_4 = QtGui.QLabel(self.layoutWidget1)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.output = QtGui.QSpinBox(self.layoutWidget1)
        self.output.setAccelerated(True)
        self.output.setMaximum(255)
        self.output.setObjectName("output")
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.FieldRole, self.output)
        self.toolBox.addItem(self.page_5, "")
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 191, 155))
        self.page_2.setObjectName("page_2")
        self.formLayoutWidget_2 = QtGui.QWidget(self.page_2)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 91, 80))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.kpLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.kpLabel.setObjectName("kpLabel")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.kpLabel)
        self.kiLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.kiLabel.setObjectName("kiLabel")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.kiLabel)
        self.kdLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.kdLabel.setObjectName("kdLabel")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.kdLabel)
        self.kpDoubleSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget_2)
        self.kpDoubleSpinBox.setAccelerated(False)
        self.kpDoubleSpinBox.setObjectName("kpDoubleSpinBox")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.kpDoubleSpinBox)
        self.kiDoubleSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget_2)
        self.kiDoubleSpinBox.setAccelerated(False)
        self.kiDoubleSpinBox.setObjectName("kiDoubleSpinBox")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.kiDoubleSpinBox)
        self.kdDoubleSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget_2)
        self.kdDoubleSpinBox.setAccelerated(False)
        self.kdDoubleSpinBox.setObjectName("kdDoubleSpinBox")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.kdDoubleSpinBox)
        self.formLayoutWidget_3 = QtGui.QWidget(self.page_2)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(90, 20, 81, 60))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_4 = QtGui.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_4.setObjectName("formLayout_4")
        self.tvLabel = QtGui.QLabel(self.formLayoutWidget_3)
        self.tvLabel.setObjectName("tvLabel")
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.tvLabel)
        self.tnLabel = QtGui.QLabel(self.formLayoutWidget_3)
        self.tnLabel.setObjectName("tnLabel")
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.tnLabel)
        self.tvDoubleSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget_3)
        self.tvDoubleSpinBox.setEnabled(False)
        self.tvDoubleSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.tvDoubleSpinBox.setObjectName("tvDoubleSpinBox")
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.tvDoubleSpinBox)
        self.tnDoubleSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget_3)
        self.tnDoubleSpinBox.setEnabled(False)
        self.tnDoubleSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.tnDoubleSpinBox.setObjectName("tnDoubleSpinBox")
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.tnDoubleSpinBox)
        self.ParameterButtonBox = QtGui.QDialogButtonBox(self.page_2)
        self.ParameterButtonBox.setGeometry(QtCore.QRect(0, 100, 176, 25))
        self.ParameterButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset)
        self.ParameterButtonBox.setObjectName("ParameterButtonBox")
        self.toolBox.addItem(self.page_2, "")
        self.page_4 = QtGui.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 191, 155))
        self.page_4.setObjectName("page_4")
        self.formLayoutWidget_4 = QtGui.QWidget(self.page_4)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 101, 111))
        self.formLayoutWidget_4.setObjectName("formLayoutWidget_4")
        self.formLayout_5 = QtGui.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_5.setObjectName("formLayout_5")
        self.xminLabel = QtGui.QLabel(self.formLayoutWidget_4)
        self.xminLabel.setObjectName("xminLabel")
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.LabelRole, self.xminLabel)
        self.xminSpinBox = QtGui.QSpinBox(self.formLayoutWidget_4)
        self.xminSpinBox.setMaximum(255)
        self.xminSpinBox.setObjectName("xminSpinBox")
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.FieldRole, self.xminSpinBox)
        self.xmaxLabel = QtGui.QLabel(self.formLayoutWidget_4)
        self.xmaxLabel.setObjectName("xmaxLabel")
        self.formLayout_5.setWidget(1, QtGui.QFormLayout.LabelRole, self.xmaxLabel)
        self.xmaxSpinBox = QtGui.QSpinBox(self.formLayoutWidget_4)
        self.xmaxSpinBox.setMaximum(255)
        self.xmaxSpinBox.setObjectName("xmaxSpinBox")
        self.formLayout_5.setWidget(1, QtGui.QFormLayout.FieldRole, self.xmaxSpinBox)
        self.yminLabel = QtGui.QLabel(self.formLayoutWidget_4)
        self.yminLabel.setObjectName("yminLabel")
        self.formLayout_5.setWidget(2, QtGui.QFormLayout.LabelRole, self.yminLabel)
        self.yminSpinBox = QtGui.QSpinBox(self.formLayoutWidget_4)
        self.yminSpinBox.setMaximum(255)
        self.yminSpinBox.setObjectName("yminSpinBox")
        self.formLayout_5.setWidget(2, QtGui.QFormLayout.FieldRole, self.yminSpinBox)
        self.ymaxLabel = QtGui.QLabel(self.formLayoutWidget_4)
        self.ymaxLabel.setObjectName("ymaxLabel")
        self.formLayout_5.setWidget(3, QtGui.QFormLayout.LabelRole, self.ymaxLabel)
        self.ymaxSpinBox = QtGui.QSpinBox(self.formLayoutWidget_4)
        self.ymaxSpinBox.setMaximum(255)
        self.ymaxSpinBox.setObjectName("ymaxSpinBox")
        self.formLayout_5.setWidget(3, QtGui.QFormLayout.FieldRole, self.ymaxSpinBox)
        self.ScaleButtonBox = QtGui.QDialogButtonBox(self.page_4)
        self.ScaleButtonBox.setGeometry(QtCore.QRect(0, 120, 176, 25))
        self.ScaleButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset)
        self.ScaleButtonBox.setObjectName("ScaleButtonBox")
        self.toolBox.addItem(self.page_4, "")
        self.page_3 = QtGui.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 191, 155))
        self.page_3.setObjectName("page_3")
        self.layoutWidget2 = QtGui.QWidget(self.page_3)
        self.layoutWidget2.setGeometry(QtCore.QRect(0, 10, 81, 52))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.eepromButton = QtGui.QPushButton(self.layoutWidget2)
        self.eepromButton.setObjectName("eepromButton")
        self.verticalLayout_4.addWidget(self.eepromButton)
        self.fileButton = QtGui.QPushButton(self.layoutWidget2)
        self.fileButton.setObjectName("fileButton")
        self.verticalLayout_4.addWidget(self.fileButton)
        self.toolBox.addItem(self.page_3, "")
        self.page = QtGui.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 191, 155))
        self.page.setObjectName("page")
        self.layoutWidget3 = QtGui.QWidget(self.page)
        self.layoutWidget3.setGeometry(QtCore.QRect(0, 0, 139, 148))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_3.setObjectName("formLayout_3")
        self.portLabel = QtGui.QLabel(self.layoutWidget3)
        self.portLabel.setObjectName("portLabel")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.portLabel)
        self.portLineEdit = QtGui.QLineEdit(self.layoutWidget3)
        self.portLineEdit.setObjectName("portLineEdit")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.portLineEdit)
        self.speedLabel = QtGui.QLabel(self.layoutWidget3)
        self.speedLabel.setObjectName("speedLabel")
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.speedLabel)
        self.speedLineEdit = QtGui.QLineEdit(self.layoutWidget3)
        self.speedLineEdit.setObjectName("speedLineEdit")
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.speedLineEdit)
        self.updateLabel = QtGui.QLabel(self.layoutWidget3)
        self.updateLabel.setObjectName("updateLabel")
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.updateLabel)
        self.updateDoubleSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget3)
        self.updateDoubleSpinBox.setDecimals(1)
        self.updateDoubleSpinBox.setMaximum(10.0)
        self.updateDoubleSpinBox.setSingleStep(0.1)
        self.updateDoubleSpinBox.setObjectName("updateDoubleSpinBox")
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.updateDoubleSpinBox)
        self.verticalLayout_3.addLayout(self.formLayout_3)
        self.connectCheckBox = QtGui.QCheckBox(self.layoutWidget3)
        self.connectCheckBox.setObjectName("connectCheckBox")
        self.verticalLayout_3.addWidget(self.connectCheckBox)
        self.connectButton = QtGui.QPushButton(self.layoutWidget3)
        self.connectButton.setObjectName("connectButton")
        self.verticalLayout_3.addWidget(self.connectButton)
        self.connectionLabel = QtGui.QLabel(self.layoutWidget3)
        self.connectionLabel.setObjectName("connectionLabel")
        self.verticalLayout_3.addWidget(self.connectionLabel)
        self.toolBox.addItem(self.page, "")
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 290, 311))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget4 = QtGui.QWidget(self.groupBox)
        self.layoutWidget4.setGeometry(QtCore.QRect(20, 20, 121, 110))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dialLabel = QtGui.QLabel(self.layoutWidget4)
        self.dialLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dialLabel.setObjectName("dialLabel")
        self.verticalLayout_2.addWidget(self.dialLabel)
        self.dial = QtGui.QDial(self.layoutWidget4)
        self.dial.setMaximum(255)
        self.dial.setWrapping(False)
        self.dial.setNotchesVisible(False)
        self.dial.setObjectName("dial")
        self.verticalLayout_2.addWidget(self.dial)
        self.formLayoutWidget = QtGui.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(170, 20, 101, 86))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_6)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.setpointLabel = QtGui.QLabel(self.formLayoutWidget)
        self.setpointLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.setpointLabel.setMargin(2)
        self.setpointLabel.setIndent(-1)
        self.setpointLabel.setObjectName("setpointLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.setpointLabel)
        self.outputLabel = QtGui.QLabel(self.formLayoutWidget)
        self.outputLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.outputLabel.setMargin(2)
        self.outputLabel.setObjectName("outputLabel")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.outputLabel)
        self.pvLabel = QtGui.QLabel(self.formLayoutWidget)
        self.pvLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.pvLabel.setMargin(2)
        self.pvLabel.setObjectName("pvLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.pvLabel)
        self.errorLabel = QtGui.QLabel(self.formLayoutWidget)
        self.errorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.errorLabel.setMargin(2)
        self.errorLabel.setIndent(-1)
        self.errorLabel.setObjectName("errorLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.errorLabel)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 520, 20))
        self.menubar.setObjectName("menubar")
        self.menuTinyPID = QtGui.QMenu(self.menubar)
        self.menuTinyPID.setObjectName("menuTinyPID")
        MainWindow.setMenuBar(self.menubar)
        self.actionBeenden = QtGui.QAction(MainWindow)
        self.actionBeenden.setObjectName("actionBeenden")
        self.action_Auto_Connect = QtGui.QAction(MainWindow)
        self.action_Auto_Connect.setCheckable(True)
        self.action_Auto_Connect.setObjectName("action_Auto_Connect")
        self.menuTinyPID.addAction(self.actionBeenden)
        self.menubar.addAction(self.menuTinyPID.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionBeenden, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QObject.connect(self.autoRadioButton, QtCore.SIGNAL("toggled(bool)"), self.output.setDisabled)
        QtCore.QObject.connect(self.manRadioButton, QtCore.SIGNAL("toggled(bool)"), self.output.setEnabled)
        QtCore.QObject.connect(self.setpoint, QtCore.SIGNAL("valueChanged(QString)"), self.setpointLabel.setText)
        QtCore.QObject.connect(self.output, QtCore.SIGNAL("valueChanged(QString)"), self.outputLabel.setText)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "tinyPID", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_6), QtGui.QApplication.translate("MainWindow", "Monitor", None, QtGui.QApplication.UnicodeUTF8))
        self.autoRadioButton.setText(QtGui.QApplication.translate("MainWindow", "auto", None, QtGui.QApplication.UnicodeUTF8))
        self.manRadioButton.setText(QtGui.QApplication.translate("MainWindow", "manuell", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "SP:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Output:", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_5), QtGui.QApplication.translate("MainWindow", "Steuerung", None, QtGui.QApplication.UnicodeUTF8))
        self.kpLabel.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">K<span style=\" vertical-align:sub;\">P</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.kiLabel.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">K<span style=\" vertical-align:sub;\">I</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.kdLabel.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">K<span style=\" vertical-align:sub;\">D</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tvLabel.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">T<span style=\" vertical-align:sub;\">V</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tnLabel.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">T<span style=\" vertical-align:sub;\">N</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QtGui.QApplication.translate("MainWindow", "Parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.xminLabel.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">x</span><span style=\" font-size:12pt; vertical-align:sub;\">min</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.xmaxLabel.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">x</span><span style=\" font-size:12pt; vertical-align:sub;\">max</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.yminLabel.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">y</span><span style=\" font-size:12pt; vertical-align:sub;\">min</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.ymaxLabel.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">y</span><span style=\" font-size:12pt; vertical-align:sub;\">max</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), QtGui.QApplication.translate("MainWindow", "Skala", None, QtGui.QApplication.UnicodeUTF8))
        self.eepromButton.setText(QtGui.QApplication.translate("MainWindow", "EEPROM", None, QtGui.QApplication.UnicodeUTF8))
        self.fileButton.setText(QtGui.QApplication.translate("MainWindow", "Datei", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), QtGui.QApplication.translate("MainWindow", "Speichern", None, QtGui.QApplication.UnicodeUTF8))
        self.portLabel.setText(QtGui.QApplication.translate("MainWindow", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.portLineEdit.setText(QtGui.QApplication.translate("MainWindow", "/dev/ttyUSB0", None, QtGui.QApplication.UnicodeUTF8))
        self.speedLabel.setText(QtGui.QApplication.translate("MainWindow", "Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.speedLineEdit.setText(QtGui.QApplication.translate("MainWindow", "19200", None, QtGui.QApplication.UnicodeUTF8))
        self.updateLabel.setText(QtGui.QApplication.translate("MainWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.connectCheckBox.setText(QtGui.QApplication.translate("MainWindow", "Auto-Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.connectButton.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QtGui.QApplication.translate("MainWindow", "Kommunikation", None, QtGui.QApplication.UnicodeUTF8))
        self.dialLabel.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "PV:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Error:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "SP:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Output:", None, QtGui.QApplication.UnicodeUTF8))
        self.setpointLabel.setText(QtGui.QApplication.translate("MainWindow", "255", None, QtGui.QApplication.UnicodeUTF8))
        self.outputLabel.setText(QtGui.QApplication.translate("MainWindow", "255", None, QtGui.QApplication.UnicodeUTF8))
        self.pvLabel.setText(QtGui.QApplication.translate("MainWindow", "255", None, QtGui.QApplication.UnicodeUTF8))
        self.errorLabel.setText(QtGui.QApplication.translate("MainWindow", "255", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTinyPID.setTitle(QtGui.QApplication.translate("MainWindow", "tinyPID", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBeenden.setText(QtGui.QApplication.translate("MainWindow", "&Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Auto_Connect.setText(QtGui.QApplication.translate("MainWindow", "&Auto-Connect", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

