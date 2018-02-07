from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

### The dialog window showing the apps in a group, and allowing the user to remove them from the group
class hostsInChannelWidget(QDialog):
    def __init__(self, parent=None):

        super(hostsInChannelWidget, self).__init__(parent)
        self.setFixedSize(300, 400)
        self.setWindowTitle("Hosts in Channel")


        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.setStyleSheet("QDialog{background-color:white;}QLabel{color:rgba(41, 107, 116, 1);}")

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

        self.hostitemsLayout = QFormLayout()
        self.hostitemsLayout.setObjectName("hostitemsLayout")
        self.mainLayout.addLayout(self.hostitemsLayout)

        line0 = QFrame();
        line0.setFrameShape(QFrame.HLine);
        line0.setFrameShadow(QFrame.Sunken);
        self.hostitemsLayout.setWidget(0, QFormLayout.SpanningRole, line0)

        font = QFont()
        font.setBold(True)
        font.setWeight(75)

        self.hostnamelab = QLabel()
        self.hostnamelab.setFont(font)
        self.hostnamelab.setText("Host Name")
        self.hostitemsLayout.setWidget(1, QFormLayout.LabelRole, self.hostnamelab)

        self.siglab = QLabel()
        self.siglab.setFont(font)
        self.siglab.setText("Signal")
        self.hostitemsLayout.setWidget(1, QFormLayout.FieldRole, self.siglab)

        line1 = QFrame();
        line1.setFrameShape(QFrame.HLine);
        line1.setFrameShadow(QFrame.Sunken);
        self.hostitemsLayout.setWidget(2, QFormLayout.SpanningRole, line1)


    def fillList(self, hostList, title):
        i = 2
        self.labelTitle.setText(title)

        for key, value in hostList.items():

            print(key)
            print(value)

            i = i + 1
            host = QLabel()
            host.setText(key)
            self.hostitemsLayout.setWidget(i, QFormLayout.LabelRole, host)

            sig = QLabel()
            sig.setText(value)
            self.hostitemsLayout.setWidget(i, QFormLayout.FieldRole, sig)

            i = i + 1

            line = QFrame();
            line.setFrameShape(QFrame.HLine);
            line.setFrameShadow(QFrame.Sunken);
            self.hostitemsLayout.setWidget(i, QFormLayout.SpanningRole, line)
