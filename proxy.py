#!/usr/bin/env python
# encoding: utf-8

import argparse

from logger import log, logger
import pprint


class Proxy(object):

    relations = []

    def __init__(self, args, action=None, session=None):
        self.args = args
        self.action = action
        self.session = session

    def run(self):
        namespace = self.parse_args()
        _params = vars(namespace)
        params = {}
        for k, v in _params.items():
            if not(v is None):
                params[k] = v
        return getattr(self, self.action)(params)

    @log
    def parse_args(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        get = subparsers.add_parser('get')
        get.add_argument('--id', type=str, help='object giud', required=True)

        delete = subparsers.add_parser('delete')
        delete.add_argument( '--id', type=str, help='object giud for delete', required=True)
        
        cascade_delete = subparsers.add_parser('cascade_delete')
        cascade_delete.add_argument( '--id', type=str, help='object giud for cascade delete', required=True)

        show = subparsers.add_parser('show')
        for param, options in self.schema.items():
            show.add_argument('--{}'.format(param), required=False)

        update = subparsers.add_parser('update')
        for param, options in self.schema.items():
            argument_settings = dict(required=('update' in options['required_in']))
            if 'choices' in options:
                argument_settings['choices'] = options['choices']
            update.add_argument('--{}'.format(param), **argument_settings)

        create = subparsers.add_parser('create')
        for param, options in self.schema.items():
            argument_settings = dict(required=('create' in options['required_in']))
            if 'choices' in options:
                argument_settings['choices'] = options['choices']
            create.add_argument('--{}'.format(param), **argument_settings)

        return parser.parse_args([self.action] + self.args)

    def pprint(self, obj):
        data = dict()
        for key in self.schema:
            if hasattr(obj, key):
                data[key] = getattr(obj, key)
        logger.debug(pprint.pformat(data, indent=4))

    @log
    def show(self, params, **kwargs):
        '''
        show all object in module
        ./sugar_cli.py account show 

        or find by attr
        ./sugar_cli.py account show --name=t2
        '''
        items = self.cls(**params)
        results = self.session.get_entry_list(items)
        for each in results:
            self.pprint(each)
        return results

    @log
    def create(self, params):
        '''
        ./sugar_cli.py account create --billing_address_postalcode 1234 --account_type 'cli' --name "Some name" --industry "Home" --phone_office  +4234234234 --billing_address_city Moscow --billing_address_street "red 1"
        '''
        obj = self.cls(**params)
        result = self.session.set_entry(obj)
        self.pprint(result)
        return result

    @log
    def get(self, params):
        '''
        get by id
        ./sugar_cli.py account get --id=a3a0f97a-749d-f1a6-9a08-5bf5d7d63de1
        '''
        _id = params.get('id')
        current = self.session.get_entry(self.cls.module, _id)
        if current:
            self.pprint(current)
            return current
        else:
            raise ValueError('Not found {} [{}]'.format(self.cls.module, _id))

    @log
    def update(self, params):
        '''
        update by id
        ./sugar_cli.py account update --billing_address_postalcode 123 --id  b3746d3b-5582-e09b-a01e-5c1b571b0147
        '''        
        _id = params.get('id')
        current = self.session.get_entry(self.cls.module, _id)
        if current:
            for key, value in params.items():
                setattr(current, key, value)
            current = self.session.set_entry(current)
            return current
        else:
            raise ValueError('Not found {} [{}]'.format(self.cls.module, _id))
        

    @log
    def delete(self, params):
        '''
        delete by id
        ./sugar_cli.py account delete --id=a3a0f97a-749d-f1a6-9a08-5bf5d7d63de1
        '''
        _id = params.get('id')
        current = self.session.get_entry(self.cls.module, _id)
        if current:
            current.deleted = True
            current = self.session.set_entry(current)
            return True
        else:
            raise ValueError('Not found {} [{}]'.format(self.cls.module, _id))

    @log
    def cascade_delete(self, params):
        '''
        cascade delete by id
        ./sugar_cli.py account cascade_delete --id=a3a0f97a-749d-f1a6-9a08-5bf5d7d63de1
        '''
        _id = params.get('id')
        current = self.session.get_entry(self.cls.module, _id)
        if current:
            for relation in self.relations:

                link = dict()
                link[relation.cls.module] = ['id']
                linked = self.session.get_entry(self.cls.module, current.id, links=link)
                if linked:
                    if hasattr(linked, relation.cls.module.lower()):
                        for link in getattr(linked, relation.cls.module.lower()):
                            rel = relation(None, action='cascade_delete', session=self.session)
                            rel.cascade_delete(dict(id=link.id))
            
            current.deleted = True
            current = self.session.set_entry(current)
            return True
            
        else:
            raise ValueError('Not found {} [{}]'.format(self.cls.module, _id))
