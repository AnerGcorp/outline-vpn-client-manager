from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt

import sys
import json
from datetime import datetime
from actions.recorddata import RecordData as rd
# from recorddata import RecordData as rd

class AddServer(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.rd = rd()
        self.setWindowTitle("Add Client to Database")
        self.setWindowIcon(QIcon("images/icons/add-server.png"))
        self.setGeometry(450, 150, 450, 300)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.logic()

    def widgets(self):
        self.actionText = QLabel("Choose action")
        self.actionEntry = QComboBox()
        self.actionEntry.addItem(QIcon('images/icons/add-server.png'), "Add Server")
        self.actionEntry.addItem(QIcon('images/icons/remove-server.png'), "Remove Server")
        self.actionEntry.currentTextChanged.connect(self.text_changed)
        self.serverNamesText = QLabel("Server names")
        self.serverNamesEntry = QComboBox()
        self.serverNameText = QLabel("Enter name of server")
        self.serverNameEntry = QLineEdit()
        self.serverNameEntry.textChanged.connect(self.verifyServerName)
        self.serverNameEntry.setPlaceholderText("e.g: iowa-1, ger-1, osaka-3,..")
        self.serverObjectText = QLabel("Enter server")
        self.serverObjectEntry = QPlainTextEdit() # QLineEdit()
        self.serverObjectEntry.setPlaceholderText(
            "e.g: {\n'apiUrl': \n\t'https://34.97.7.154:35154/FkF2pDS2XW5BAxsvTjpGfw',\n'certSha256': \n\t'755859EA4CEE72186F6164960565923D34A36A64FC1ECB40704140665F21466C'\n}"
            )
        self.serverObjectEntry.setFixedHeight(120)
        self.showStatus = QLabel()
        self.showStatus.setFont(QFont("Arial", 14))
        self.showStatus.setStyleSheet("QLabel {color: red}")
        self.addServerBtn = QPushButton(QIcon('images/icons/add-server.png'), "Add Server")
        self.addServerBtn.clicked.connect(self.funcAddServer)
        self.removeServerBtn = QPushButton(QIcon('images/icons/remove-server.png'), "Remove Server")
        self.removeServerBtn.clicked.connect(self.funcRemoveServer)

    def logic(self):
        self.servers = self.rd.read_servers()
        self.text_changed()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayoutTop = QFormLayout()
        self.mainLayoutTop.addRow(self.actionText, self.actionEntry)
        
        self.addServerFrame = QFrame()
        self.addServerLayout = QFormLayout()
        self.addServerLayout.addRow(self.serverNameText, self.serverNameEntry)
        self.addServerLayout.addRow(self.serverObjectText, self.serverObjectEntry)
        self.addServerLayout.addRow(self.showStatus)
        self.addServerLayout.addRow(self.addServerBtn)
        self.addServerFrame.setLayout(self.addServerLayout)

        self.removeServerFrame = QFrame()
        self.removeServerLayout = QGridLayout()
        self.removeServerLayout.addWidget(self.serverNamesText, 0, 0)
        self.removeServerLayout.addWidget(self.serverNamesEntry, 0, 1)
        self.removeServerLayout.addWidget(self.removeServerBtn, 1, 0, 1, 2)
        self.removeServerFrame.setLayout(self.removeServerLayout)

        self.mainLayout.addLayout(self.mainLayoutTop)
        self.mainLayout.addWidget(self.addServerFrame)
        self.mainLayout.addWidget(self.removeServerFrame)
        self.setLayout(self.mainLayout)

    def verifyServerName(self):
        self.serverName = self.serverNameEntry.text()
        for server in self.servers:
            if self.serverName == list(server.keys())[0]:
                self.showStatus.setText("Please choose different name..")
                break
        else:
            self.showStatus.clear()

    def funcAddServer(self):
        self.servers = self.rd.read_servers()

        self.serverEntry = self.serverObjectEntry.toPlainText()
        if self.serverEntry:
            try:
                self.serverEntry = json.loads(self.serverEntry)
                self.serverValues = list(self.serverEntry.keys())
                print("Server values:", self.serverValues)
                if self.serverValues != ["apiUrl", "certSha256"]:
                    self.message = QMessageBox.warning(
                    self, 
                    "Wrong Server Entry",
                    "Make sure your server correct format")
                    self.serverObjectEntry.clear()
                else:
                    if not self.showStatus.text():
                        self.server = {self.serverName: self.serverEntry}
                        self.verifyServerName()
                        today = datetime.now().strftime("%H:%M %d/%m/%y")
                        self.server['status'] = False
                        self.server['dateCreated'] = today
                        self.servers.append(self.server)
                        self.rd.write_servers(self.servers)
                        self.serverObjectEntry.clear()
                        self.serverNameEntry.clear()
                    else:
                        self.message = QMessageBox.information(
                            self,
                            "Wrong Information",
                            "Please choose different name for your server.."
                        )
            except AttributeError as e:
                self.message = QMessageBox.warning(
                    self, 
                    "Wrong Server Entry",
                    "Make sure your server correct format")
                self.serverObjectEntry.clear()
            except json.decoder.JSONDecodeError as e:
                self.message = QMessageBox.warning(
                    self, 
                    "Wrong Server Entry",
                    "Make sure your server correct format")
                self.serverObjectEntry.clear()
            
        else:
            self.message = QMessageBox.information(
                    self, 
                    "Missing fields",
                    "Make sure you fill all the fields with\n desired information..")
        self.parent.display_servers()

    def funcRemoveServer(self):
        self.servers = self.rd.read_servers()

        self.selectedServer = self.serverNamesEntry.currentText()
        for server in self.servers:
            if self.selectedServer == list(server.keys())[0]:
                index = self.servers.index(server)
                break
        self.message = QMessageBox.warning(
            self,
            "Remove Server",
            "Do you really want to remove <b>{}</b> server from database!".format(self.selectedServer),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) 

        if self.message == QMessageBox.StandardButton.Yes:
            item_index = self.serverNamesEntry.currentIndex()
            self.serverNamesEntry.removeItem(item_index)
            del self.servers[index]
            self.rd.write_servers(self.servers)
            
        self.parent.display_servers()

    def text_changed(self):
        if self.actionEntry.currentText() == "Add Server":
            self.addServerFrame.show()
            self.removeServerFrame.hide()

        else:
            self.addServerFrame.hide()
            self.removeServerFrame.show()
            for server in self.servers:
                self.serverNamesEntry.addItem(list(server.keys())[0])    

# def main():
#     app = QApplication(sys.argv)
#     window = AddServer()
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()