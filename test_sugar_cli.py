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
    parser, namespace, args = parse_args(
        cmd if type(cmd) is list else cmd.split(' '))
    handler = namespace.func(args, action=namespace.action, session=session)
    return handler.run()


def test_connect(state, session):
    assert state
    assert session


def test_account_not_has_account_with_type_Other(state, session):
    assert not run_command(session, 'account show --account_type Other')


def test_account_create(state, session):
    cmd = [
        'account',
        'create',
        '--billing_address_postalcode', '1234',
        '--billing_address_country', 'Russia',
        '--account_type', 'Other',
        '--name', 'Some name',
        '--industry', 'Other',
        '--phone_office', '+4234234234',
        '--billing_address_city', 'Moscow',
        '--billing_address_street', 'red square 1',
    ]
    obj = run_command(session, cmd)
    assert obj
    state['account'] = obj


def test_search_account_by_params(state, session):
    assert run_command(session, 'account show --account_type Other')
    assert run_command(session, 'account show --industry Other')


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


def test_meeting_create_for_account(state, session):
    cmd = [
        'meeting',
        'create',
        '--name', 'one',
        '--description', 'description one',
        '--date_start', '2018-12-23T12:00:00-00:00',
        '--date_end', '2018-12-23T13:00:00-00:00',
        '--parent_id', state.get('account').id,
        '--parent_type', state.get('account').module
    ]
    obj = run_command(session, cmd)
    assert obj
    state['meeting'] = obj


def test_call_create_for_contact(state, session):
    cmd = [
        'call',
        'create',
        '--name', 'one call to %s %s' % (state.get('contact').first_name,
                                         state.get('contact').last_name),
        '--date_start', '2018-12-23T12:00:00-00:00',
        '--parent_id', state.get('contact').id,
        '--parent_type', state.get('contact').module
    ]
    obj = run_command(session, cmd)
    assert obj
    state['call'] = obj


def test_opportunity_create_for_account(state, session):
    cmd = [
        'opportunity',
        'create',
        '--name', 'some my opportunity',
        '--date_closed', '2018-12-23T12:00:00-00:00',
        '--account_id', state.get('contact').id,
        '--amount', '100500'
    ]
    obj = run_command(session, cmd)
    assert obj
    state['opportunity'] = obj


def test_task_create_for_account(state, session):
    cmd = [
        'task',
        'create',
        '--name', 'it is account task',
        '--description', 'description task',
        '--priority', 'Low',
        '--date_start', '2018-12-23T12:00:00-00:00',
        '--date_end', '2018-12-23T13:00:00-00:00',
        '--contact_id', state.get('contact').id,
        '--parent_id', state.get('account').id,
        '--parent_type', state.get('account').module
    ]
    obj = run_command(session, cmd)
    assert obj
    state['account_task'] = obj


def test_task_create_for_opportunity(state, session):
    cmd = [
        'task',
        'create',
        '--name', 'it is opportunity task',
        '--description', 'description task',
        '--priority', 'High',
        '--date_start', '2018-12-23T12:00:00-00:00',
        '--date_end', '2018-12-23T13:00:00-00:00',
        '--contact_id', state.get('contact').id,
        '--parent_id', state.get('opportunity').id,
        '--parent_type', state.get('opportunity').module
    ]
    obj = run_command(session, cmd)
    assert obj
    state['opportunity_task'] = obj


def test_contact_delete(state, session):
    _id = state.get('contact').id
    assert run_command(session, 'contact delete --id %s' % _id)


def test_account_delete(state, session):
    _id = state.get('account').id
    assert run_command(session, 'account delete --id %s' % _id)


def test_meeting_delete(state, session):
    _id = state.get('meeting').id
    assert run_command(session, 'meeting delete --id %s' % _id)


def test_call_delete(state, session):
    _id = state.get('call').id
    assert run_command(session, 'call delete --id %s' % _id)


def test_opportunity_delete(state, session):
    _id = state.get('opportunity').id
    assert run_command(session, 'opportunity delete --id %s' % _id)


def test_account_cascade_delete(state, session):
    test_account_create(state, session)
    test_contact_create(state, session)
    test_meeting_create_for_account(state, session)
    test_opportunity_create_for_account(state, session)

    _id = state.get('account').id
    assert run_command(session, 'account cascade_delete --id %s' % _id)


def test_account_cascade_create(state, session):
    objs = run_command(session, 'account cascade_create --count=1')
    assert objs
    state['account_cascade_create'] = objs


def test_account_cascade_delete_cleanup(state, session):
    if 'account_cascade_create' in state:
        for each in state['account_cascade_create']:
            assert run_command(
                session, 'account cascade_delete --id %s' % each.id)
