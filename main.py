import sys
from PyQt6.QtWidgets import \
    QApplication, QMainWindow, QWidget, QTabWidget, \
    QHBoxLayout, QVBoxLayout, QGroupBox, QTabWidget, \
    QTableWidget, QTableWidgetItem, QLabel, QLineEdit, \
    QPushButton, QSpinBox, QRadioButton, QGridLayout, \
    QHeaderView, QMessageBox, QSystemTrayIcon, QMenu
        
from PyQt6.QtGui import QIcon, QAction, QFont
from PyQt6.QtCore import Qt, QSize, QTimer, QCoreApplication
import json
from actions import addclient, removeclient, \
    updateclient, updatekey, updateclient, \
    addserver, updatekeys as uks, checkservers, \
    sendkeys as sdk, settings, recorddata as rd, \
    search, ftr, extensions as ext, autocalculate as ac

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QOut Client Manager")
        self.setGeometry(70, 70, 1280, 720)
        self.setWindowIcon(QIcon("images/icons/app-icon.png"))
        self.rd = rd.RecordData()
        self.ext = ext.Extensions()
        
        self.UI()

    def UI(self):
        self.toolBar()
        self.tabWidget()
        self.widgets()
        self.layouts()
        self.display_items()
        self.display_servers()

        # updating table items
        self.timer_status = QTimer()
        self.timer_status.timeout.connect(self.funcAuto)
        # check every half-second
        self.timer_status.start(1000*4*60*5)


    def toolBar(self):
        self.tb = self.addToolBar("ToolBar")
        self.tb.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.tb.setIconSize(QSize(64, 64))

        ######################## ToolBar Buttons ############################
        ######################### Add Client ###############################
        self.addClient = QAction(QIcon("images/icons/add-user.png"), 'Add Client', self)
        self.tb.addAction(self.addClient)
        self.tb.addSeparator()
        self.addClient.triggered.connect(self.funcAddClient)
        ######################## Remove Client ##########################
        self.removeClient = QAction(QIcon("images/icons/remove-user.png"), 'Remove Client', self)
        self.tb.addAction(self.removeClient)
        self.tb.addSeparator()
        self.removeClient.triggered.connect(self.funcRemoveClient)
        ######################### Update Key ############################
        self.updateKey = QAction(QIcon("images/icons/update-key"), 'Update Key', self)
        self.tb.addAction(self.updateKey)
        self.tb.addSeparator()
        self.updateKey.triggered.connect(self.funcUpdateKey)
        ######################### Update Keys ############################
        self.updateKeys = QAction(QIcon("images/icons/update-key"), 'Update Keys', self)
        self.tb.addAction(self.updateKeys)
        self.tb.addSeparator()
        self.updateKeys.triggered.connect(self.funcUpdateKeys)
        ######################### Update Client ############################
        self.updateClient = QAction(QIcon("images/icons/update-user.png"), 'Update Client', self)
        self.tb.addAction(self.updateClient)
        self.tb.addSeparator()
        self.updateClient.triggered.connect(self.funcUpdateClient)
        ######################## Send Keys ##############################
        self.sendKeys = QAction(QIcon('images/icons/send-keys.png'), 'Send Keys', self)
        self.tb.addAction(self.sendKeys)
        self.tb.addSeparator()
        self.sendKeys.triggered.connect(self.funcSendKeys)
        ######################## Search Servers ##############################
        self.checkServers = QAction(QIcon("images/icons/server-search.png"), 'Check Servers', self)
        self.tb.addAction(self.checkServers)
        self.tb.addSeparator()
        self.checkServers.triggered.connect(self.funcCheckServers)
        ######################## Add Server ##############################
        self.addServer = QAction(QIcon("images/icons/add-server.png"), 'Add Server', self)
        self.tb.addAction(self.addServer)
        self.tb.addSeparator()
        self.addServer.triggered.connect(self.funcAddServer)
         ######################## Check Status ##############################
        # self.addServer = QAction(QIcon("images/icons/bluetooth.png"), 'Check Status', self)
        # self.tb.addAction(self.addServer)
        # self.tb.addSeparator()
        ######################## Settings ##############################
        self.settings = QAction(QIcon("images/icons/settings.png"), 'Settings', self)
        self.tb.addAction(self.settings)
        self.tb.addSeparator()
        self.settings.triggered.connect(self.funcSettings)


        
    def tabWidget(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        # self.tab2 = QWidget()
        self.tabs.addTab(self.tab1, QIcon("images/icons/clients.png"), "Clients")
        self.tabs.addTab(self.tab2, QIcon("images/icons/servers.png"), "Servers")
        # self.tabs.addTab(self.tab2, QIcon("images/icons/octopus.png"), "Servers")

    def widgets(self):
        ################### Tab1 Widgets ############################
        ################### Main Left Layout Widgets ##################
        self.clientsTable = QTableWidget()
        self.clientsTable.setColumnCount(17)
        self.clientsTable.setColumnHidden(0, True)
        self.clientsTable.setColumnHidden(3, True)
        self.clientsTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.clientsTable.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
        self.clientsTable.setHorizontalHeaderItem(2, QTableWidgetItem("Phone"))
        self.clientsTable.setHorizontalHeaderItem(3, QTableWidgetItem("Mail"))
        self.clientsTable.setHorizontalHeaderItem(4, QTableWidgetItem("Devices #"))
        self.clientsTable.setHorizontalHeaderItem(5, QTableWidgetItem("Price"))
        self.clientsTable.setHorizontalHeaderItem(6, QTableWidgetItem("Discount"))
        self.clientsTable.setHorizontalHeaderItem(7, QTableWidgetItem("Key"))
        self.clientsTable.setHorizontalHeaderItem(8, QTableWidgetItem("Server"))
        self.clientsTable.setHorizontalHeaderItem(9, QTableWidgetItem("Start Date"))
        self.clientsTable.setHorizontalHeaderItem(10, QTableWidgetItem("Expire Date"))
        self.clientsTable.setHorizontalHeaderItem(11, QTableWidgetItem("Interval"))
        self.clientsTable.setHorizontalHeaderItem(12, QTableWidgetItem("Penalty"))
        self.clientsTable.setHorizontalHeaderItem(13, QTableWidgetItem("Remaining"))
        self.clientsTable.setHorizontalHeaderItem(14, QTableWidgetItem("Paid"))
        self.clientsTable.setHorizontalHeaderItem(15, QTableWidgetItem("Debt"))
        self.clientsTable.setHorizontalHeaderItem(16, QTableWidgetItem("Status"))

        # Resizing for clear view
        self.clientsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.clientsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.clientsTable.itemDoubleClicked.connect(self.funcUpdateClient)

        ####################### Servers Table ##################################
        self.serversTable = QTableWidget()
        self.serversTable.setColumnCount(3)
        self.serversTable.setHorizontalHeaderItem(0, QTableWidgetItem("Server Name"))
        self.serversTable.setHorizontalHeaderItem(1, QTableWidgetItem("Server IP"))
        self.serversTable.setHorizontalHeaderItem(2, QTableWidgetItem("Status"))
        # Resizing for clear view
        self.serversTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.serversTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)


        #################### Main Right Layout Widgets #########################
        # Searching...
        # self.searchText = QLabel("Search")
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Search..")
        self.searchEntry.textChanged.connect(self.funcSearch)
        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.funcSearch)

        # Filtering
        self.intervalText = QLabel("Interval")
        self.intervalMinText = QLabel("Min")
        self.intervalMaxText = QLabel("Max")
        self.intervalMaxEntry = QSpinBox()
        self.intervalMaxEntry.setMinimum(0)
        self.intervalMaxEntry.setMaximum(736)
        self.intervalMinEntry = QSpinBox()
        self.intervalMinEntry.setMinimum(0)
        self.intervalMinEntry.setMaximum(736)

        self.penaltyText = QLabel("Penalty")
        self.penaltyMaxText = QLabel("Max")
        self.penaltyMinText = QLabel("Min")
        self.penaltyMinEntry = QSpinBox()
        self.penaltyMaxEntry = QSpinBox()
        self.penaltyMinEntry.setMinimum(0)
        self.penaltyMinEntry.setMaximum(25)
        self.penaltyMaxEntry.setMinimum(0)
        self.penaltyMaxEntry.setMaximum(25)
        
        self.remainingText = QLabel("Remaining")
        self.remainingMaxText = QLabel("Max")
        self.remainingMinText = QLabel("Min")
        self.remainingMinEntry = QSpinBox()
        self.remainingMinEntry.setMinimum(0)
        self.remainingMinEntry.setMaximum(735)
        self.remainingMaxEntry = QSpinBox()
        self.remainingMaxEntry.setMinimum(0)
        self.remainingMaxEntry.setMaximum(735)

        self.statusText = QLabel("Server Status")
        self.statusYes = QRadioButton("Running..")
        self.statusNo = QRadioButton("Stopped")
        self.filterButton = QPushButton("Filter")
        self.filterButton.clicked.connect(self.funcFilter)
        self.clearFilterBtn = QPushButton("Clear Filter")
        self.clearFilterBtn.clicked.connect(self.funcClearFilterBtn)

    def layouts(self):
        ############### Tab1 Layouts #################################
        self.mainLayout = QHBoxLayout()
        self.mainLeftLayout = QVBoxLayout()
        self.mainRightLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightMiddleLayout = QGridLayout()
        self.topGroupBox = QGroupBox("Search Box")
        self.middleGroupBox = QGroupBox("Filter Items")

        ############## Main Left Layout ###################################
        self.mainLeftLayout.addWidget(self.clientsTable)
        ################# Right Top Layout #########################
        self.mainLayout.addLayout(self.mainLeftLayout, 80)
        self.mainLayout.addLayout(self.mainRightLayout, 20)
        # self.rightTopLayout.addWidget(self.searchText)
        self.mainRightLayout.addWidget(self.topGroupBox)
        self.rightTopLayout.addWidget(self.searchEntry)
        # self.rightTopLayout.addStretch(1)
        self.topGroupBox.setFixedHeight(200)
        self.rightTopLayout.addWidget(self.searchButton)
        self.topGroupBox.setLayout(self.rightTopLayout)
        # Filtering
        self.mainRightLayout.addWidget(self.middleGroupBox)
        ## Interval 
        self.rightMiddleLayout.addWidget(self.intervalText, 0, 0, 1, 4)
        self.rightMiddleLayout.addWidget(self.intervalMinText, 1, 0)
        self.rightMiddleLayout.addWidget(self.intervalMinEntry, 1, 1)
        self.rightMiddleLayout.addWidget(self.intervalMaxText, 1, 2)
        self.rightMiddleLayout.addWidget(self.intervalMaxEntry, 1, 3)
        ## Penalty
        self.rightMiddleLayout.addWidget(self.penaltyText, 2, 0, 1, 4)
        self.rightMiddleLayout.addWidget(self.penaltyMinText, 3, 0)
        self.rightMiddleLayout.addWidget(self.penaltyMinEntry, 3, 1)
        self.rightMiddleLayout.addWidget(self.penaltyMaxText, 3, 2)
        self.rightMiddleLayout.addWidget(self.penaltyMaxEntry, 3, 3)
        ## Remaining
        self.rightMiddleLayout.addWidget(self.remainingText, 4, 0, 1, 4)
        self.rightMiddleLayout.addWidget(self.remainingMinText, 5, 0)
        self.rightMiddleLayout.addWidget(self.remainingMinEntry, 5, 1)
        self.rightMiddleLayout.addWidget(self.remainingMaxText, 5, 2)
        self.rightMiddleLayout.addWidget(self.remainingMaxEntry, 5, 3)
        ## Server Status
        self.rightMiddleLayout.addWidget(self.statusText, 6, 0, 1, 1)
        self.rightMiddleLayout.addWidget(self.statusYes, 7, 0, 2, 1)
        self.rightMiddleLayout.addWidget(self.statusNo, 7, 1, 2, 1)
        self.rightMiddleLayout.addWidget(self.filterButton, 8, 0, 1, 1)
        self.rightMiddleLayout.addWidget(self.clearFilterBtn, 8, 1, 1, 1)

        self.middleGroupBox.setLayout(self.rightMiddleLayout)

        self.mainRightLayout.addLayout(self.rightMiddleLayout, 90)
        self.mainRightLayout.addLayout(self.rightTopLayout, 10)

        self.tab1.setLayout(self.mainLayout)

        #### Tab 2 Layout ##########
        self.serversMainLayout = QHBoxLayout()
        self.serversMainLayout.addWidget(self.serversTable)
        self.tab2.setLayout(self.serversMainLayout)

    def display_items(self, outside=None):
        self.clientsTable.setFont(QFont("Arial", 12))
        for i in reversed(range(self.clientsTable.rowCount())):
            self.clientsTable.removeRow(i)
        if outside == None:
            self.clients = self.rd.read_clients()
        else:
            self.clients = outside

        if self.clients:
            for c in self.clients:
                row_num = self.clientsTable.rowCount()
                self.clientsTable.insertRow(row_num)
                for col_num, data in enumerate(c.values()):
                    if data == None:
                        self.clientsTable.setItem(row_num, col_num, QTableWidgetItem(""))
                        continue
                    self.clientsTable.setItem(row_num, col_num, QTableWidgetItem(str(data)))

        self.clientsTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def display_servers(self):
        self.serversTable.setFont(QFont("Arial", 12))
        for i in reversed(range(self.serversTable.rowCount())):
            self.serversTable.removeRow(i)

        self.servers = self.rd.read_servers()
        if self.servers:
            for s in self.servers:
                row_num = self.serversTable.rowCount()
                self.serversTable.insertRow(row_num)
                name = list(s.keys())[0]
                serverObj = s[name]
                serverUrl = serverObj["apiUrl"]
                ip = serverUrl[8:].split(":")[0]
                try:
                    status = s['status']
                except KeyError as e:
                    status = False
                ser = {"name": name, "ip": ip, "status": status}
                for col_num, data in enumerate(ser.values()):
                    if data == None:
                        self.serversTable.setItem(row_num, col_num, QTableWidgetItem(""))
                        continue
                    self.serversTable.setItem(row_num, col_num, QTableWidgetItem(str(data)))

        self.serversTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def funcAddClient(self):
        self.add_client = addclient.AddClient(self)
        
        
    def funcRemoveClient(self):
        _id = self.clientsTable.currentRow()
        if _id != -1:
            self.remove_client = removeclient.RemoveClient(self)
        else:
            self.message = QMessageBox.information(
                self,
                "Information",
                "Please select the client first!"
                )

    def funcUpdateKey(self):
        _id = self.clientsTable.currentRow()
        if _id != -1:
            self.update_key = updatekey.UpdateKey(self)
            self.update_key.show()
        else:
            self.message = QMessageBox.information(
                self,
                "Information",
                "Please select the client first!"
                )

    def funcUpdateKeys(self):
        self.update_keys = uks.UpdateKeys(self)
    
    def funcUpdateClient(self):
        _id = self.clientsTable.currentRow()
        if _id != -1:
            self.update_client = updateclient.UpdateClient(self)
        else:
            self.message = QMessageBox.information(
                self,
                "Information",
                "Please select the client first!"
                )

    def funcAddServer(self):
        self.addServer = addserver.AddServer(self)
    
    def funcCheckServers(self):
        self.checkServer = checkservers.CheckServers(self)

    def funcSendKeys(self):
        self.sdk = sdk.SendKeys()

    def funcSettings(self):
        self.sett = settings.Settings()

    def funcSearch(self):
        self.search = search.Search(self)

    def funcFilter(self):
        self.filter = ftr.Filter(self)
        self.clearFilterBtn.setDisabled(False)
    
    def funcClearFilterBtn(self):
        self.display_items()
        self.clearFilterBtn.setDisabled(True)

    def funcAuto(self):
        self.automated = ac.AutoCalculate(self)
        self.automated.calculate()

    def selected_client(self):
        self.update_client = updateclient.UpdateClient(self)

    def close(self, event):
        self.hide()
    
class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        menu = QMenu(parent)
        exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)
        exitAction.triggered.connect(self.exit)
    
    def exit(self):
        QCoreApplication.exit()


def main():
    app = QApplication(sys.argv)
    window = Window()
    # window.setQuitOnLastWindowClosed(False)
    window.show()
    # sys.exit(app.exec())

    # app = QApplication(sys.argv)
    # w = QWidget()
    trayIcon = SystemTrayIcon(QIcon("images/icons/app-icon.png"), window)
    trayIcon.show()
    # sys.exit(app.exec())
    app.exec()

if __name__ == "__main__":
    main()