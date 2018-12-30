#!/usr/bin/env python
# encoding: utf-8

from sugarcrm import Contact
from proxy import Proxy, Relation
from meetings import MeetingProxy
from calls import CallProxy
from tasks import TaskProxy

import generate

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

    def fake_data(self, params):
        
        primary_address_city = next(generate.generate_City())
        primary_address_street = next(generate.generate_Street())

        phones = generate.generate_Phone()

        first_name, last_name, _, salutation = generate.generate_person()
        
        return dict(
            first_name=first_name,
            last_name=last_name,
            title=generate.generate_Position(),
            primary_address_street=primary_address_street,
            primary_address_city=primary_address_city,
            primary_address_postalcode=generate.generate_ZIP(),
            phone_home=next(phones),
            phone_mobile=next(phones),
            phone_other=next(phones),
            phone_work=next(phones),
            salutation=salutation,
            email1=generate.generate_Email(first_name, last_name),
            account_id=params.get('account_id'),
        )