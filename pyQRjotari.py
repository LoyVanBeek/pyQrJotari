#!/usr/bin/python
import yaml
import time, datetime
from dateutil import parser

dummy_time_str = """20-10-2012 20:01"""
current_time = datetime.datetime(*time.strptime(dummy_time_str, "%d-%m-%Y %H:%M")[:6])

class JotariQrBackend(object):
    def __init__(self, schedules, onScannedCB, datetimeOverrule=None):
        self.schedules = schedules
        self.onScannedCB = onScannedCB
        self.datetimeOverrule = datetimeOverrule
        
    def lookup(self, code):
        code = code.lower().strip()
        age = code[:5]
        group = int(code[5:])
        print "Code: {0} = {1}:{2}".format(code, age, group)
        
        ## import ipdb; ipdb.set_trace()
        if not self.datetimeOverrule:
            current_time = datetime.datetime.now()
        else:
            current_time = parser.parse(self.datetimeOverrule)

        try:
            #import ipdb; ipdb.set_trace()
            age_sched = self.schedules[age]
            current_activities = age_sched[current_time] 

            next_activity = "Onbekend"
            if current_activities:
                try:
                    #Keep looking through the schedule until a next, different program is found. 
                    next_activities = current_activities
                    time_gap = 1
                    # import ipdb; ipdb.set_trace()
                    while next_activities[group] == current_activities[group]:
                        next_activities = age_sched[current_time + datetime.timedelta(0,0,minutes=time_gap)] # days, seconds, then other fields.] #TODO: Set correct/current time!
                        time_gap += 1
                    print "Next program starts in {0} minutes".format(time_gap)
                    next_activity = next_activities[group]
                except:
                    pass
            
            group_activity = current_activities[group]
            group_activity = group_activity.lower()
            next_activity  = next_activity.lower()
            
            #print age, group, group_activity, time, None
            self.onScannedCB(age, group, group_activity, current_time, None,
                             next_activity=next_activity, next_start=time_gap) #age, group, activity, time, image
            return group_activity
        except KeyError, ke:
            print ke
            print "Haal Loy even, iets is er misgegaan!"
            # import pdb; pdb.set_trace()
            # self.wait_stop()
        except TypeError, te:
            print te
            print "Is het wel JOTARI? Er is geen programma op {0}.".format(current_time)
        # except Exception, ex:
        #     print ex


def main(config):
    from schedule_reading.csv_interface import build_interface
    # from qr_reading.cv_scanner import CvInterface
    from qr_reading.process_interface import ZBarInterface
    klein, groot = build_interface()

    schedules = {'klein':klein, "groot":groot}
    
    def update(*args):
        print args

    backend = JotariQrBackend(schedules, update)
    # scanner = CvInterface(data_callback=backend.lookup)
    scanner = ZBarInterface(callback=backend.lookup, command='zbarcam')

    scanner.start()
    scanner.wait_stop()
    
if __name__ == "__main__":
    confpath = "configuration.yaml"
    conffile = open(confpath)
    config = yaml.load(conffile)
        
    main(config)
