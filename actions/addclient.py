from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

from datetime import datetime, timedelta
import sys
import json
from actions.client_object import Client
from actions.recorddata import RecordData as rd
from actions.extensions import Extensions as ext

class AddClient(QWidget):
	def __init__(self, parent):
		super().__init__()
		self.parent = parent
		self.rd = rd()
		self.ext = ext()
		self.setWindowTitle("Add Client to Database")
		self.setWindowIcon(QIcon("images/icons/add-user.png"))
		self.setGeometry(450, 150, 350, 550)
		self.setFixedSize(self.size())
		self.UI()
		self.show()


	def UI(self):
		self.widgets()
		self.layouts()

	def widgets(self):
		############# Widgets of top Layout #########
		self.addClientImg = QLabel()
		self.img = QPixmap("images/icons/octopus.png")
		self.addClientImg.setPixmap(self.img)
		self.titleText = QLabel("Add Client")
		############# Widgets of bottom Layout ######
		self.nameEntry = QLineEdit()
		self.nameEntry.setPlaceholderText("Enter the name of client..")
		self.phoneEntry = QLineEdit()
		self.phoneEntry.setPlaceholderText("+993 65 12-34-56")
		self.mailEntry = QLineEdit()
		self.mailEntry.setPlaceholderText("Enter the mail address..")
		self.deviceEntry = QSpinBox()
		self.deviceEntry.setValue(1)
		self.deviceEntry.setMinimum(1)
		self.deviceEntry.setMaximum(30)
		# layout for displaying price
		self.priceLayout = QHBoxLayout()
		self.priceEntry = QSpinBox()
		self.priceEntry.setValue(101)
		self.priceEntry.setMinimum(0)
		self.priceEntry.setMaximum(1000)
		self.priceCurrency = QLabel("DTM")
		self.priceLayout.addWidget(self.priceEntry)
		self.priceLayout.addWidget(self.priceCurrency)
		self.submitBtn = QPushButton("Submit")
		self.submitBtn.clicked.connect(self.create_user)

	def layouts(self):
		self.mainLayout = QVBoxLayout()
		self.topLayout = QVBoxLayout()
		self.bottomLayout = QFormLayout()
		# self.topFrame = QFrame()
		# self.bottomFrame = QFrame()
		########## Adding widgets ##########
		############ Widgets of top layout #####
		self.topLayout.addWidget(self.addClientImg)
		# self.topLayout.addWidget(self.titleText)
		self.topLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		# self.topFrame.setLayout(self.topLayout)

		########### widgets of form layout ######
		self.bottomLayout.addRow(QLabel("Name:  "), self.nameEntry)
		self.bottomLayout.addRow(QLabel("Phone Number:  "), self.phoneEntry)
		self.bottomLayout.addRow(QLabel("Mail Address:  "), self.mailEntry)
		self.bottomLayout.addRow(QLabel("Number of Devices"), self.deviceEntry)
		self.bottomLayout.addRow(QLabel("Price"), self.priceLayout)
		# self.bottomLayout.addRow(QLabel(), self.submitBtn)
		# self.bottomFrame.setLayout(self.bottomLayout)
		# self.mainLayout.addLayout(self.topFrame)
		# self.mainLayout.addLayout(self.bottomFrame)
		self.mainLayout.addLayout(self.topLayout)
		self.mainLayout.addLayout(self.bottomLayout)
		self.mainLayout.addWidget(self.submitBtn)
		self.setLayout(self.mainLayout)

	def create_user(self):
		clients = self.rd.read_clients()
		c = Client()
		if len(clients) != 0:
			_id = clients[-1]['_id']
			_id += 1
		else:
			_id = 0
		c.id = _id
		c.name = self.nameEntry.text()
		c.phone = self.phoneEntry.text()
		phoneAccept = self.ext.validate_phone(c.phone)
		c.mail = self.mailEntry.text()
		mailAccept = self.ext.validate_email(c.mail)
		c.device = self.deviceEntry.value()
		c.price = self.priceEntry.value()
		c.startDate = datetime.now().strftime("%H:%M %d/%m/%y")

		if not phoneAccept:
			self.message = QMessageBox.warning(self, 
				"WARNING", 
				"Please correct your phone number")
			self.phoneEntry.clear()
			self.phoneEntry.setFocus()
		if not mailAccept:
			self.message = QMessageBox.warning(self, 
				"WARNING", 
				"Please correct your mail address")
			self.mailEntry.clear()
			self.mailEntry.setFocus()

		if c.name == "" or c.phone == "" or c.mail == "":
			print("There is blank space")
			self.message = QMessageBox.information(self, 
				"Information Box", 
				"Please fill all the  blanks with correct information")
			if self.message.Ok:
				print("Some of the fields are empty!")
		elif not phoneAccept or not mailAccept:
			self.message = QMessageBox.information(self, 
				"Information", 
				"Please check the information you entered")
		else:
			self.message = QMessageBox.information(self, 
				"Congratulations", 
				"New Client is successfully created!")
			if self.message:
				clients.append(c.to_dict())
				self.rd.write_clients(clients)
				
				self.parent.display_items()
				self.close()

# def main():
#     app = QApplication(sys.argv)
#     window = AddClient()
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()