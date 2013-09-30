#! /usr/bin/python
import os
from bottle import route, run, template
import datetime
from dateutil import parser
from csv_interface import build_interface

klein, groot = build_interface()
schedules = {"klein":klein, "groot":groot}

@route('/qr/<code>/<time>')
def index(code='klein1', time=None):
    age = code[:5]
    group = int(code[5:])
    if age in schedules:
        if time:
            time = parser.parse(time)
        if not time: 
            time = datetime.datetime.now()
        activity = schedules[age][time][group]
        return template('<b>Je moet naar {{activity}}</b>!', activity=activity)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    run(host='0.0.0.0', port=port, debug=True)
