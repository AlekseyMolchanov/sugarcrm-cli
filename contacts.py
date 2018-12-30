#!/usr/bin/env python
# encoding: utf-8

from sugarcrm import Contact
from proxy import Proxy, Relation
from meetings import MeetingProxy
from calls import CallProxy
from tasks import TaskProxy


schema = dict(
    first_name=dict(help='First Name of contact', required_in=['create']),
    last_name=dict(required_in=['create']),
    title=dict(required_in=['create']),
    primary_address_street=dict(required_in=['create']),
    primary_address_city=dict(required_in=['create']),
    primary_address_postalcode=dict(required_in=['create']),
    phone_home=dict(required_in=['create']),
    phone_mobile=dict(required_in=['create']),
    phone_other=dict(required_in=['create']),
    phone_work=dict(required_in=['create']),
    salutation=dict(required_in=['create']),
    email1=dict(required_in=['create']),
    id=dict(required_in=['get', 'update', 'delete', 'cascade_delete']),
    account_id=dict(required_in=['create']),
)


class ContactProxy(Proxy):
    cls = Contact
    schema = schema
    relations = [
        Relation(MeetingProxy, 'parent_id', 'parent_type'), 
        Relation(CallProxy, 'parent_id', 'parent_type'),
        Relation(TaskProxy, 'contact_id', None),
        Relation(TaskProxy, 'parent_id', 'parent_type')
    ]
