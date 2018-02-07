# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'speedtest.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
sys.path.append("../Network")

class VPNstatusWidget(QWidget):

    def __init__(self, parent=None):

        super(VPNstatusWidget, self).__init__(parent)

        self.mainlayout = QHBoxLayout()
        self.setLayout(self.mainlayout)

        self.label = QLabel("VPN status:")
        self.mainlayout.addWidget(self.label)

        self.imgGreen = QIcon('./images/vpngreen.png')
        self.imgRed = QIcon('./images/vpnred.png')

        self.button = QPushButton()
        self.button.setIcon(self.imgRed)
        self.button.clicked.connect(self.buttonClicked)
        self.button.setFlat(True)
        self.button.setIconSize(QSize(40,60))
        self.mainlayout.addWidget(self.button)

        self.secured = False
        self.setActive()

    def getStatus(self):
        return self.secured

    def setActive(self):
        self.secured = True
        self.button.setIcon(self.imgGreen)

    def setInactive(self):
        self.secured = False
        self.button.setIcon(self.imgRed)

    def toggleStatus(self):
        if self.secured is True:
            self.secured = False
            self.button.setIcon(self.imgRed)
        else:
            self.secured = True
            self.button.setIcon(self.imgGreen)

    def setSignal(self, signal):
        self.signal = signal

    def buttonClicked(self):
        self.signal.emit()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    appA = VPNstatusWidget()
    appA.show()
    sys.exit(app.exec_())
