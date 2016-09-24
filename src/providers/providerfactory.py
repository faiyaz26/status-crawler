#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.providers.statusio import StatusIo
from src.providers.statuspageio import StatusPageIo


class ProviderFactory(object):
    @staticmethod
    def createCrawler(service_type, url):
        if service_type == 'StatusPageIo':
            return StatusPageIo(url)
        elif service_type == 'StatusIo':
            return StatusIo(url)