#!/usr/bin/env python
# encoding: utf-8


from sugarcrm import SugarObject
from proxy import Proxy

import generate


class Meeting(SugarObject):
    module = "Meetings"


schema = dict(
    name=dict(required_in=['create']),
    description=dict(required_in=['create']),
    date_start=dict(required_in=['create']),  # yyyy-mm-ddThh:mm:ss-00:00
    date_end=dict(required_in=['create']),  # yyyy-mm-ddThh:mm:ss-00:00
    id=dict(required_in=['get', 'update', 'delete', 'cascade_delete']),
    parent_id=dict(required_in=['create']),
    parent_type=dict(required_in=['create'])
)


class MeetingProxy(Proxy):
    cls = Meeting
    schema = schema

    def fake_data(self, params):
        date_start, date_end = generate.generate_dates_range()
        _id = id(self)

        return dict(
            name="Meeting in {}".format(_id),
            description="Some description about this Meeting {}".format(_id),
            date_start=date_start,
            date_end=date_end,
            parent_id=params.get('parent_id'),
            parent_type=params.get('parent_type')
        )
