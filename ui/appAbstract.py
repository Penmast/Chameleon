# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'appwidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from appPopUpSecurity import appPopUpSecurity
import time

### This an abstract class for a group or app item, used to secure them
class appAbstract(QWidget):
    def __init__(self, parent=None):

        super(appAbstract, self).__init__(parent)


        ### Create the sub widgets
        self.label = QLabel("")
        self.buttonSecurity = QPushButton()

        ### Resize the self.buttons
        self.sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.buttonSecurity.setSizePolicy(self.sizePolicy)

        ### Add the sub widgets to a layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.buttonSecurity)

        ### Add an image to the buttons
        self.buttonSecurity.setIcon(QIcon('./images/unlock.png'))

        ### Set the layout to the widget
        self.setLayout(self.layout)

        ### Connect the buttons to functions
        self.buttonSecurity.clicked.connect(self.buttonSecurityClick)

        ### Enables de security button if an OpenVPN certificate is present
        self.buttonSecurity.setEnabled(self.hasRegisteredOpenVPNCertificate())

        ### Secured boolean
        self.secured = False

    ### Returns the label's text
    @pyqtSlot()
    def getLabelText(self):
        return self.label.text()

    ### Change the label's text
    @pyqtSlot(str)
    def setLabelText(self, value):
        self.label.setText(value)
        self.update()

    @pyqtSlot(bool)
    def enableSecurityButton(self, value):
        self.buttonSecurity.setEnabled(value)

    @pyqtSlot()
    def getSecured(self):
        return self.secured

    def stopNetwork(self):
        pass

    ### Triggers when the security button is clicked
    @pyqtSlot()
    def buttonSecurityClick(self):
        ### If the app is not secured
        if self.secured is False:
            ### Open the form
            dialog = appPopUpSecurity()
            if "%)" in self.label.text():
                dialog.setTitle(self.label.text().split(' (')[0])
            else:
                dialog.setTitle(self.label.text())

            ### Get the values entered
            value = dialog.exec_()

            ### If the dialog was completed correctly
            if (value != None):
                self.secured = True

                ### Read the current actions file
                filename = "data/appsActions.data"
                fr = open(filename, "r")
                data_list = fr.readlines()
                fr.close()

                try :
                    ### Update an exiting action if needed
                    for line in data_list:
                        if self.label.text() + ",security" in line:
                            data_list.remove(line)

                    ### Write into the file
                    newLine = self.label.text() + ","
                    newLine += "security,"
                    newLine += str(value["duration"])+ ","
                    newLine += str(time.time() + 3600*value["time"]) + "\n"
                    data_list.append(newLine)
                    fh = open(filename, "w")
                    fh.writelines(data_list)
                    fh.close()

                    self.buttonSecurity.setIcon(QIcon('./images/lock.png'))
                    self.manageVPN(value["duration"], value["time"])
                except (RuntimeError):
                    print("App PID has changed, aborting action")
        ### If the app is secured
        else:
            ### Remove the VPN
            self.secured = False
            self.buttonSecurity.setIcon(QIcon('./images/unlock.png'))
            self.stopVPN()

    ### Virtual function to stop running the app through openVPN
    def stopVPN(self):
        pass

    ### Virtual function to start running the app through openVPN
    def manageVPN(self, durationType, durationTime):
        pass

    ### Checks if an openVPN certificate was registered
    ## Returns true is so
    ## Returns false otherwise
    @pyqtSlot()
    def hasRegisteredOpenVPNCertificate(self):
        fr = open('data/openVPNcertificates.data', "r")
        if ( fr.read() is not "" ):
            return True
        else:
            return False


    labelText = pyqtProperty(str, getLabelText, setLabelText)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    appA = appAbstract()
    appA.show()
    sys.exit(app.exec_())
