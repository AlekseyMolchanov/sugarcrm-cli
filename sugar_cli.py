#!/usr/bin/env python
# encoding: utf-8


import argparse

from connection import connect
from accounts import AccountProxy
from contacts import ContactProxy
from meetings import MeetingProxy
from calls import CallProxy


MODULES = {
    'account': AccountProxy,
    'contact': ContactProxy,
    'call': CallProxy,
    'meeting': MeetingProxy,
    'opportunitie': None
}


def parse_args(args=None):
    parser = argparse.ArgumentParser(prog='sugar_cli')
    subparsers = parser.add_subparsers()
    for module, proxy in MODULES.items():
        if proxy:
            sp = subparsers.add_parser(module)
            choices = ['show', 'get', 'create', 'update', 'delete', 'cascade_delete']
            sp.add_argument('action', type=str, help='Sugar CRM model action', choices=choices)
            sp.set_defaults(func=proxy)

    return parser.parse_known_args(args=args)


if __name__ == "__main__":
    session = connect()
    namespace, args = parse_args()
    print(namespace, args)
    handler = namespace.func(args, action=namespace.action, session=session)
    try:
        exit(handler.run())
    except ValueError as exception:
        print (exception)
        exit(1)
