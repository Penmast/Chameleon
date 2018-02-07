# -*- coding: utf-8 -*-

# self implementation generated from reading ui file 'appPopUpSecurity.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

### The form for the duration of a security action
class appPopUpSecurity(QDialog):
    def __init__(self):
        super(appPopUpSecurity, self).__init__()

        ### Set up the form window
        self.setObjectName("appPopUpSecurity")
        self.setFixedSize(329, 290)

        self.setStyleSheet("QDialog{background-color:white;}QLabel#label,QLabel#label_2{color:rgba(41, 107, 116, 1);}")


        ### Title
        self.labelTitle = QLabel(self)
        self.labelTitle.setWordWrap(True)
        self.labelTitle.setGeometry(QRect(0, 0, 329, 71))
        font = QFont()
        font.setPointSize(18)
        font.setWeight(0)
        font.setLetterSpacing(QFont.AbsoluteSpacing,2)
        self.labelTitle.setFont(font)
        self.labelTitle.setTextFormat(Qt.AutoText)
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.labelTitle.setObjectName("label")

        ### Line under title
        self.line = QFrame(self)
        self.line.setGeometry(QRect(60, 70, 221, 16))
        self.line.setLineWidth(1)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")

        ### Network subtitle
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(20, 120, 281, 20))
        font = QFont()
        font.setPointSize(11)
        font.setLetterSpacing(QFont.AbsoluteSpacing,2)
        font.setWeight(0)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        ### Form layout
        self.formLayoutWidget = QWidget(self)
        self.formLayoutWidget.setGeometry(QRect(20, 150, 281, 71))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout_2 = QFormLayout(self.formLayoutWidget)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")

        ##### Duration menu
        ### Drop down menu label
        self.label_6 = QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_6)

        ### Drop down menu
        self.durationBox = QComboBox(self.formLayoutWidget)
        self.durationBox.setObjectName("durationBox")
        self.durationBox.addItem("")
        self.durationBox.addItem("")
        self.durationBox.addItem("")
        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.durationBox)

        self.durationBox.currentIndexChanged.connect(self.activateTimeInput)

        ##### Time menu
        ### Time label
        self.label_7 = QLabel(self.formLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_7)

        ### Time input
        self.inputTime = QLineEdit(self.formLayoutWidget)
        self.inputTime.setObjectName("inputTime")
        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.inputTime)
        self.inputTime.setEnabled(False)

        ### Submit button
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QRect(210, 240, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.exitDialog)

        self.cancel = False

        self.retranslateUi(self)
        QMetaObject.connectSlotsByName(self)

    @pyqtSlot()
    def exitDialog(self):
        self.accept()

    ### Enable or disable the time input if it is needed or not
    @pyqtSlot()
    def activateTimeInput(self):
        if (self.durationBox.currentIndex() == 1):
            self.inputTime.setEnabled(True)
        else:
            self.inputTime.setEnabled(False)
            self.inputTime.setText("")

    @pyqtSlot(str)
    def setTitle(self, value):
        self.labelTitle.setText(value)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Security options"))
        self.labelTitle.setText(_translate("Dialog", "Appli Name"))
        self.label_2.setText(_translate("Dialog", "Security"))
        self.pushButton.setText(_translate("Dialog", "OK"))
        self.label_6.setText(_translate("Dialog", "Duration"))
        self.durationBox.setItemText(0, _translate("Dialog", "Until the application is closed"))
        self.durationBox.setItemText(1, _translate("Dialog", "For a set period of time"))
        self.durationBox.setItemText(2, _translate("Dialog", "Forever"))
        self.label_7.setText(_translate("Dialog", "Hours"))

    def closeEvent(self, event):
        self.cancel = True
        self.reject()


    ### Is triggered when the form is the submit.
    ### Returns the following dictionary:
    #### 'duration' : the type of duration; 0: until the application is closed, 1: for a set period of time, 2: forever
    #### 'time' : the entered set period of time
    ### Returns None if the form is cancelled
    def exec_(self):
        super(appPopUpSecurity, self).exec_()
        if(self.cancel is True):
            return None
        if( self.durationBox.currentIndex() == 1 ):
            return { 'duration' : self.durationBox.currentIndex(), 'time' : int(self.inputTime.text()) }
        else:
            return { 'duration' : self.durationBox.currentIndex(), 'time' : 0 }
