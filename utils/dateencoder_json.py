#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json
import datetime

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


if __name__ == "__mian__":
    dic = {'name': 'jack', 'create_time': datetime.datetime(2019, 3, 19, 10, 6, 6)}
    de = DateEncoder()
    data = de.default(dic)
    print(json.dumps(data,cls=DateEncoder))


