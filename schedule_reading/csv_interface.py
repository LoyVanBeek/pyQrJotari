#!/usr/bin/env python

#csv_interface.py
#This program expects the schedule to have all common programms to be completely filled out, 
#   to all occupied times and columns. 
#Empty cells are filled from to next filled cell above, 
#   which automatically fills in group numbers.
#Times must be complete, date and time.

import csv, time, datetime
import yaml
from schedule import parse_time, Schedule, export_program


class SimpleCsvSchedule(Schedule):
    """Parse and query a more simple format. Columns have headers (start,end, N group numbers).
    Each row has a start and end date."""

    def __init__(self, filename):
        self.schedule = list(self.parse(filename))

    @staticmethod
    def parse(filename):
        schedule = csv.DictReader(open(filename))
        for row in schedule:
            try:
                row["start"] = parse_time(row["start"])
                row["eind"] = parse_time(row["eind"])
                groupkeys = [k for k in row if k.isdigit()]
                for group in groupkeys:
                    row[int(group)] = row[group] #Copy string key to int
                    del row[group] #delete the string version of the key.
                yield row
            except ValueError, ve:
                print ve, row
                import ipdb; ipdb.set_trace()

    def __getitem__(self, querytime):
        for timeslot in self.schedule:
            if timeslot["start"] <= querytime < timeslot["eind"]:
                return timeslot
        else:
            raise KeyError("There is no program on {0}".format(querytime))


def check_program(interval=10):
    start = datetime.datetime(*time.strptime("19-10-2013 09:31", "%d-%m-%Y %H:%M")[:6])
    end   = datetime.datetime(*time.strptime("20-10-2013 15:30", "%d-%m-%Y %H:%M")[:6])
    curr  = start+datetime.timedelta(minutes=interval)
    
    while start <= curr < end:
        if s.has_key(curr):
            if None in s[curr].values():
                print "Groups {0} have no activity at {1}".format([k for k, v in s[curr].iteritems() if v == None], curr)
        else:
            print "No program defined at {0}".format(curr)
        curr += datetime.timedelta(minutes=interval)


def build_interface():
    confpath = "configuration.yaml"
    conffile = open(confpath)
    config = yaml.load(conffile)

    schedule_config = {item['schedule']['age']:item['schedule']['path'] for item in
                       [item for item in config if "schedule" in item.keys()]}
    path_klein = schedule_config['klein']
    path_groot = schedule_config['groot']
    
    klein = SimpleCsvSchedule(path_klein)
    groot = SimpleCsvSchedule(path_groot)

    return klein, groot


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    klein, groot = build_interface()
    
    # try:
    #     test(klein, groot)
    # except:
    #     import ipdb; ipdb.pm()
    #     pass

    #import ipdb; ipdb.set_trace()
    #print klein[parse_time("19-10-2013 13:05")]

    export_program(klein, "klein_export.csv")
    # print "#"*20
    export_program(groot, "groot_export.csv")


    


