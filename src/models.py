#!/usr/bin/python3
import json
from datetime import datetime
import calendar

class Status:
    _data = {'url' : '', 'provider' : '', 'status' : 0, 'messages' : [], 'updatedAt': None}
    
    def __init__(self):
        pass
    
    def __init__(self, url, provider):
        self._data['url'] = url
        self._data['provider'] = provider
        self._data['updateAt'] = calendar.timegm(datetime.utcnow().utctimetuple())

    def set(self, status, message_list):
        self._data['status'] = status
        self._data['messages'] = message_list
        self._data['updatedAt'] = calendar.timegm(datetime.utcnow().utctimetuple())
    
    def print(self):
        print(self._data)
        return

    def getJson(self):
        return json.dumps(self._data)


class StatusValue:
    unknown     = 0
    non_impact  = 100
    operational = 200
    minor       = 300
    major       = 500
