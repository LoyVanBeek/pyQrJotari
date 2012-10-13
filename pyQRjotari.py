#!/usr/bin/python
import yaml
import csv_interface
import process_interface
import time, datetime

dummy_time_str = """21-10-2012 11:01"""
current_time = datetime.datetime(*time.strptime(dummy_time_str, "%d-%m-%Y %H:%M")[:6])

class JotariQrBackend(object):
    def __init__(self, schedules, onScannedCB, scannerClass=process_interface.ZBarInterface):
        self.schedules = schedules
        self.onScannedCB = onScannedCB
        
        self.scanner = scannerClass(callback=self.lookup) 
        
    def lookup(self, code):
        code = code.lower().strip()
        age = code[:5]
        group = int(code[5:])
        print "Code: {0} = {1}:{2}".format(code, age, group)
        
        #import ipdb; ipdb.set_trace()
        current_time = datetime.datetime.now()

        try:
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
        except Exception, ex:
            print ex
    
    def start(self):
        self.scanner.start()
    
    def wait_stop(self):
        self.scanner.wait_stop()
        
    def force_stop(self):
        self.scanner.force_stop()

def main(config):
    timeformat = [item['timeformat'] for item in config if item.has_key("timeformat")][0] #load timeformat markup
    schedules = [item['schedule'] for item in config if item.has_key("schedule")] #load schedule yaml-objects

    path_klein = "data/planning_2012_edit_klein_commonPrograms_fixed_2.csv"
    path_groot = "data/planning_2012_groot_1.csv"

    saturday_prognames_klein = ((2,2),(3,9)) #3C t/m 3I
    saturday_data_area_klein = ((3,0), (32,9)) #5A t/m 33I

    sunday_prognames_klein = ((43,2), (44,7))
    sunday_data_area_klein = ((34,0), (53,7))

    saturday_prognames_groot_dag    = ((8,2), (9,8)) #9C t/m 9H
    saturday_data_area_groot_dag    = ((2,0), (23,8)) #4A t/m 23H

    saturday_prognames_groot_avond  = ((23,2), (24,8)) #24C tm 24H
    saturday_data_area_groot_avond  = ((24,0), (35,8)) #25A tm 35H

    sunday_prognames_groot          = ((42,2), (43,7)) #43C tm 43G
    sunday_data_area_groot          = ((37,0), (56,7)) #38A tm 57G


    zat_klein = csv_interface.ScheduleFragment(path_klein, 
            programnamecells_area=saturday_prognames_klein, 
            datacells_area=saturday_data_area_klein)
    zon_klein = csv_interface.ScheduleFragment(path_klein, 
            programnamecells_area=sunday_prognames_klein, 
            datacells_area=sunday_data_area_klein)

    zat_groot_dag   = csv_interface.ScheduleFragment(path_groot, 
            saturday_prognames_groot_dag, 
            saturday_data_area_groot_dag, 
            groupcount=24)
    zat_groot_avond = csv_interface.ScheduleFragment(path_groot, 
            saturday_prognames_groot_avond, 
            saturday_data_area_groot_avond, 
            groupcount=24)
    zon_groot       = csv_interface.ScheduleFragment(path_groot, 
        sunday_prognames_groot, 
        sunday_data_area_groot, 
        groupcount=24)


    klein = csv_interface.Schedule(zat_klein, zon_klein)
    groot = csv_interface.Schedule(zat_groot_dag, zat_groot_avond, zon_groot)


    schedules = {'klein':klein, "groot":groot}
    
    def update(*args):
        print args
    
    backend = JotariQrBackend(schedules, update)
    backend.start()
    backend.wait_stop()
    
if __name__ == "__main__":
    confpath = "configuration.yaml"
    conffile = open(confpath)
    config = yaml.load(conffile)
        
    main(config)
