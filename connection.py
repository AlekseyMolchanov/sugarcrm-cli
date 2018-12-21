#!/usr/bin/env python
# encoding: utf-8


import os
from sugarcrm import Session


def connect():
    url = os.environ['URL']
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    session = Session(url, username, password)
    return session
