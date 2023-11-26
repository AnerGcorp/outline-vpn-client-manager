from datetime import datetime, timedelta
import json
import re
import os
import subprocess
from dateutil import parser

class Extensions:
    def __init__(self):
        pass
    
    def remaining_calculate(self, startDate, interval, penalty):
        self.today = datetime.now()
        interval = interval + penalty
        startDate = parser.parse(startDate)
        expireDate = startDate + timedelta(days=interval)
        remaining = expireDate - self.today
        expireDate = expireDate.strftime("%H:%M %d/%m/%y")
        return expireDate, remaining.days
    
    def debt_calculate(self, expireDate, device, price, discount, debt, paid):
        self.today = datetime.now()
        if discount == None:
            discount = 0
        if not paid:
            expireDate = parser.parse(expireDate)
            remaining = expireDate - self.today
            remaining = remaining.days
            if remaining <= -1:
                debt += price * device - discount
                return debt
            return debt
        return debt


    def _replace(self, items_list, index, item):
        _item = items_list[index]
        del items_list[index]
        items_list.insert(index, item)
        return items_list
    
    def is_pingable(self, ip):
        try:
            if type(ip) is str:
                subprocess.check_output(["ping", "-n", "1", ip])
                return True                      
        except subprocess.CalledProcessError:
            return False

    def validate_email(self, email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

        if(re.search(regex, email)):   
            return True   
        else:   
            return False 
    
    def validate_phone(self, phone):
        if len(phone) == 12:
            if phone.startswith("+9936"):
                phone = phone[5:]
                if phone.startswith("1") or phone.startswith("2") or \
                    phone.startswith("3") or phone.startswith("4") or \
                    phone.startswith("5"):
                    return True
                return False
            return False
        elif len(phone) == 11:
            if phone.startswith("9936"):
                phone = phone[4:]
                if phone.startswith("1") or phone.startswith("2") or \
                    phone.startswith("3") or phone.startswith("4") or \
                    phone.startswith("5"):
                    return True
                return False
        elif len(phone) == 9:
            if phone.startswith("86"):
                phone = phone[2:]
                if phone.startswith("1") or phone.startswith("2") or \
                    phone.startswith("3") or phone.startswith("4") or \
                    phone.startswith("5"):
                    return True
                return False
            return False
        return False

    def ip_extractor(self, server):
        name = list(server.keys())[0]
        serverObj = server[name]
        serverUrl = serverObj["apiUrl"]
        ip = serverUrl[8:].split(":")[0]
        return ip

# e = Extensions()
# index = 2
# server = server_list[2]
# t = e._replace(server_list, index, server)
# print(t)
# e.debt_calculate("16:26 10/12/21", 100)