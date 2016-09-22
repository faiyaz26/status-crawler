#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.providers.statuspageio import StatusPageIo

test = StatusPageIo('https://status.newrelic.com/');

test.run()