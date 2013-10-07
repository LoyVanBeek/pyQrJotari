#! /usr/bin/python
import os
from bottle import route, run, template, post
import datetime
from dateutil import parser
from csv_interface import build_interface

klein, groot = build_interface()
schedules = {"klein":klein, "groot":groot}

@route('/qr/<code>/')
@route('/qr/<code>/<time>/', defaults={'time': None})
@route('/qr/<code>')
@route('/qr/<code>/<time>', defaults={'time': None})
def index(code='klein1', time=None):
    age = code[:5]
    group = int(code[5:])
    if age in schedules:
        if time:
            time = parser.parse(time)
        if not time: 
            time = datetime.datetime.now()
        try:
            activity = schedules[age][time][group]
            return template('Je moet naar <b>{{activity}}</b>!', activity=activity)
        except KeyError:
            return template("Het is nog geen JOTARI. Je kunt ook een tijd proberen: <a href='19-10-2013%2010:00'>Zaterdag 10 uur</a>", group=code)
        except TypeError:
            return template("Het is nog geen JOTARI. Je kunt ook een tijd proberen: <a href='19-10-2013%2010:00'>Zaterdag 10 uur</a>", group=code)

@post('/qr/reload')
@route('/qr/reload')
def reload():
    print "Pulling..."
    os.system("git pull")
    print "Pulled"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True, reloader=True)
