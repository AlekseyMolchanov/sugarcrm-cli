#!/usr/bin/env python
# encoding: utf-8


import argparse

from connection import connect
from accounts import AccountProxy
from contacts import ContactProxy
from meetings import MeetingProxy
from calls import CallProxy
from opportunity import OpportunityProxy


MODULES = {
    'account': AccountProxy,
    'contact': ContactProxy,
    'call': CallProxy,
    'meeting': MeetingProxy,
    'opportunity': OpportunityProxy
}


def parse_args(args=None):
    parser = argparse.ArgumentParser(prog='sugar_cli')

    subparsers = parser.add_subparsers()
    for module, proxy in MODULES.items():
        if proxy:
            sp = subparsers.add_parser(module)
            choices = ['show', 'get', 'create',
                       'update', 'delete', 'cascade_delete']
            sp.add_argument('action', type=str,
                            help='Sugar CRM model action', choices=choices)
            sp.set_defaults(func=proxy)
            
    namespace, args = parser.parse_known_args(args=args)
    
    return parser, namespace, args


if __name__ == "__main__":
    session = connect()
    parser, namespace, args = parse_args()
    if not hasattr(namespace, 'func') or not session:
        if not session:
            print ("\n######## Warning ########")
            print ("You must define Environment Variables:")
            print ("SUGAR_CRM_URL, SUGAR_CRM_USERNAME and SUGAR_CRM_PASSWORD")
            print ("###########################\n")
        parser.print_help()
        exit(1)

    handler = namespace.func(args, action=namespace.action, session=session)
    try:
        exit(handler.run())
    except ValueError as exception:
        print (exception)
        exit(1)
