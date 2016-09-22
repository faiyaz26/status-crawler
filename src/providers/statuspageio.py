#!/usr/bin/python3

from src.models import Status, StatusValue

import requests
from pyquery import PyQuery as pq
import feedparser

class StatusPageIo :
    _service_status = None
    _url = ''
    _dom = None

    _operational_message = 'All Systems Operational'

    def __init__(self):
        pass

    def __init__(self, url):
        self._url = url
        self._service_status = Status(url, 'statuspage.io')

    def _getHtml(self):
        r  = requests.get(self._url)
        self._dom = pq(r.text)
    
    def _parseRss(self):
        rssUrl = self._url + 'history.rss'
        d = feedparser.parse(rssUrl)
        messageList = []
        for i in range(min(5, len(d.entries))):
            msg = {
                'title' : d.entries[i].title,
                'description' : d.entries[i].description,
                'link' : d.entries[i].link,
                'published' : d.entries[i].published
            }
            messageList.append(msg)
            
        return messageList

    def _parse(self):
        status_description = self._dom('.page-status span.status').html().strip();
        status = StatusValue.unknown

        if status_description == self._operational_message :
            status = StatusValue.operational
        else:
            page_status_dom   = self._dom('.page-status')
            if len(page_status_dom) > 0 :
                if page_status_dom.hasClass('status-minor'):
                    status = StatusValue.minor
                elif page_status_dom.hasClass('status-major'):
                    status = StatusValue.major
            
            unresolved_indcident_dom = self._dom('.unresolved-incidents')

            if len(unresolved_indcident_dom) > 0:
                html = unresolved_indcident_dom.html()
                if html.find('impact-major') != -1 :
                    status = StatusValue.major
                elif html.find('impact-minor') != -1:
                    status = StatusValue.minor
                elif html.find('impact-none') != -1:
                    status = StatusValue.non_impact
        
        message_list = self._parseRss()
        self._service_status.set(status, message_list)
        self._service_status.print()
    
    def run(self):
        self._getHtml()
        self._parse()