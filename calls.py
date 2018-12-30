#!/usr/bin/env python
# encoding: utf-8

from sugarcrm import Call
from proxy import Proxy

import generate

schema = dict(
    id=dict(required_in=['get', 'update', 'delete', 'cascade_delete']),
    name=dict(required_in=['create']),
    date_start=dict(required_in=['create']),  # yyyy-mm-ddThh:mm:ss-00:00
    parent_id=dict(required_in=['create']),
    parent_type=dict(required_in=['create'])
)


class CallProxy(Proxy):
    cls = Call
    schema = schema

    def fake_data(self, params):
        date_start, date_end = generate.generate_dates_range()
        _id = id(self)

        return dict(
            name="Call at {}".format(date_start),
            date_start=date_start,
            parent_id=params.get('parent_id'),
            parent_type=params.get('parent_type')
        )
