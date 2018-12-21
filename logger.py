#!/usr/bin/env python
# encoding: utf-8

import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def log(fn):
    def inner(self, *args, **kwargs):
        logger.debug("fn={} args={} kwargs={}".format(fn, args, kwargs))
        return fn(self, *args, **kwargs)
    return inner