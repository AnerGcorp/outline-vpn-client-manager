import json
import re
from actions.recorddata import RecordData as rd

class Search:
    def __init__(self, parent):
        self.parent = parent
        self.rd = rd()
        self.logic()
    
    def logic(self):
        self.search = self.parent.searchEntry.text()
        self.search = self.search.lower()
        self.clients = self.rd.read_clients()
        customClients = []
        for client in self.clients:
            if re.match(self.search, client['name'].lower()):
                customClients.append(client)

        self.parent.display_items(customClients)