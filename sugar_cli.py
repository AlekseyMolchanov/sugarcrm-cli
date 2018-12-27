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

class _HelpAction(argparse._HelpAction):

    def __call__(self, parser, namespace, values, option_string=None):
        print(open('usage.md').read())
        parser.exit()


def parse_args(args=None):
    parser = argparse.ArgumentParser(prog='sugar_cli', add_help=False)
    parser.add_argument('--help', action=_HelpAction, help='show full help message and exit') 

    subparsers = parser.add_subparsers(help='modules')
    for module, proxy in MODULES.items():
        if proxy:
            sp = subparsers.add_parser(module, help="Module: %s" % proxy.cls.module)
            choices = ['show', 'get', 'create',
                       'update', 'delete', 'cascade_create', 'cascade_delete']
            sp.add_argument('action', type=str,
                            help='Available module action', choices=choices)
            sp.set_defaults(func=proxy)
    namespace, args = parser.parse_known_args(args=args)
    return parser, namespace, args


if __name__ == "__main__":
    session = connect()
    parser, namespace, args = parse_args()
    
    if not session:
        print ("\n######## Warning ########")
        print ("You must define Environment Variables:")
        print ("SUGAR_CRM_URL, SUGAR_CRM_USERNAME and SUGAR_CRM_PASSWORD")
        print ("###########################\n")
        exit(1)
    
    if not hasattr(namespace, 'func') or not session:
        parser.print_help()
        exit(1)


    handler = namespace.func(args, action=namespace.action, session=session)
    try:
        handler.run()
        exit(0)
    except ValueError as exception:
        print (exception)
        exit(1)
