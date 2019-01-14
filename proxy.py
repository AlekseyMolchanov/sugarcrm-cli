#!/usr/bin/env python
# encoding: utf-8

import argparse
from collections import namedtuple
from logger import log, logger
import pprint


Relation = namedtuple('Relation', ['related', 'id_field', 'module_field'])


class Proxy(object):

    relations = []

    def __init__(self, args=None, action=None, session=None):
        self.args = args
        self.action = action
        self.session = session

    def fake_data(self, params):
        raise Warning("fake_data Not implemented in [{}]".format(self.__class__.__name__))

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

        fields = subparsers.add_parser('fields')
        fields.add_argument('--type', type=str, help='fileds list name', required=False, default='module_fields')
        fields.add_argument('--field', type=str, help='filed to explain', required=False, default=None)

        get = subparsers.add_parser('get')
        get.add_argument('--id', type=str, help='object giud', required=True)

        delete = subparsers.add_parser('delete')
        delete.add_argument( '--id', type=str, help='object giud for delete', required=True)
        
        cascade_delete = subparsers.add_parser('cascade_delete')
        cascade_delete.add_argument( '--id', type=str, help='object giud for cascade delete', required=True)

        cascade_create = subparsers.add_parser('cascade_create')
        cascade_create.add_argument( '--count', type=int, help='Count of items to generate', required=True)

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

    def pprint(self, obj, fn=logger.debug):
        data = dict()
        for key in self.schema:
            if hasattr(obj, key):
                data[key] = getattr(obj, key)
        fn(pprint.pformat(data, indent=4))

    @log
    def fields(self, params, **kwargs):
        _type = params.get('type')
        _field = params.get('field')
        _data = self.session.get_module_fields(self.cls.module)
        if _type in _data:
            _data = _data.get(_type)
            if _field in _data:
                print(_data.get(_field))
            else:
                print(_data.keys())
        else:
            print(_data.keys())

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
            self.pprint(each, fn=print)
        return results

    @log
    def create(self, params):
        '''
        ./sugar_cli.py account create --billing_address_postalcode 1234 --account_type 'Integrator' --name "Some name" --industry "Home" --phone_office  +4234234234 --billing_address_city Moscow --billing_address_street "red 1"
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
    def cascade_delete(self, params, action = 'cascade_delete'):
        '''
        cascade delete by id
        ./sugar_cli.py account cascade_delete --id=a3a0f97a-749d-f1a6-9a08-5bf5d7d63de1
        '''
        _id = params.get('id')
        current = self.session.get_entry(self.cls.module, _id)
        if current:
            for relation in self.relations:
                module = relation.related.cls.module
                links = dict()
                
                if not relation.module_field: # linked by link field
                    links[module] = ['id']
                    
                    linked = self.session.get_entry(self.cls.module, current.id, links=links)
                    if linked:
                        for link in getattr(linked, module.lower(), []):
                            rel = relation.related(None, action=action, session=self.session)
                            rel.cascade_delete(dict(id=link.id))
                
                else: # linked by select field
                    links[relation.id_field] = _id
                    links[relation.module_field] = self.cls.module # may be it is over
                    linked = self.session.get_entry_list( relation.related.cls(**links) )
                    for link in linked:
                        rel = relation.related(None, action=action, session=self.session)
                        rel.cascade_delete(dict(id=link.id))

            current.deleted = True
            current = self.session.set_entry(current)
            return True
            
        else:
            raise ValueError('Not found {} [{}]'.format(self.cls.module, _id))

    @log
    def cascade_create(self, params):
        
        result = []

        count = params.get('count')
        for index, each in enumerate(range(count)):
            
            obj = self.create(self.fake_data(params))
            result.append(obj)
            for relation in self.relations:
                
                params = dict(count=count)
                params[relation.id_field] = obj.id
                if relation.module_field:
                    params[relation.module_field] = self.cls.module

                rel = relation.related(None, action='cascade_create', session=self.session)
                rel.cascade_create(params)
        
        return result
