from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

from datetime import datetime, timedelta
import sys
from actions.recorddata import RecordData as rd

class RemoveClient(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowIcon(QIcon("images/icons/remove-user.png"))

        self.parent = parent

        selected_client = self.parent.clientsTable.currentRow()
        try:
            _id = self.parent.clientsTable.item(selected_client, 0).text()
            _id = int(_id)
            for c in self.parent.clients:
                if c['_id'] == _id:
                    index = self.parent.clients.index(c)
                    break
            self.message = QMessageBox.information(
                self, 
                "Remove Client",
                "Do you really want to delete <b>{}</b> client from database?".format(c['name']), 
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            # print(QMessageBox.StandartButton.No)
            
            if self.message == QMessageBox.StandardButton.Yes:
                del self.parent.clients[index]
                _rd = rd()
                _rd.write_clients(self.parent.clients)
                self.parent.display_items()
                
            
        except AttributeError as e:
            self.message = QMessageBox.information(
                self, 
                "Remove Client",
                "No Client selected for remove")
            print("You have clicked wrong place..")