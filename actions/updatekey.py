from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt

from datetime import datetime, timedelta
import sys
import json
from actions.recorddata import RecordData as rd
from actions.serversideactions import SActions as SA
from actions.extensions import Extensions

class UpdateKey(QWidget):
    def __init__(self, par=None, server_name=""):
        super().__init__()
        self.parent = par
        self.rd = rd()
        self.sa = SA()
        self.ext = Extensions()
        self.keys = []
        self.server_name = server_name
        self.servers = self.rd.read_servers()
        self.setWindowIcon(QIcon("images/icons/update-key.png"))
        self.setGeometry(200, 200,  300, 400)
        self.UI()

    def UI(self):
        self.widgets()
        self.logic()
        self.layouts()
    
    def logic(self):
        try:
            # current Window
            if self.parent != None and self.server_name == "":
                selected_client = self.parent.clientsTable.currentRow()
                _id = self.parent.clientsTable.item(selected_client, 0).text()
                _id = int(_id)
                
                for c in self.parent.clients:
                    if c['_id'] == _id:
                        self.index = self.parent.clients.index(c)
                        break
                self.client = self.parent.clients[self.index]
                # try FileNotFoundError
                server_list = []
                for _ in self.servers:
                    # server_list += [i for i in _.keys()]
                    server_list.append(list(_.keys())[0])
                print("this is server list: ", server_list)
                self.serverEntry.addItem("None")
                for _ in server_list:
                    self.serverEntry.addItem(_)
                if self.client['server'] != None:
                    self.serverEntry.setCurrentText(list(self.client['server'].keys())[0])
                else:
                    self.serverEntry.setCurrentText("None")
                self.nameText.setText(self.client["name"])
                self.nameText.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.parent.display_items()
            # parent window
            else:
                self.parMain = self.parent.parent
                selected_client = self.parMain.clientsTable.currentRow()
                _id = self.parMain.clientsTable.item(selected_client, 0).text()
                _id = int(_id)
                for c in self.parMain.clients:
                    if c['_id'] == _id:
                        self.index = self.parMain.clients.index(c)
                        break
                self.client = self.parMain.clients[self.index]  

                if self.client['server'] != None or self.client['server'] == '':
                    self.parent.serverEntry.setCurrentText(list(self.client['server'].keys())[0])
                else:
                    self.parent.serverEntry.setCurrentText("None")
                self.parent.keyDisplay.setText(str(len(self.keys)))
                self.parMain.display_items()
                
        except AttributeError as e:
            self.message = QMessageBox.information(
                self, 
                "Update Client",
                "No Client selected for update")
            print("You have clicked wrong place..")

    def widgets(self):
        self.nameText = QLabel()
        self.nameText.setFont(QFont("Times", 20))
        self.serverText = QLabel("Servers")
        self.serverEntry = QComboBox()
        self.keyText = QLabel("Keys #")
        self.keyDisplay = QLabel()
        self.updateBtn = QPushButton(QIcon("images/icons/update-key.png"), "Update Key")
        

    def layouts(self):
        self.updateBtn.clicked.connect(self.call_update_client_key)

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.nameText, 0, 0, 2, 2)
        self.mainLayout.addWidget(self.keyText, 3, 0)
        self.mainLayout.addWidget(self.keyDisplay, 3, 1)
        self.mainLayout.addWidget(self.serverText, 4, 0)
        self.mainLayout.addWidget(self.serverEntry, 4, 1)
        self.mainLayout.addWidget(self.updateBtn, 5, 0, 1, 2)
        self.setLayout(self.mainLayout)    

    def call_update_client_key(self):
        self.message = QMessageBox.warning(
            self,
            "Connection Error",
            "You don't have internet Connection, \nplease connect the internet and try again"
        )
        self.updateBtn.setDisabled(True)
        self.update_client_key(server_name="")
        self.updateBtn.setDisabled(False)

    def update_client_key(self, server_name=''):
        if server_name == "":
            self.server = self.selected_server(server_name)

            try:
                server = list(self.server.values())[0]
                ## check it is current window or parent window
                name = self.client['name']
                device = self.client['device']

                try:
                    if self.server:
                        self.keys = self.sa.get_client_keys(server, name, device)
                    else:
                        self.keys = []
                except ConnectionError and OSError as e:
                    print("There is an error on your connection!")
                    self.keyDisplay.setText("You have connection problem")
                    self.message = QMessageBox.warning(self, 
                    "Connection Problem",
                    "Whether you are not connected to internet \nor your server is blocked by ISP provider \n:(")
                self.key = self.keys
                if self.server:
                    self.keyDisplay.setText("You have {} active keys".format(len(self.keys)))
                else:
                    self.key = []
                    self.keyDisplay.setText("Please select the server from list..")
                self.client['server'] = self.server
                self.client['key'] = self.key
                self.clients = self.ext._replace(self.parent.clients, self.index, self.client)

            except AttributeError as e:
                self.server_message = QMessageBox.warning(self, 
                "Action Required",
                "You did not choose any server for creating keys,\n please choose server from list")
                self.client['server'] = None
                self.client['key'] = []
            
            self.clients = self.rd.read_clients()
            # changed clients to self.clients
            self.clients = self.ext._replace(self.clients, self.index, self.client)
            self.rd.write_clients(self.clients)
            self.parent.display_items()

        else:
            self.server = self.selected_server(server_name)
            try:
                server = list(self.server.values())[0]
                name = self.parent.client['name']
                device = self.parent.client['device']

                try:
                    self.keys = self.sa.get_client_keys(server, name, device)
                    if self.server:
                        self.parent.key = self.keys
                        self.parent.keyDisplay.setText("You have {} active keys".format(len(self.keys)))
                    else:
                        self.parent.key = []
                        self.parent.keyDisplay.setText("Please select the server from list..")
                        self.parent.client['server'] = None
                        self.parent.client['key'] = []

                except ConnectionError and OSError as e:
                    print("There is an error on your connection!")
                    self.keyDisplay.setText("You have connection problem")
                    self.con_message = QMessageBox.warning(self, 
                    "Connection Problem",
                    "Whether you are not connected to internet \nor your server is blocked by ISP provider \n:(")
                    
                    if self.server:
                        self.parent.key = []
                        self.parent.server = self.server
                        self.parent.keyDisplay.setText("You have no active keys")
                    else:
                        self.parent.server = []
                        self.parent.key = []

            except AttributeError as e:
                self.server_message = QMessageBox.warning(self, 
                "Action Required",
                "You did not choose any server for creating keys,\n please choose server from list")
                self.parent.server = None
                self.parent.key = []
                self.parent.client['server'] = None
                self.parent.client['key'] = []
            
            except UnboundLocalError as e:
                self.parent.server = None
                self.parent.key = []
                self.parent.client['server'] = None
                self.parent.client['key'] = []

            self.clients = self.rd.read_clients()
            # changed clients to self.clients
            self.clients = self.ext._replace(self.clients, self.index, self.parent.client)
            self.rd.write_clients(self.clients)
            self.parMain.display_items()
        
        # self.parent.serverEntry.currentTextChanged.connect(self.activate_update_btn)

        if self.close() and server_name != "":
            print("Closing Application")
            self.parent.keyUpdateBtn.setDisabled(True)   
    
    def selected_server(self, server_name=''):
        if server_name == "":
            selected_server_name = self.serverEntry.currentText()
            if selected_server_name == "None":
                self.updateBtn.setDisabled(True)
                self.keyDisplay.setText("Please choose a server from list")
                return None
            for item in self.servers:
                if list(item.keys())[0] == selected_server_name:
                    server_index = self.servers.index(item)
                    break
            selected_server = self.servers[server_index]
            return selected_server
            
        else:
            selected_server = server_name
            print("TEST 3")
            # selected_server = "iowa-1"
            print("selected server: ", selected_server)
            if selected_server == "None":
                return None
            if selected_server != "None" or selected_server != '':
                self.parent.serverEntry.setCurrentText(selected_server)
                for item in self.servers:
                    if list(item.keys())[0] == selected_server:
                        server_index = self.servers.index(item)
                selected_server = self.servers[server_index]
                return selected_server
        


# def main():
#     app = QApplication(sys.argv)
#     window = UpdateKey()
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()