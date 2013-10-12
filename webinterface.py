#! /usr/bin/python
import os
from bottle import route, run, template, post
import datetime
from dateutil import parser
from csv_interface import build_interface
import pprint

klein, groot = build_interface()
schedules = {"klein":klein, "groot":groot}

@route('/qr/<code>/')
@route('/qr/<code>/<time>/', defaults={'time': None})
@route('/qr/<code>')
@route('/qr/<code>/<time>', defaults={'time': None})
def index(code='klein1', time=None):
    if "groot" in code or "klein" in code:
        age = code[:5]
        group = int(code[5:])
        if age in schedules:
            if time:
                time = parser.parse(time)
            if not time: 
                time = datetime.datetime.now()
            try:
                ageschedule = schedules[age]
                print ageschedule
                current_activities = ageschedule[time]
                print current_activities
                activity = current_activities[group]
                return template('Je moet naar <b>{{activity}}</b>!', activity=activity)
            except KeyError:
                return template("Het is nog geen JOTARI. Je kunt ook een tijd proberen: \
                    <a href='{{group}}/19-10-2013%2010:00'>Zaterdag 10 uur</a>", group=code)
            except TypeError:
                return template("Het is nog geen JOTARI. Je kunt ook een tijd proberen: \
                    <a href='{{group}}/19-10-2013%2010:00'>Zaterdag 10 uur</a>", group=code)
    else:
        output = "<html>\n"
        time = parser.parse(code)
        for age,ageschedule in schedules.iteritems():
            current_activities = ageschedule[time]

            schedulestr = "<br>".join("{0}:{1}".format(k,v) for k,v in current_activities.iteritems())

            output += template("<b>{{age}}</b>:<br>{{!current_activities}}", 
                age=age, 
                current_activities=schedulestr)

            output += "<hr>"
        output += "</html>"
        return output


@post('/qr/reload')
@route('/qr/reload')
def reload():
    print "Pulling..."
    os.system("git pull")
    print "Pulled"

@route('/qr/log')
def log():
    with open("web.log") as f:
        content = f.read()
        content = content.replace("\n", "<br>\n")
        return content #template("!{{content}}", content=content)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True, reloader=True)
