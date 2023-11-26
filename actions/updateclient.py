from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

from datetime import datetime, timedelta
import sys
import json
from actions.client_object import Client
from actions.extensions import Extensions
from actions.recorddata import RecordData as rd
from actions.updatekey import UpdateKey as uk

class UpdateClient(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.rd = rd()
        self.setWindowTitle("Update Client Information")
        self.setWindowIcon(QIcon("images/icons/update-user.png"))
        self.setGeometry(450, 150, 350, 650)
        self.setFixedSize(self.size())
        self.UI()
        self.show()


    def UI(self):
        self.widgets()
        self.get_values()
        self.layouts()

    def widgets(self):
        ########### Widgets of Top Layout #################
        self.clientImg = QLabel()
        self.image = QPixmap("images/icons/tortoise.png")
        self.clientImg.setPixmap(self.image)
        ########## Widgets of Bottom Layout ##############
        self.nameText = QLabel("Name")
        self.nameEntry = QLineEdit()
        self.phoneText = QLabel("Phone Number")
        self.phoneEntry = QLineEdit()
        self.mailText = QLabel("Mail Addres")
        self.mailEntry = QLineEdit()
        self.serverText = QLabel("Servers")
        self.serverEntry = QComboBox()
        self.deviceText = QLabel("Devices #")
        self.deviceEntry = QSpinBox()
        self.deviceEntry.setValue(1)
        self.deviceEntry.setMinimum(1)
        self.deviceEntry.setMaximum(30)
        # discounting
        self.discountLayout = QHBoxLayout()
        self.discountText = QLabel("Discount")
        self.discountEntry = QSpinBox()
        self.discountEntry.setValue(0)
        self.discountEntry.setMinimum(0)
        self.discountEntry.setMaximum(1000)
        self.discountCurrency = QLabel("DTM")
        self.discountLayout.addWidget(self.discountEntry)
        self.discountLayout.addWidget(self.discountCurrency)
        # price
        self.priceLayout = QHBoxLayout()
        self.priceText = QLabel("price")
        self.priceEntry = QSpinBox()
        self.priceEntry.setValue(100)
        self.priceEntry.setMinimum(0)
        self.priceEntry.setMaximum(1000)
        self.priceCurrency = QLabel("DTM")
        self.priceLayout.addWidget(self.priceEntry)
        self.priceLayout.addWidget(self.priceCurrency)
        self.keyText = QLabel("Key")
        self.keyDisplay = QLabel()
        self.keyUpdateBtn = QPushButton("Update Key")
        self.keyUpdateBtn.clicked.connect(self.update_client_key)
        self.intervalText = QLabel("Interval")
        self.intervalEntry = QSpinBox()
        self.intervalEntry.setValue(30)
        self.intervalEntry.setMinimum(1)
        self.intervalEntry.setMaximum(366)
        self.penaltyText = QLabel("Penalty")
        self.penaltyEntry = QSpinBox()
        self.penaltyEntry.setValue(0)
        self.penaltyEntry.setMinimum(0)
        self.penaltyEntry.setMaximum(29)
        self.remainingText = QLabel("Remaining")
        self.remainingDisplay = QLabel()
        self.paidText = QLabel("Paid")
        self.paidEntry = QRadioButton()
        self.debtText = QLabel("Debt")
        self.debtDisplay = QLabel()
        self.statusText = QLabel("Status")
        self.statusDisplay = QLabel()
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.submit)

    def get_values(self):
        selected_client = self.parent.clientsTable.currentRow()
        try:
            self._id = self.parent.clientsTable.item(selected_client, 0).text()
            # print("Test: ", self._id)
            self._id = int(self._id)
            for c in self.parent.clients:
                if c['_id'] == self._id:
                    self.index = self.parent.clients.index(c)
                    break
            self.client = self.parent.clients[self.index]
            self.name = self.parent.clients[self.index]['name']
            self.phone = self.parent.clients[self.index]['phone']
            self.mail = self.parent.clients[self.index]['mail']
            self.device = self.parent.clients[self.index]['device']
            self.price = self.parent.clients[self.index]['price']
            self.discount = self.parent.clients[self.index]['discount']
            self.key = self.parent.clients[self.index]['key']
            self.server = self.parent.clients[self.index]['server']
            self.startDate = self.parent.clients[self.index]['startDate']
            self.interval = self.parent.clients[self.index]['interval']
            self.penalty = self.parent.clients[self.index]['penalty']
            self.remaining = self.parent.clients[self.index]['remaining']
            self.paid = self.parent.clients[self.index]['paid']
            self.status = self.parent.clients[self.index]['status']
            self.debt = self.parent.clients[self.index]['debt']

            ############ Setting Values #############
            self.nameEntry.setText(self.name)
            self.phoneEntry.setText(self.phone)
            self.mailEntry.setText(self.mail)
            self.deviceEntry.setValue(int(self.device))
            self.priceEntry.setValue(int(self.price))
            self.discountEntry.setValue(int(self.discount))
            ### Displaying servers
            self.servers = self.rd.read_servers()
            server_list = []
            for _ in self.servers:
                server_list += [i for i in _.keys()]
            self.serverEntry.addItem("None")
            for _ in server_list:
                self.serverEntry.addItem(_)
            
            if self.server:         
                self.serverEntry.setCurrentText(list(self.server.keys())[0])
            else:
                self.serverEntry.setCurrentText("None")
            ### Displaying Keys
            if self.key != None and self.key != []:
                number_of_keys = len(self.key) 
                self.keyDisplay.setText("You have {} active key(s).".format(number_of_keys))
            else:
                self.keyDisplay.setText("")
            self.intervalEntry.setValue(int(self.interval))
            self.penaltyEntry.setValue(int(self.penalty))
            self.remainingDisplay.setText(str(self.remaining))
            
            if self.paid:
                self.paidEntry.setChecked(True)
            else:
                self.paidEntry.setChecked(False)
            self.debtDisplay.setText("{} DTM".format(self.debt))
            if self.status:
                s_st = QPixmap("images/icons/server-running.png")
                s_st = s_st.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
                self.statusDisplay.setPixmap(s_st)
                self.statusDisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else:
                s_st = QPixmap("images/icons/server-stopped.png")
                s_st = s_st.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
                self.statusDisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.statusDisplay.setPixmap(s_st)
            
        except AttributeError as e:
            print("You have clicked wrong place")

    def update_client_key(self):
        server_name = self.serverEntry.currentText()
        self.uk = uk(self, server_name)
        self.update_key = self.uk.update_client_key(server_name)
        if self.update_key != None:
            self.update_key.show()

    # def update_client_key(self):
    #     self.server = self.selected_server()
    #     if self.server:
    #         self.key = "Test"  # get_client_key_from_server(name, server)
    #         self.keyDisplay.setText(self.key)
    #     else:
    #         self.key = None
    #         self.keyDisplay.setText("Please select the server from list..")
    
    # def selected_server(self):
    #     selected_server = self.serverEntry.currentText()
    #     if selected_server != "None":
    #         for item in self.servers:
    #             if list(item.keys())[0] == selected_server:
    #                 server_index = self.servers.index(item)
    #         selected_server = self.servers[server_index]
    #         return selected_server
    #     return None

    def submit(self):
        c = Client()
        c.id = self._id
        c.name = self.nameEntry.text()
        c.phone = self.phoneEntry.text()
        c.mail = self.mailEntry.text()
        c.device = self.deviceEntry.value()
        c.price = self.priceEntry.value()
        c.discount = self.discountEntry.value()
        c.server = self.uk.selected_server(self.serverEntry.currentText())
        c.key = self.key
        c.interval = self.intervalEntry.value()
        c.penalty = self.penaltyEntry.value()
        c.startDate = self.startDate
        if self.paidEntry.isChecked():
            c.paid = True
        else:
            c.paid = False
        e = Extensions()
        c.expireDate, c.remaining = e.remaining_calculate(self.startDate, c.interval, c.penalty)
        c.debt += e.debt_calculate(c.expireDate, c.device, c.price, c.discount, self.debt, c.paid)
        c.status = True
        
        self.clients = e._replace(self.parent.clients, self.index, c.to_dict())
        self.rd.write_clients(self.clients)
        self.message = QMessageBox.information(self, 
				"Congratulations", 
				"Client <b>{}</b> successfully updated!".format(c.name))
        self.parent.display_items()
        self.close()
        
        # c = Client()
        # c.name = self.nameEntry.text()

    
    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topMainLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        ########## Top Layout Widgets ####################
        self.topMainLayout.addWidget(self.clientImg)
        self.topMainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ########### Bottom Layout Widgets ################
        self.bottomLayout.addRow(self.nameText, self.nameEntry)
        self.bottomLayout.addRow(self.phoneText, self.phoneEntry)
        self.bottomLayout.addRow(self.mailText, self.mailEntry)
        self.bottomLayout.addRow(self.deviceText, self.deviceEntry)
        self.bottomLayout.addRow(self.priceText, self.priceLayout)
        self.bottomLayout.addRow(self.discountText, self.discountLayout)
        self.bottomLayout.addRow(self.serverText, self.serverEntry)
        self.bottomLayout.addRow(self.keyText, self.keyDisplay)
        self.bottomLayout.addRow(QLabel(), self.keyUpdateBtn)
        self.bottomLayout.addRow(self.intervalText, self.intervalEntry)
        self.bottomLayout.addRow(self.penaltyText, self.penaltyEntry)
        self.bottomLayout.addRow(self.remainingText, self.remainingDisplay)
        self.bottomLayout.addRow(self.paidText, self.paidEntry)
        self.bottomLayout.addRow(self.debtText, self.debtDisplay)
        self.bottomLayout.addRow(self.statusText, self.statusDisplay)

        ################ Adding Layout to Main Layout #########
        self.mainLayout.addLayout(self.topMainLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.submitBtn)

        self.setLayout(self.mainLayout)


# def main():
#     app = QApplication(sys.argv)
#     window = UpdateClient()
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()