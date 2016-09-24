#!/usr/bin/python3

from src.models import Status, StatusValue
from src.providers.provider import Provider
import requests
from pyquery import PyQuery as pq
import feedparser

class StatusPageIo(Provider):
    
    _operational_message = 'All Systems Operational'

    def __init__(self, url):
        self._url = url
        self._service_status = Status(url, 'statuspage.io')

    def _getHtml(self):
        r  = requests.get(self._url)
        self._dom = pq(r.text)
    
    def check(self):
        d = self._dom('.powered-by a')
        if(len(d) == 0):
            return False
        else:
            if(d.attr('href') == 'http://www.statuspage.io'):
                return True
            return False

    def _parseRss(self):
        rssUrl = self._url + 'history.rss'
        d = feedparser.parse(rssUrl)
        messageList = []
        for i in range(min(5, len(d.entries))):
            msg = {
                'title' : d.entries[i].title,
                'description' : d.entries[i].description,
                'link' : d.entries[i].link,
                'publishedAt' : d.entries[i].published
            }
            messageList.append(msg)
            
        return messageList
    

    def _getScheduledMessages(self):
        scheduledMessageList = []
        scheduled_maintenances_container = self._dom('.scheduled-maintenances-container')
        
        if(len(scheduled_maintenances_container) > 0):
            all_scheduled_msg = self._dom('.scheduled-maintenance')
            for cur in self._dom('.scheduled-maintenance').items():
                msg = {
                    'title' : cur.find('.incident-title a').text().strip(),
                    'description' : cur.find('.updates-container .update').text().strip(),
                    'scheduledDate' : cur.find('.incident-title small').text().strip(),
                    'publishedAt' : cur.find('.updates-container .update small').text().strip()
                }
                scheduledMessageList.append(msg)
            
        return scheduledMessageList

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
        
        scheduled_msg_list = self._getScheduledMessages()
        incident_msg_list = self._parseRss()
        self._service_status.set(status, scheduled_msg_list, incident_msg_list)
        self._service_status.print()
    
    def run(self):
        self._getHtml()
        if self.check() == False:
            print("Provider doesn't match")
            return
        self._parse()