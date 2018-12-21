#!/usr/bin/env python
# encoding: utf-8

import os
import pytest

from sugar_cli import parse_args, connect


@pytest.fixture(scope="module")
def session(request):
    __session = connect()
    return __session


def test_connect(session):
    assert session

def run_command(session, cmd):
    namespace, args = parse_args(cmd.split(' '))
    handler = namespace.func(args, action=namespace.action, session=session)
    return handler.run()
    
def test_account_not_has_account_type_cli(session):
    assert not run_command(session, 'account show --account_type cli')
    
def test_connection2(session):
    assert run_command(session, 'account show --name t2')
    
def test_account_delete(session):
    assert run_command(session, 'account delete --id ba36a059-debb-4d53-beed-5c1b5765410d')

    
