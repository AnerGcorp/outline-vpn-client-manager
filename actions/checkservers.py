from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt

import sys
import json
from actions.recorddata import RecordData as rd
from actions.serversideactions import SActions as SA
from actions.extensions import Extensions


class CheckServers(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.rd = rd()
        self.sa = SA()
        self.ext = Extensions()
        self.setWindowTitle("Check Servers")
        self.setWindowIcon(QIcon("images/icons/server-search.png"))
        self.setGeometry(200, 200,  600, 400)
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.logic()
        self.layouts()
        
    def widgets(self):
        self.check = QPushButton("Check")
        self.statusFailed = QLabel()
        self.statusSuccess = QLabel()
        self.statusProgress = QProgressBar()
        self.listServerStatus = QListWidget()
        

    def logic(self):
        self.servers = self.rd.read_servers()
        self.success = 0
        self.failed = 0
        self.total = len(self.servers)
        self.start = 0
        self.counter = 1
        self.statusProgress.setRange(self.start, self.total)

    def layouts(self):
        self.check.clicked.connect(self.funcUpdateBtn)
        self.mainLayout = QVBoxLayout()
        self.mainTopLayout = QHBoxLayout()
        self.mainMiddleLayout = QHBoxLayout()
        self.mainBottomLayout = QHBoxLayout()

        self.mainTopLayout.addWidget(self.check)
        self.mainTopLayout.addWidget(self.statusProgress)
        self.mainMiddleLayout.addWidget(self.statusSuccess)
        self.mainMiddleLayout.addWidget(self.statusFailed)

        self.mainBottomLayout.addWidget(self.listServerStatus)
        self.mainLayout.addLayout(self.mainTopLayout)
        self.mainLayout.addLayout(self.mainMiddleLayout)
        self.mainLayout.addLayout(self.mainBottomLayout)

        self.setLayout(self.mainLayout)

    def funcUpdateBtn(self):
        if self.servers == [] or self.servers == None:
            self.message = QMessageBox(
                self,
                "Server Misconfiguration",
                "You have misconfigured servers database,\n Please contact the server administrator"
            )
        self.listServerStatus.addItem("Server Name\t\t Server IP\t\t Completed\t\t Is Running")
        for server in self.servers:
            self.counter += 1
            serverName = list(server.keys())[0]
            serverObj = server[serverName]
            serverUrl = serverObj["apiUrl"]
            serverIp = serverUrl[8:].split(":")[0]
            status = self.ext.is_pingable(serverIp)
            index = self.servers.index(server)
            server["status"] = status
            if status:
                self.success += 1
                self.statusSuccess.setText("Success: {}".format(self.success))
                self.listServerStatus.addItem("{0}\t\t {1}\t\t Done\t\t {2}".format(serverName, serverIp, status))
            else:
                self.failed += 1
                self.statusFailed.setText("Failed: {}".format(self.failed))
                self.listServerStatus.addItem("{0}\t\t {1}\t\t Done\t\t {2}".format(serverName, serverIp, status))
            self.statusProgress.setValue(self.counter)
            
            self.servers = self.ext._replace(self.servers, index, server)
        self.rd.write_servers(self.servers)
        self.statusSuccess.setText("Success: {}".format(self.success))
        self.statusFailed.setText("Failed: {}".format(self.failed))
        self.parent.display_servers()

            

# def main():
#     app = QApplication(sys.argv)
#     window = UpdateKeys()
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()






    
