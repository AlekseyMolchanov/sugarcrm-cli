#!/usr/bin/env python
# encoding: utf-8

from sugarcrm import Opportunity
from proxy import Proxy, Relation

from tasks import TaskProxy
from calls import CallProxy
from meetings import MeetingProxy

import generate

schema = dict(
    id=dict(help='Opportunity ID', required_in=[
            'get', 'update', 'delete', 'cascade_delete']),
    name=dict(help='Opportunity Name', required_in=['create']),
    date_closed=dict(help='Expected Close Date', required_in=[
                     'create']),  # yyyy-mm-ddThh:mm:ss-00:00
    account_id=dict(help='Account ID', required_in=['create']),
    account_name=dict(help='Account Name', required_in=[]),
    amount=dict(help='Opportunity Amount', required_in=['create']),
)


class OpportunityProxy(Proxy):
    cls = Opportunity
    schema = schema
    relations = [
        Relation(TaskProxy, 'parent_id', 'parent_type'),
        Relation(CallProxy, 'parent_id', 'parent_type'),
        Relation(MeetingProxy, 'parent_id', 'parent_type'), 
    ]
    
    def fake_data(self, params):

        _, date_closed = generate.generate_dates_range()
        now = generate.generate_now()
        
        _id = id(self)

        return dict(
            name="Opportunity #{}".format(_id),
            date_closed=date_closed, # yyyy-mm-ddThh:mm:ss-00:00
            amount=1,                      
            account_id=params.get('account_id')
        )