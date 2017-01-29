#!/usr/bin/python3
# encoding: utf-8
from src.providers.providerfactory import ProviderFactory

test = ProviderFactory.createCrawler('StatusIo','http://status.objectrocket.com/')

test.run()

print(test)