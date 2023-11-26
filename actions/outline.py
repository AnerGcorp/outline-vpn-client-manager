#!/usr/bin/env python
import argparse
import json
import requests
import ssl
from requests_toolbelt.adapters.fingerprint import FingerprintAdapter
import urllib
from actions.recorddata import RecordData as rd

ACCESS_PREAMBLE = "https://s3.amazonaws.com/outline-vpn/invite.html#"
servers = {}
server_names = []
serverDownMessage = "There is a connection error or your server is down!"

# Outline servers use self-signed certs
# We're using requests_toolbelt to compare the certificate sha256 against the definition
# and will throw an error if they don't match
requests.packages.urllib3.disable_warnings()

class Outline:
  def __init__(self):
    self.rd = rd()
    self.__load_servers()

  def __load_servers(self):
    """
      Load list of servers from JSON file and populate server list.
      Server list format is  
            [
              { 
                "mnemonic": { output object from Outline setup }}, 
              {...}
            ]
      We'll be using both the servers and the server_names variables!
    """
    global servers
    global server_names
    servers = self.rd.read_servers()
    if servers != []:
      for key_dict in servers:
        key = list(key_dict.keys())[0]
        server_names.append(key)
    return None

  def __call_api(self, action, server, userid=None, username=None):
    """Wrapper thing to call the API based on different actions."""
    if action == 'deluser' and not userid:
      # raise Exception('Cannot call deluser without passing a User ID')
      print( "Cannot call deluser without passing a User ID")
      return None

    # Construct the URL string to use and get the sha256 fp from the server definition
    for _ in servers:
      if list(_.values())[0] == server:
        index = servers.index(_)
    # index = server_names.index(server)
    urlline = [servers[index][server_names[index]]['apiUrl'], '/access-keys']
    certfp = servers[index][server_names[index]]['certSha256']

    # Mount adapter to verify fingerprint
    s = requests.Session()
    s.mount(urlline[0], FingerprintAdapter(certfp))

    if action == "adduser":
      try:
        r = s.post(''.join(urlline), verify=False)
      except Exception as e:
        # raise e
        print(serverDownMessage)
        return None

      # TODO: Figure out how to get the username to show up in the record we print when done
      if username:
        data = json.loads(r.text)
        uid = data['id']
        urlline.append("/" + str(uid) + "/name")
        try:
          r2 = s.put(''.join(urlline), data = {'name':username}, verify=False)
        except Exception as e:
          # raise e
          print(serverDownMessage)
          return None

        # print(r2)

    
    elif action == "deluser":
      urlline.append("/" + str(userid))
      try:
        r = s.delete(''.join(urlline), verify=False)
      except Exception as e:
        # raise e
        print(serverDownMessage)
        return None

      else:
        if r.status_code == requests.codes.no_content:
          print("User key %s deleted successfully" % userid)
        else:
          print("Unexpected status code: %s" % r.status_code)
    
    elif action == "listusers":
      try:
        r = s.get(''.join(urlline), verify=False)
      except Exception as e:
        # raise e
        print(serverDownMessage)
        return None
    else:
      # raise Exception("%s is not a legal option!" % action)
      print("WE ARE SORRY YOU CHOOSE WRONG OPTION")
      return None
    return r


  def adduser(self, server, username):
    """Takes a server ID and add a new user key on the server. Prints a pretty record of the new key for ease of sharing."""
    result = self.__call_api('adduser', server, username=username)
    # print(result)
    if result != None:
      data = json.loads(result.text)
      self.__prettyrecord(data)
      return result
    return None

  def deluser(self, server, userid):
    """Takes a server ID and a user key ID and deletes the key from the server. Will alert if you get anything but HTTP 204 in response."""
    result = self.__call_api('deluser', server, userid=userid)

  def listusers(self, server):
    """Takes a server ID and returns a pretty record of all user keys on the server."""
    result = self.__call_api('listusers', server)
    if result != None:
      data = json.loads(result.text)

      for key in data['accessKeys']:
        print(key['id'])
        output = self.__prettyrecord(key)
        print(output)
        return output
      return None

  def __prettyrecord(self, accesskey):
    """Takes a JSON format access key record and prints a pretty version.
    Plays nice and listens to the -i switch to either print a one-click access link or not."""
    s = str(ACCESS_PREAMBLE + urllib.parse.quote(accesskey["accessUrl"]))
    return s

if __name__ == '__main__':
  print("successfully Imported")
  # out = Outline()
  # # out.listusers('usa')
  # print(out.adduser("usa", 'Azamat'))
