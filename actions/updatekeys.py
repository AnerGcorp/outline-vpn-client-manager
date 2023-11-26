from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt

import sys
import json
from actions.recorddata import RecordData as rd
from actions.serversideactions import SActions as SA
from actions.extensions import Extensions


class UpdateKeys(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.rd = rd()
        self.sa = SA()
        self.ext = Extensions()
        self.servers = self.rd.read_servers()
        self.setWindowTitle("Update Keys")
        self.setWindowIcon(QIcon("images/icons/update-key.png"))
        self.setGeometry(200, 200,  450, 600)
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.logic()
        self.layouts()
        
    def widgets(self):
        self.update = QPushButton("Update")
        self.statusFailed = QLabel()
        self.statusSuccess = QLabel()
        self.statusProgress = QProgressBar()
        self.listServerStatus = QListWidget()
        

    def logic(self):
        self.clients = self.rd.read_clients()
        self.success = 0
        self.failed = 0
        self.total = len(self.clients)
        self.start = 0
        self.counter = 1

        self.statusProgress.setRange(self.start, self.total)
        
                


    def layouts(self):
        self.update.clicked.connect(self.funcUpdateBtn)
        self.mainLayout = QVBoxLayout()
        self.mainTopLayout = QHBoxLayout()
        self.mainMiddleLayout = QHBoxLayout()
        self.mainBottomLayout = QHBoxLayout()

        self.mainTopLayout.addWidget(self.update)
        self.mainTopLayout.addWidget(self.statusProgress)
        self.mainMiddleLayout.addWidget(self.statusSuccess)
        self.mainMiddleLayout.addWidget(self.statusFailed)

        self.mainBottomLayout.addWidget(self.listServerStatus)
        self.mainLayout.addLayout(self.mainTopLayout)
        self.mainLayout.addLayout(self.mainMiddleLayout)
        self.mainLayout.addLayout(self.mainBottomLayout)

        self.setLayout(self.mainLayout)

    def funcUpdateBtn(self):
        
        self.listServerStatus.addItem("Client Name\t\t Completed\t\t Status")
        status = False
        for client in self.clients:
            self.counter += 1
            server = client['server']
            if server == "" or server == None:
                print("Please First Choose server!")
                self.failed += 1
                self.statusFailed.setText("Failed: {}".format(self.failed))
                status = False
                self.listServerStatus.addItem("{0} \t\t Done\t\t {1}".format(client['name'], "Running.." if status else "Stopped." ))
                client['key'] = []
                self.statusProgress.setValue(self.counter)
            else:
                serverName = list(server.keys())[0]
                server = server[serverName]
                self.key = self.sa.get_client_keys(server, client['name'], client['device'])
                if self.key:
                    self.success += 1
                    status = True
                else:
                    self.failed += 1
                    status = False
                self.statusSuccess.setText("Success: {}".format(self.success))
                self.statusFailed.setText("Failed: {}".format(self.failed))
                client['key'] = self.key
                self.statusProgress.setValue(self.counter)
                client['status'] = status
                self.listServerStatus.addItem("{0} \t\t Done\t\t {1}".format(client['name'], "Running.." if status else "Stopped." ))
            index = self.clients.index(client)
            # WE MAY COME up here with bugs
            self.clients = self.ext._replace(self.clients, index, client)
        self.rd.write_clients(self.clients)
        self.parent.display_items()


# def main():
#     app = QApplication(sys.argv)
#     window = UpdateKeys()
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()






    
