import json

class RecordData:
    def __init__(self):
        pass

    def read_clients(self):
        with open('actions/database/clients.json', 'r') as file:
            self.clients = json.load(file)
        return self.clients

    def read_servers(self):
        with open('actions/database/servers.json', 'r') as file:
            self.servers = json.load(file)
        return self.servers

    def write_clients(self, clients):
        with open("actions/database/clients.json", "w") as file:
            json.dump(clients, file, indent=2)
    
    def write_servers(self, servers):
        with open("actions/database/servers.json", "w") as file:
            json.dump(servers, file, indent=2)

    def read_settings(self):
        with open('actions/database/config.json', 'r') as file:
            self.config = json.load(file)
        return self.config
    
    def write_settings(self, config):
        with open("actions/database/config.json", "w") as file:
            json.dump(config, file, indent=2)

    def read_keys(self):
        with open('actions/database/sharekeys.json', 'r') as file:
            self.keys = json.load(file)
        return self.keys
    
    def write_keys(self, keys):
        with open("actions/database/sharekeys.json", "w") as file:
            json.dump(keys, file, indent=2)

    

    
    
    

    

    