from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt

import sys
import json
from actions.recorddata import RecordData as rd


class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.rd = rd()
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon("images/icons/settings.png"))
        self.setGeometry(200, 200,  350, 250)
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.logic()
        self.layouts()
    
    def widgets(self):
        self.emailText = QLabel("Email Address")
        self.emailEntry = QLineEdit()
        self.passwordText = QLabel("Password")
        self.passwordEntry = QLineEdit()
        self.passwordEntry.setEchoMode(QLineEdit.EchoMode.Password)
        self.save = QPushButton("Save")
        self.save.clicked.connect(self.funcSave)

    def logic(self):
        self.config = self.rd.read_settings()
        self.emailEntry.setText(self.config['email'])
        self.passwordEntry.setText(self.config['password'])


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.mainGroupBox = QGroupBox("Settings")

        self.mainTopLayout = QGridLayout()
        
        self.mainTopGroupBox = QGroupBox('Mail Settings')
        self.mainLayout.addWidget(self.mainTopGroupBox)

        self.mainTopLayout.addWidget(self.emailText, 0, 0)
        self.mainTopLayout.addWidget(self.emailEntry, 0, 1)
        self.mainTopLayout.addWidget(self.passwordText, 1, 0)
        self.mainTopLayout.addWidget(self.passwordEntry, 1, 1)
        self.mainTopLayout.addWidget(self.save, 2, 0, 1, 2)
        self.mainTopLayout.setRowStretch(0, 1)
        self.mainTopGroupBox.setLayout(self.mainTopLayout)
        self.mainGroupBox.setLayout(self.mainLayout)

        self.setLayout(self.mainLayout)
    
    def funcSave(self):
        self.config['email'] = self.emailEntry.text()
        self.config['password'] = self.passwordEntry.text()
        self.message = QMessageBox.information(
            self,
            "Information",
            "Are you sure all the information is correct",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if self.message == QMessageBox.StandardButton.Yes:
            self.rd.write_settings(self.config)
            self.close()
        print(self.config)

# def main():
#     app = QApplication(sys.argv)
#     window = Settings()
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()
