#!/usr/bin/python3

from src.models import Status, StatusValue
from src.providers.provider import Provider
import requests
from pyquery import PyQuery as pq
import feedparser

class StatusIo(Provider) :
    _operational_message = 'All Systems Operational'

    def __init__(self, url):
        self._url = url
        self._service_status = Status(url, 'status.io')

    def _getHtml(self):
        r  = requests.get(self._url)
        self._dom = pq(r.text)
    
    def check(self):
        d = self._dom('#statusio_branding')

        if(len(d) == 0):
            return False
        return True


    def _parseRss(self):
        rssUrl = self._dom('#tab_rss a').attr('href')
        #print(rssUrl)
        d = feedparser.parse(rssUrl)
        d.entries.reverse()
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
        scheduled_maintenances_container = self._dom('#section_maintenance_scheduled')
        
        if(len(scheduled_maintenances_container) > 0):
            all_scheduled_msg = self._dom('div[id^="statusio_maintenance_scheduled"]')
            for cur in all_scheduled_msg.items():
                detailed_info_dom = list(cur.find('.maintenance_section.event_inner_text').items())
                #print(len(detailed_info_dom))
                msg = {
                    'title' : cur.find('.maintenance_status_description').siblings('a').text().strip(),
                    'description' : detailed_info_dom[3].text().strip(),
                    'scheduledDate' : detailed_info_dom[0].text().strip(),
                    'publishedAt' : None
                }
                scheduledMessageList.append(msg)
            
        return scheduledMessageList

    def _parse(self):
        status_description = self._dom('#statusbar_text').html().strip();
        status = StatusValue.unknown

        if status_description == self._operational_message :
            status = StatusValue.operational
        elif status_description.find('impact-major'):
            status = StatusValue.major
        elif status_description.find('impact-minor'):
            status = StatusValue.minor
        else:
            status = StatusValue.unknown
        
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