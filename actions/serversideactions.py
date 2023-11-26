from actions.outline import Outline
import json


class SActions:
    def __init__(self):
        self.out = Outline()

    def get_client_keys(self, server, name, device=1):
        keys = []
        if device >= 0 and device <= 1:
            key = self.__get_key(server, name)
            if key:
                keys.append(key)
        else:
            for num in range(device):
                nickname = "{0} device {1}".format(name, num + 1)
                key = self.__get_key(server, nickname)
                if key:
                    keys.append(key)
        return keys

    def __get_key(self, server, name):
        result = self.out.adduser(server, username=name)
        if result != None:
            data = json.loads(result.text)

            key = data['accessUrl']
            client_id = data['id']
            return key
        return None