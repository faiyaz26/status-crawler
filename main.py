#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.providers.statusio import StatusIo

test = StatusIo('http://status.objectrocket.com/');

test.run()