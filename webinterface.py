#! /usr/bin/python
import os
from bottle import route, run, template, post
import datetime
from dateutil import parser
from csv_interface import build_interface

klein, groot = build_interface()
schedules = {"klein":klein, "groot":groot}

@route('/qr/<code>/')
@route('/qr/<code>')
@route('/qr/<code>/<time>/', defaults={'time': None})
@route('/qr/<code>/<time>', defaults={'time': None})
def qr(code='klein1', time=None):
    if "groot" in code or "klein" in code:
        return group(code, time)
    else:
        return schedule(code) #No group specified, interpret code as time

def find_next(age_sched, current_time, group, time_gap=1):
    current_activities = age_sched[current_time] #TODO: Set correct/current time!
    next_activity = "Onbekend"
    if current_activities:
        try:
            #Keep looking through the schedule until a next, different program is found. 
            next_activities = current_activities
            time_gap = 1
            #import ipdb; ipdb.set_trace()
            while next_activities == current_activities:
                next_activities = age_sched[current_time + datetime.timedelta(0,0,minutes=time_gap)] # days, seconds, then other fields.] #TODO: Set correct/current time!
                time_gap += 5
            print "Next program starts in {0} minutes".format(time_gap)
            next_activity = next_activities[group]
            return next_activity, time_gap
        except:
            pass

def group(code, time):
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

            next_activity, time_gap = find_next(ageschedule, time, group)

            return template('group', activity=activity, group=code, time=time, next_activity=next_activity, time_to_next=time_gap)
        except KeyError:
            return template("Het is nog geen JOTARI. Je kunt ook een tijd proberen: \
                <a href='{{group}}/18-10-2014%2010:00'>Zaterdag 10 uur</a>", group=code)
        except TypeError:
            return template("Het is nog geen JOTARI. Je kunt ook een tijd proberen: \
                <a href='{{group}}/18-10-2014%2010:00'>Zaterdag 10 uur</a>", group=code)

def schedule(time):
    time = parser.parse(time)

    k = {group:act for group,act in schedules['klein'][time].iteritems() if isinstance(group, int)}
    g = {group:act for group,act in schedules['groot'][time].iteritems() if isinstance(group, int)}

    return template('schedule', klein=k, groot=g, time=time)


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
