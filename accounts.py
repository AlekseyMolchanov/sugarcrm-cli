#!/usr/bin/env python
# encoding: utf-8

import generate
from proxy import Proxy, Relation
from sugarcrm import Account
from contacts import ContactProxy
from meetings import MeetingProxy
from calls import CallProxy
from opportunity import OpportunityProxy


account_type_choices = ['Analyst', 'Competitor', 'Customer', 'Integrator',
                        'Investor', 'Other', 'Partner', 'Press', 'Prospect', 'Reseller']

account_industry_choices = [
    'Apparel', 'Banking', 'Biotechnology', 'Chemicals', 'Communications', 'Construction', 'Consulting', 'Education',
    'Electronics', 'Energy', 'Engineering', 'Entertainment', 'Environmental', 'Finance', 'Government', 'Healthcare',
    'Hospitality', 'Insurance', 'Machinery', 'Manufacturing', 'Media', 'Not For Profit', 'Other', 'Recreation',
    'Retail', 'Shipping', 'Technology', 'Telecommunications', 'Transportation', 'Utilities'
]

schema = dict(
    account_type=dict(help='Type', required_in=[
                      'create'], choices=account_type_choices),
    name=dict(help='Account Name', required_in=['create']),
    billing_address_country=dict(help='Billing Country', required_in=[]),
    billing_address_street=dict(help='Billing Street', required_in=['create']),
    billing_address_postalcode=dict(
        help='Billing Postal Code', required_in=['create']),
    billing_address_city=dict(help='Billing City', required_in=['create']),
    phone_office=dict(help='Office Phone', required_in=['create']),
    industry=dict(help='Industry', required_in=['create']),
    id=dict(help='Account ID', required_in=[
            'get', 'update', 'delete', 'cascade_delete']),
)


class AccountProxy(Proxy):
    cls = Account
    schema = schema
    relations = [
        Relation(ContactProxy, 'account_id', None),
        Relation(MeetingProxy, 'parent_id', 'parent_type'),
        Relation(CallProxy, 'parent_id', 'parent_type'),
        Relation(OpportunityProxy, 'account_id', None)
    ]

    def fake_data(self, params):
        
        name = next(generate.generate_CompanyName())
        phone_office = next(generate.generate_Phone())
        billing_address_city = next(generate.generate_City())
        billing_address_street = next(generate.generate_Street())
        
        return dict(
            billing_address_postalcode=generate.generate_ZIP(),
            billing_address_country=generate.generate_Country(),
            account_type=generate.generate_AccountType(),
            name=name,
            industry=generate.generate_Industry(),
            phone_office=phone_office,
            billing_address_city=billing_address_city,
            billing_address_street=billing_address_street
        )