#!/usr/bin/env python
# encoding: utf-8

from sugarcrm import Task
from proxy import Proxy, Relation
from calls import CallProxy


schema = dict(
    name=dict(required_in=['create']),
    description=dict(required_in=['create']),
    date_start=dict(required_in=['create']), # yyyy-mm-ddThh:mm:ss-00:00
    date_end=dict(required_in=['create']), # yyyy-mm-ddThh:mm:ss-00:00
    date_modified=dict(required_in=[]),
    priority=dict(required_in=['create'], choices=['High','Low','Medium']),                      
    id=dict(required_in=['get', 'update', 'delete', 'cascade_delete']),
    parent_id=dict(required_in=['create']),
    parent_type=dict(required_in=['create'])
)


class TaskProxy(Proxy):
    cls = Task
    schema = schema
    relations = [
        Relation(CallProxy, 'parent_id', 'parent_type')
    ]
