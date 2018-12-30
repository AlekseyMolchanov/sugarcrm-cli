#!/usr/bin/env python
# encoding: utf-8

from sugarcrm import Task
from proxy import Proxy, Relation
from calls import CallProxy

import generate

schema = dict(
    name=dict(required_in=['create']),
    description=dict(required_in=['create']),
    date_start=dict(required_in=['create']), # yyyy-mm-ddThh:mm:ss-00:00
    date_end=dict(required_in=['create']), # yyyy-mm-ddThh:mm:ss-00:00
    date_modified=dict(required_in=[]),
    priority=dict(required_in=['create'], choices=['High','Low','Medium']),                      
    id=dict(required_in=['get', 'update', 'delete', 'cascade_delete']),
    contact_id=dict(required_in=['create']),
    parent_id=dict(required_in=['create']),
    parent_type=dict(required_in=['create'])
)


class TaskProxy(Proxy):
    cls = Task
    schema = schema
    relations = [
        Relation(CallProxy, 'parent_id', 'parent_type')
    ]

    def fake_data(self, params):

        date_start, date_end = generate.generate_dates_range()
        now = generate.generate_now()
        
        _id = id(self)

        return dict(
            name="Task #{}".format(_id),
            description="Some task description",
            date_start=date_start, # yyyy-mm-ddThh:mm:ss-00:00
            date_end=date_end, # yyyy-mm-ddThh:mm:ss-00:00
            date_modified=now,
            priority='Medium',                      
            contact_id=params.get('contact_id'),
            parent_id=params.get('parent_id'),
            parent_type=params.get('parent_type')
        )