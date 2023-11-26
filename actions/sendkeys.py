from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys

from actions.recorddata import RecordData as rd
from actions.extensions import Extensions as ext
from actions.sendtomail import Gmail

header = "Thanks for using our service...\n\n"
footer = "\n\nIf you have any question please write directly to this email"

class SendKeys(QWidget):
    def __init__(self):
        super().__init__()
        self.rd = rd()
        self.ext = ext()
        self.setWindowTitle("SendKeys")
        self.setWindowIcon(QIcon('images/icons/send-keys.png'))
        self.setGeometry(200, 200, 600, 800)

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.logic()
        self.layouts()

    def widgets(self):
        self.send = QPushButton("Send")
        self.statusFailed = QLabel()
        self.statusSuccess = QLabel()
        self.headerMsgText = QLabel("Header")
        self.headerMsgEntry = QPlainTextEdit()
        self.headerMsgEntry.setFixedHeight(120)
        self.headerMsgEntry.setPlainText(header)
        self.footerMsgText = QLabel("Footer")
        self.footerMsgEntry = QPlainTextEdit()
        self.footerMsgEntry.setFixedHeight(120)
        self.footerMsgEntry.setPlainText(footer)
        self.statusProgress = QProgressBar()
        self.listSentStatus = QListWidget()

    def logic(self):
        self.clients = self.rd.read_clients()
        self.keys = self.rd.read_keys()
        keys = []
        # config
        self.success = 0
        self.failed = 0
        self.total = len(self.clients)
        self.start = 0
        self.counter = 1

        self.statusProgress.setRange(self.start, self.total)
        clientKeyIds = [_["_id"] for _ in self.keys]
        if len(self.keys) > 0:
            # add new clients key
            for client in self.clients:
                clientKey = dict()
                if client['_id'] not in clientKeyIds:
                    clientKey["_id"] = client["_id"]
                    clientKey["name"] = client["name"]
                    clientKey["key"] = client["key"]
                    clientKey['mail'] = client['mail']
                    clientKey['device'] = client['device']
                    clientKey["isSent"] = False
                    keys.append(clientKey)
                else:
                    for key in self.keys:
                        if client["_id"] == key["_id"]:
                            index = self.keys.index(key)
                            if client['key'] == self.keys[index]['key']:
                                key["isSent"] = True
                            else:
                                key['isSent'] = False
                            keys.append(key)
        else:
            for client in self.clients:
                clientKey = dict()
                if client['_id'] not in clientKeyIds:
                    clientKey["_id"] = client["_id"]
                    clientKey["name"] = client["name"]
                    clientKey["key"] = client["key"]
                    clientKey['mail'] = client['mail']
                    clientKey['device'] = client['device']
                    clientKey["isSent"] = False
                    keys.append(clientKey)
            self.rd.write_keys(keys)

    def layouts(self):
        self.send.clicked.connect(self.funcSendBtn)
        self.mainLayout = QVBoxLayout()
        self.mainTopLayout = QHBoxLayout()
        self.mainMiddleLayout = QGridLayout()
        
        self.mainMiddleLayout.addWidget(self.headerMsgText, 0, 0)
        self.mainMiddleLayout.addWidget(self.headerMsgEntry, 0, 1)
        self.mainMiddleLayout.addWidget(self.footerMsgText, 1, 0)
        self.mainMiddleLayout.addWidget(self.footerMsgEntry, 1, 1)
        self.mainMiddleLayout.addWidget(self.statusSuccess, 2, 0)
        self.mainMiddleLayout.addWidget(self.statusFailed, 2, 1)
        self.mainBottomLayout = QHBoxLayout()

        self.mainTopLayout.addWidget(self.send)
        self.mainTopLayout.addWidget(self.statusProgress)

        self.mainBottomLayout.addWidget(self.listSentStatus)
        self.mainLayout.addLayout(self.mainTopLayout)
        self.mainLayout.addLayout(self.mainMiddleLayout)
        self.mainLayout.addLayout(self.mainBottomLayout)

        self.setLayout(self.mainLayout)

    def messageCreate(name, key):
        message = ""
        if device <= 1:
            message += "{0} \n{1}".format(name, key[0])
            return message
        else:
            for device in range(len(devices)):
                message += "\n{0} device {1} \n {2}\n".format(name, device+1, key[device])
            return message

    def funcSendBtn(self):
        if not self.ext.is_pingable("google.ru"):
            self.message = QMessageBox.warning(
                self,
                "Connection Lost",
                "You don't have internet connection, please connect the internet first"
            )
            self.close()
            return
        self.keys = self.rd.read_keys()
        self.config = self.rd.read_settings()
        self.header = self.headerMsgEntry.toPlainText()
        self.footer = self.footerMsgEntry.toPlainText()
        self.listSentStatus.addItem("Name\t\t e-Mail\t Device\t\t Status\t\t Completed")
        for key in self.keys:
            self.counter += 1
            self.statusProgress.setValue(self.counter)
            
            if key['key'] == []:
                self.failed += 1
                self.statusFailed.setText(str(self.failed))
                self.listSentStatus.addItem("{0}\t\t {1}\t {2}\t\t {3}\t\t Done".format(key['name'], key['mail'], len(key['key'])+1, key['isSent']))
                continue
            
            elif key['isSent'] == False:
                message = self.header + ""
                cust = self.messageCreate(msg["name"], msg['key'])
                message += cust
                message += self.footer
                self.email = Gmail(self.config['email'], self.config['password'])
                self.email.draft(key['mail'], message)
                self.email.send()
                self.email.quit()
                key['isSent'] = True
                self.success += 1
                self.statusSuccess.setText(str(self.succes))
                self.listSentStatus.addItem("{0}\t\t {1}\t {2}\t\t {3}\t\t Done".format(key['name'], key['mail'], len(key['key'])+1, key['isSent']))
            else:
                self.failed += 1
                self.statusFailed.setText(str(self.failed))
                self.listSentStatus.addItem("{0}\t\t {1}\t {2}\t\t {3}\t\t Done".format(key['name'], key['mail'], len(key['key'])+1, key['isSent']))   
        
        self.send.setDisabled(True)

# def main():
#     app = QApplication(sys.argv)
#     window = SendKeys()
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()
