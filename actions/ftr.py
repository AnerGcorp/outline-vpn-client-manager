
class Filter:
    def __init__(self, parent):
        self.parent = parent
        self.logic()

    def logic(self):
        self.clients = self.parent.clients
        self.intervalMin= self.parent.intervalMinEntry.value()
        self.intervalMax = self.parent.intervalMaxEntry.value()
        self.penaltyMin = self.parent.penaltyMinEntry.value()
        self.penaltyMax = self.parent.penaltyMaxEntry.value()
        self.remainingMin = self.parent.remainingMinEntry.value()
        self.remainingMax = self.parent.remainingMaxEntry.value()
        if self.parent.statusYes.isChecked():
            self.status = True
        elif self.parent.statusNo.isChecked():
            self.status = False
        else:
            self.status = None

        clients = []
        clients = list(filter(self._filter_interval, self.clients))
        clients = list(filter(self._filter_penalty, clients))
        clients = list(filter(self._filter_remaining, clients))
        clients = list(filter(self._filter_status, clients))
        self.parent.display_items(clients)

    def _filter_interval(self, client):
        if client['interval'] >= self.intervalMin and client['interval'] <= self.intervalMax:
            return True
        else:
            return False

    def _filter_penalty(self, client):
        if client['penalty'] >= self.penaltyMin and client['penalty'] <= self.penaltyMax:
            return True
        else:
            return False

    def _filter_remaining(self, client):
        if client['remaining'] >= self.remainingMin and client['remaining'] <= self.remainingMax:
            return True
        else:
            return False
    
    def _filter_status(self, client):
        if client['status'] == True or client['status'] == None:
            return True
        else:
            return False
        

        

        
