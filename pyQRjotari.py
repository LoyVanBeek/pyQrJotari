#!/usr/bin/python
import yaml
import process_interface
import time, datetime
from dateutil import parser

dummy_time_str = """20-10-2012 20:01"""
current_time = datetime.datetime(*time.strptime(dummy_time_str, "%d-%m-%Y %H:%M")[:6])

class JotariQrBackend(object):
    def __init__(self, schedules, onScannedCB, scannerClass=process_interface.ZBarInterface, command="zbarcam"):
        self.schedules = schedules
        self.onScannedCB = onScannedCB
        
        self.scanner = scannerClass(callback=self.lookup, command=command) 
        
    def lookup(self, code):
        code = code.lower().strip()
        age = code[:5]
        group = int(code[5:])
        print "Code: {0} = {1}:{2}".format(code, age, group)
        
        ## import ipdb; ipdb.set_trace()
        current_time = datetime.datetime.now()
        #current_time = parser.parse("19-10-2013 20:01")

        try:
            #import ipdb; ipdb.set_trace()
            age_sched = self.schedules[age]
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
                except:
                    pass
            
            group_activity = current_activities[group]
            group_activity = group_activity.lower()
            next_activity  = next_activity.lower()
            
            #print age, group, group_activity, time, None
            self.onScannedCB(age, group, group_activity, current_time, None, next_activity=next_activity,next_start=time_gap) #age, group, activity, time, image
        except KeyError, ke:
            print ke
            print "Haal Loy even, iets is er misgegaan!"
            import pdb; pdb.set_trace()
            self.wait_stop()
        except TypeError, te:
            print "Is het wel JOTARI? Er is geen programma op {0}.".format(current_time)
        except Exception, ex:
            print ex
    
    def start(self):
        self.scanner.start()
    
    def wait_stop(self):
        self.scanner.wait_stop()
        
    def force_stop(self):
        self.scanner.force_stop()

def main(config):
    from csv_interface import build_interface
    klein, groot = build_interface()

    schedules = {'klein':klein, "groot":groot}
    
    def update(*args):
        print args
    
    backend = JotariQrBackend(schedules, update, command="zbarcam /dev/video1")
    backend.start()
    backend.wait_stop()
    
if __name__ == "__main__":
    confpath = "configuration.yaml"
    conffile = open(confpath)
    config = yaml.load(conffile)
        
    main(config)
