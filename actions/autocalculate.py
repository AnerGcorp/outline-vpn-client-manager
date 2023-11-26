from actions.extensions import Extensions as ext
from actions.recorddata import RecordData as rd
# from extensions import Extensions as ext
# from recorddata import RecordData as rd


class AutoCalculate:
    def __init__(self, parent=None):
        self.parent = parent
        self.ext = ext()
        self.rd = rd()

    def check_connection(self):
        result = self.ext.is_pingable("google.ru")
        return result

    def calculate(self):
        self.clients = self.rd.read_clients()
        clients = []
        for client in self.clients:
            client['startDate'], client['interval'], client['penalty'] = self.ext.remaining_calculate(
                client['startDate'], client['interval'], client['penalty'])
            client['debt'] = ext.debt_calculate(client["expireDate"], client["device"], client["price"], client['discount'], client["debt"], client["paid"])
            if self.check_connection():
                ip = self.ext.ip_extractor(client["server"])
                client["status"] = self.ext.is_pingable(ip)
            clients.append(client)
        self.rd.write_clients(clients)
        if self.parent != None:
            self.parent.display_items()

        self.servers = self.rd.read_servers()
        servers = []
        for server in self.servers:
            ip = self.ext.ip_extractor(server)
            if self.check_connection():
                ip = self.ext.ip_extractor(server)
                server["status"] = self.ext.is_pingable(ip)
            servers.append(server)
        self.rd.write_servers(servers)
        if self.parent != None:
            self.parent.display_servers()
            