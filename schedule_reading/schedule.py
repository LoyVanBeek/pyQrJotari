# Common classes for interpreting Jotari schedules

import datetime
from dateutil import parser


class memoize:
    def __init__(self, function):
        self.function = function
        self.memoized = {}

    def __call__(self, *args):
        try:
            return self.memoized[args]
        except KeyError:
            self.memoized[args] = self.function(*args)
            return self.memoized[args]


parse_time = memoize(parser.parse)


class RowNotFoundException(Exception):
    pass


class ScheduleFragment(object):
    """ A fragment of a schedule. Each fragment has assigned its own dictionary of programnames.
    When passed a time into __getitem__, it returns a list of program names, one for each group number."""

    def __init__(self, groupcount):
        # type: (int) -> None
        self.groupcount = groupcount

    def query(self, querytime, groupnumber):
        # type: (datetime.datetime, int) -> str
        raise NotImplementedError

    def has_key(self, querytime):
        # type: (datetime.datetime) -> bool
        try:
            _ = self[querytime]
            return True
        except RowNotFoundException:
            return False

    def __getitem__(self, querytime):
        # type: (datetime.datetime) -> dict
        try:
            return {groupnr: self.query(querytime, groupnr) for groupnr in xrange(1, self.groupcount + 1)}
        except RowNotFoundException:
            raise KeyError(querytime)


class Schedule(object):
    """Overall interface to a Schedule"""

    def __getitem__(self, querytime):
        # type: (datetime.datetime) -> dict
        raise NotImplementedError


def generate_times(start, end, step=datetime.timedelta(minutes=5)):
    """Like xrange for times...
    >>> times = list(generate_times(parse_time("19-10-2013 09:30"), parse_time("20-10-2013 16:00")))
    >>> assert parse_time("19-10-2013 14:00") in times
    >>> assert parse_time("20-10-2013 14:00") in times"""
    now = start
    while now <= end:
        yield now
        now += step


def export_program(schedule, filename):
    start = parse_time("19-10-2013 09:30")
    end = parse_time("20-10-2013 16:00")

    before_jump = start
    previous = {}

    columns = ["start"]
    columns += schedule[start].keys()

    with open(filename, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, columns)
        writer.writeheader()

        for time in generate_times(start, end):
            try:
                current = schedule[time]
                # if current and not previous: import ipdb; ipdb.set_trace();# current = schedule[time]
                if previous != current and current != None:
                    # print time, current

                    previous = current
                    before_jump = time

                    to_write = current.copy()
                    to_write["start"] = time
                    writer.writerow(to_write)
            except KeyError:
                print time
                pass


def test(klein, groot):
    t0 = parse_time("19-10-2013 09:40")
    t1 = parse_time("19-10-2013 14:35")
    t2 = parse_time("19-10-2013 14:35")
    t3 = parse_time("20-10-2013 08:15")
    t4 = parse_time("20-10-2013 12:35")
    t5 = parse_time("21-10-2013 14:35")  # Monday after!
    t6 = parse_time("20-10-2013 08:35")
    t7 = parse_time("20-10-2013 13:35")
    t8 = parse_time("19-10-2013 10:05")
    t9 = parse_time("19-10-2013 23:35")

    # print "1: ", klein[datetime.datetime(*time.strptime("19-10-2012 14:35", "%d-%m-%Y %H:%M")[:6])][5]
    # print "2: ", klein[datetime.datetime(*time.strptime("19-10-2012 17:35", "%d-%m-%Y %H:%M")[:6])][5]
    # print "3: ", klein[datetime.datetime(*time.strptime("19-10-2012 18:35", "%d-%m-%Y %H:%M")[:6])][5]
    # print "4: ", klein[datetime.datetime(*time.strptime("19-10-2012 23:35", "%d-%m-%Y %H:%M")[:6])][5]

    print "ZATERDAG:"
    # import ipdb; ipdb.set_trace()
    for groupnumber, activity in klein[t9].iteritems():
        print "klein" + str(groupnumber), activity

    for groupnumber, activity in klein[t1].iteritems():
        print "klein" + str(groupnumber), activity

    print "ZONDAG:"
    for groupnumber, activity in klein[t4].iteritems():
        print "klein" + str(groupnumber), activity

    print "#" * 20
    print "Groot"

    print "ZATERDAG {0}:".format(t1)
    for groupnumber, activity in groot[t1].iteritems():
        print "groot" + str(groupnumber), activity

    print "ZONDAG: {0}".format(t7)
    for groupnumber, activity in groot[t7].iteritems():
        print "groot" + str(groupnumber), activity