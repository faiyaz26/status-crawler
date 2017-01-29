#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq

class Provider:
    _url = ''
    _dom = None
    _service_status = None
    _operational_message = None
    _service_status = None

    def __init__():
        pass

    def _getHtml(self):
    	r=requests.get(self._url)
    	self._dom = pq(r.text)

    @property
    def check(self):
    	raise NotImplementedError("Subclasses should implement this!")
    
    @property
    def run(self):
    	raise NotImplementedError("Subclasses should implement this!")

    def __str__(self):
    	return self._url + str(self._service_status)

