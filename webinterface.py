#! /usr/bin/python
import os
from bottle import route, run, template, post
import datetime
from dateutil import parser
from csv_interface import build_interface
from leidingplanning import build_interface as leiding_interface
from bottledaemon import daemon_run
from collections import OrderedDict

klein, groot = build_interface()
schedules = {"klein":klein,
             "groot":groot}
leiding_planning = leiding_interface()

@route('/qr/<code>/')
@route('/qr/<code>')
@route('/qr/<code>/<time>/', defaults={'time': None})
@route('/qr/<code>/<time>', defaults={'time': None})
def qr(code='klein1', time=None):
    if "groot" in code or "klein" in code:
        return group(code, time)
    if 'leiding' in code:
        return leiding(code, time)
    else:
        return schedule(code) #No group specified, interpret code as time

def find_next(age_sched, current_time, group, time_gap=1):
    current_activities = dict(age_sched[current_time]) #TODO: Set correct/current time!
    next_activity = "Onbekend"
    if current_activities:
        try:
            #Keep looking through the schedule until a next, different program is found. 
            next_activities = current_activities
            time_gap = 1
            #import ipdb; ipdb.set_trace()
            while next_activities == current_activities:
                next_time = current_time + datetime.timedelta(0,0,minutes=time_gap)
                next_activities = dict(age_sched[next_time]) # days, seconds, then other fields.] #TODO: Set correct/current time!
                time_gap += 1
            print "Next program starts in {0} minutes".format(time_gap)
            next_activity = next_activities[group]
            return next_activity, time_gap
        except:
            pass

def group(code, time):
    parts = code.split(":")
    age = parts[0]
    group_ = int(parts[1])
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
            activity = current_activities[group_]

            next_activity, time_gap = find_next(ageschedule, time, group_)

            return template('group', activity=activity, age=age, group=str(group_), time=time, next_activity=next_activity, time_to_next=time_gap)
        except KeyError:
            return template("Het is nog geen JOTARI. Je kunt ook een tijd proberen: \
                <a href='{{group}}/17-10-2015%2010:00'>Zaterdag 10 uur</a>", group=code)
        except TypeError:
            return template("Het is nog geen JOTARI. Je kunt ook een tijd proberen: \
                <a href='{{group}}/17-10-2015%2010:00'>Zaterdag 10 uur</a>", group=code)

def leiding(code, time):
    parts = code.split(":")
    _ = parts[0]  # Should be 'leiding'
    speltak = parts[1]
    naam = parts[2]

    group_ = (speltak, naam)

    if time:
        time = parser.parse(time)
    if not time:
        time = datetime.datetime.now()

    try:
        current_activities = leiding_planning[time]
        print current_activities
        activity = current_activities[group_]

        next_activity, time_gap = find_next(leiding_planning, time, group_)

        return template('group', activity=activity, age='leiding', group="{} ({})".format(naam, speltak), time=time, next_activity=next_activity,
                        time_to_next=time_gap)
    except KeyError:
            return template("Het is nog geen JOTARI. Je kunt ook een tijd proberen: \
                <a href='{{group}}/17-10-2015%2010:00'>Zaterdag 10 uur</a>", group=code)


def schedule(time):
    time = parser.parse(time)

    leiding_at_time = OrderedDict(leiding_planning[time])
    leiding_at_time = OrderedDict(sorted(leiding_at_time.iteritems()))

    k = {group:act for group,act in schedules['klein'][time].iteritems() if isinstance(group, int)}
    g = {group:act for group,act in schedules['groot'][time].iteritems() if isinstance(group, int)}
    l = leiding_at_time

    return template('schedule', klein=k, groot=g, leiding=l, time=time)


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
