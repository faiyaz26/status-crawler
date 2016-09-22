#!/usr/bin/python3

from src.providers.statuspageio import StatusPageIo

test = StatusPageIo('https://metastatuspage.com/');

test.run()