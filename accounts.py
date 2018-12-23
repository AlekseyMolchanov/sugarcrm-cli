#!/usr/bin/env python
# encoding: utf-8

from proxy import Proxy
from sugarcrm import Account
from contacts import ContactProxy
from meetings import MeetingProxy


schema = dict(
    account_type=dict(help='type of account', required_in=['create']),
    name=dict(help='Name of account', required_in=['create']),
    billing_address_country=dict(required_in=[]),
    billing_address_street=dict(required_in=['create']),
    billing_address_postalcode=dict(required_in=['create']),
    billing_address_city=dict(required_in=['create']),
    phone_office=dict(required_in=['create']),
    industry=dict(required_in=['create']),
    id=dict(required_in=['get', 'update', 'delete', 'cascade_delete']),
)


class AccountProxy(Proxy):
    cls = Account
    schema = schema
    relations = [ContactProxy, MeetingProxy]
