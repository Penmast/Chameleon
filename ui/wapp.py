from PyQt5.QtCore import *
from appAbstract import appAbstract
import sys
sys.path.append("Network")
import inject

### This class represents an item corresponding to a running process using internet
class WappWidget(appAbstract):

    def __init__(self, parent=None):

        super(WappWidget, self).__init__(parent)

        self.setStyleSheet("QPushButton{border-radius: 5px;width:60px; height:60px; border: 1px solid rgba(41, 107, 116,1); background-color: rgba(41, 107, 116,0);}QPushButton:hover{background-color: rgba(41, 107, 116,0.25);}")
        self.buttonSecurity.setIconSize(QSize(40,40))
        self.buttonSecurity.setToolTip("Security configuration")
        self.threadList = {}
        self.nic = None

    @pyqtSlot(str)
    def setProcessName(self, value):
        self.processName = value

    @pyqtSlot()
    def getProcessName(self):
        return self.processName

    @pyqtSlot(list)
    def setPIDlist(self, value):
        self.PID_list = value

    @pyqtSlot()
    def getPIDlist(self):
        return self.PID_list

    def setNic(self, nic):
        self.nic = nic

    ### Runs the app through openVPN
    def manageVPN(self, durationType, durationTime):
        self.threadList = inject.ChangeProcessIp(self.PID_list, self.processName, self.nic)

    ### Detaches the app from openVPN
    def stopVPN(self):
        self.clean()

    ### Detaches the app from openVPN
    def clean(self):
        self.deleteAction()
        if len(self.threadList) is not 0:
            for key,thread in self.threadList.items():
                try:
                    thread.do_run = False
                except:
                    pass

    ### Deletes an action from the actions file
    def deleteAction(self):
            fr = open('data/appsActions.data', 'r')
            actions = fr.readlines()
            fr.close()

            insertData = []

            for action in actions:
                line = action.split(',')
                dic = {'processName':line[0], 'actionType':line[1], 'durationType':line[2], 'durationTime':line[3]}

                if ( not (dic['processName'] == self.processName and dic['actionType'] == 'security' ) ):
                    insertData.append(action)

                fw = open('data/appsActions.data', 'w')
                fw.writelines(insertData)
                fw.close()






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wapp = WappWidget()
    wapp.show()
    sys.exit(app.exec_())
