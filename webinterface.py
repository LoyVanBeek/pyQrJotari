#! /usr/bin/python
from bottle import route, run, template

#from pyQRjotari import 

@route('/qr/<group>')
def index(group='klein1'):
    return template('<b>Je moet naar {{group}}</b>!', group=group)

run(host='localhost', port=8080)
