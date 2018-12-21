#!/usr/bin/env python
# encoding: utf-8

import os
import pytest
from sugar_cli import parse_args, connect


@pytest.fixture(scope="module")
def state():
    return {'account': None}


@pytest.fixture(scope="module")
def session(request):
    __session = connect()
    return __session


def run_command(session, cmd):
    namespace, args = parse_args(cmd if type(cmd) is list else cmd.split(' '))
    handler = namespace.func(args, action=namespace.action, session=session)
    return handler.run()


def test_connect(state, session):
    assert state
    assert session


def test_account_not_has_account_type_cli(state, session):
    assert not run_command(session, 'account show --account_type cli')


def test_account_create(state, session):
    cmd = [
        'account',
        'create',
        '--billing_address_postalcode', '1234',
        '--billing_address_country', 'Russia',
        '--account_type', 'cli',
        '--name', 'Some name',
        '--industry', 'Home',
        '--phone_office', '+4234234234',
        '--billing_address_city', 'Moscow',
        '--billing_address_street', 'red square 1',
    ]
    obj = run_command(session, cmd)
    assert obj
    state['account'] = obj


def test_search_account_by_params(state, session):
    assert run_command(session, 'account show --account_type cli')
    assert run_command(session, 'account show --industry Home')


def test_get_account_by_id(state, session):
    _id = state.get('account').id
    assert run_command(session, 'account get --id %s' % _id)


def test_get_account_by_unreal_id(session):
    with pytest.raises(ValueError, match=r'Not found .*'):
        run_command(session, 'account delete --id unreal-id')


def test_update_account_by_id(state, session):
    new_name = 'New Name'
    _id = state.get('account').id
    cmd = ['account', 'update', '--name', new_name, '--id', _id]
    assert run_command(session, cmd)
    obj = run_command(session, 'account get --id %s' % _id)
    assert obj.name == new_name


def test_contact_create(state, session):
    cmd = [
        'contact',
        'create',
        '--first_name', 'Malchanov',
        '--last_name', 'Aleksey',
        '--title', 'Team Lead',
        '--primary_address_street', 'Malomoskovskaja 15a',
        '--primary_address_city', 'Moscow',
        '--primary_address_postalcode', '129164',
        '--phone_home', '+42342000001',
        '--phone_mobile', '+42342000002',
        '--phone_other', '+42342000003',
        '--phone_work', '+42342000004',
        '--salutation', 'Mr.',
        '--email1', 'some@email.com',
        '--account_id', state.get('account').id
    ]
    obj = run_command(session, cmd)
    assert obj
    state['contact'] = obj


def test_get_contact_by_id(state, session):
    _id = state.get('contact').id
    assert run_command(session, 'contact get --id %s' % _id)


def test_update_contact_by_id(state, session):
    first_name = 'Molchanov'
    _id = state.get('contact').id
    assert run_command(
        session, ['contact', 'update', '--first_name', first_name, '--id', _id])
    obj = run_command(session, 'contact get --id %s' % _id)
    assert obj.first_name == first_name


def test_contact_delete(state, session):
    _id = state.get('contact').id
    assert run_command(session, 'contact delete --id %s' % _id)


def test_account_delete(state, session):
    _id = state.get('account').id
    assert run_command(session, 'account delete --id %s' % _id)
