# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'appwidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time

### The dialog window showing the apps in a group, and allowing the user to remove them from the group
class appsInGroupWidget(QDialog):
    def __init__(self, parent=None):

        super(appsInGroupWidget, self).__init__(parent)
        self.setFixedSize(200, 400)
        self.setWindowTitle("Apps in group")
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.setStyleSheet("QDialog{background-color:white;}QLabel{color:rgba(41, 107, 116, 1);}QPushButton{border-radius: 20px;width:60px; height:60px;border: 1px solid rgb(41, 107, 116); background-color: rgb(41, 107, 116);}QPushButton:hover{border: 1px solid rgba(41, 107, 116, 0.5); background-color: rgba(41, 107, 116,0.5);}")

        ### Title label
        self.labelTitle = QLabel()
        font = QFont()
        font.setPointSize(20)
        font.setWeight(0)
        font.setLetterSpacing(QFont.AbsoluteSpacing,2)
        self.labelTitle.setFont(font)
        self.labelTitle.setTextFormat(Qt.AutoText)
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.labelTitle)

        ### Line separator
        self.line = QFrame();
        self.line.setFrameShape(QFrame.HLine);
        self.line.setFrameShadow(QFrame.Sunken);
        self.mainLayout.addWidget(self.line)

        ### The list of the apps
        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.mainLayout.addWidget(self.list)

        self.appListLayoutWidget = QWidget()
        self.mainLayout.addWidget(self.appListLayoutWidget)
        self.appListLayout = QVBoxLayout(self.appListLayoutWidget)
        self.appListLayout.addWidget(self.list)

        ## Delete button
        self.buttonDelete = QPushButton()
        self.buttonDelete.setIcon(QIcon('./images/deletewhite.png'))
        self.buttonDelete.setToolTip("Remove application(s) from group")
        self.mainLayout.addWidget(self.buttonDelete)
        self.buttonDelete.clicked.connect(self.deleteSelection)

        self.setWindowTitle("Apps in group")

    def setTitle(self, title):
        self.labelTitle.setText(title)

    ### Fills the apps list
    def fillList(self, listApp):
        self.list.clear()
        for app in listApp:
            self.list.addItem(app)

    ### Remove the deleted apps from the group
    def deleteSelection(self):
        toDelete = []
        for app in self.list.selectedItems():
            toDelete.append(app.text())
        self.delSig.emit(toDelete)

    def setDeleteSignal(self, signal):
        self.delSig = signal



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    appA = appsInGroupWidget()
    appA.show()
    sys.exit(app.exec_())
