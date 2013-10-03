#!/usr/bin/python
#csv_interface.py
#This program expects the schedule to have all common programms to be completely filled out, 
#   to all occupied times and columns. 
#Empty cells are filled from to next filled cell above, 
#   which automatically fills in group numbers.
#Times must be complete, date and time.

import csv, time, datetime
from dateutil import parser

class RowNotFoundException(Exception):
    pass


class CellCoordParser(object):
    """Parse Excel's A1 and C6 etc to coordinate tuples and areas."""

    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    @staticmethod
    def to_coord(coordstr, is_end=False):
        """ Parse cell coords to a (column, row) tuple
        >>> CellCoordParser.to_coord("A1")
        (0, 0)
        >>> CellCoordParser.to_coord("A2")
        (0, 1)
        >>> CellCoordParser.to_coord("B1")
        (1, 0)
        >>> CellCoordParser.to_coord("B2")
        (1, 1)
        >>> CellCoordParser.to_coord("I32")
        (8, 31)

        >>> CellCoordParser.to_coord("A1", is_end=True)
        (1, 1)
        >>> CellCoordParser.to_coord("A2", is_end=True)
        (1, 2)
        >>> CellCoordParser.to_coord("B1", is_end=True)
        (2, 1)
        >>> CellCoordParser.to_coord("B2", is_end=True)
        (2, 2)
        """
        letter = coordstr[0]
        column = CellCoordParser.letters.index(letter) + (1 if is_end else 0)
        row = int(coordstr[1:]) - (1 if not is_end else 0)
        return (column, row)

    @staticmethod
    def to_area(start, end):
        """
        >>> CellCoordParser.to_area("C3", "I3") 
        ((2, 2), (9, 3))"""
        startcoord  = CellCoordParser.to_coord(start)
        endcoord    = CellCoordParser.to_coord(end, is_end=True)

        return startcoord, endcoord


class ExcelFile(object):
    """Wrapper around a csv file generated from Excel or LibreOffice"""

    def __init__(self, filename):
        f = open(filename)
        self.arr = ExcelFile.csv_to_array(csv.reader(f))

    @staticmethod
    def csv_to_array(reader):
        lines = [line for line in reader]

        for rowno, line in enumerate(lines):
            for cellno, cell in enumerate(line):
                try:
                    lines[rowno][cellno] = cell
                except ValueError:
                    #The cell did not contain only numbers.
                    pass
        return lines

    def __getitem__(self, coordstr):
        """
        >>> ef = ExcelFile("data/excel_test.csv")
        >>> ef['A1'] 
        'aap'
        >>> ef['A2'] 
        'mies'
        >>> ef['B1'] 
        'noot'
        >>> ef['B2'] 
        'vis'"""
        col, row = CellCoordParser.to_coord(coordstr)
        return self.arr[row][col]

    def get_area(self, start, end):
        """
        >>> ef = ExcelFile("data/excel_test.csv")
        >>> ef.get_area('A1','B1')
        [['aap', 'noot']]
        >>> ef.get_area('A2','B2')
        [['mies', 'vis']]
        >>> ef.get_area('A1','B2')
        [['aap', 'noot'], ['mies', 'vis']]
        """
        if isinstance(start, str) and isinstance(end, str):
            start, end = CellCoordParser.to_area(start, end)

        startcol, endcol = start[0], end[0]
        startrow, endrow = start[1], end[1]

        rows = self.arr[startrow:endrow]

        rows = [row[startcol:endcol] for row in rows]
        return rows


class ScheduleRow(ExcelFile):
    """A row in a jotari schedule."""

    def __init__(self, filename, row):
        ExcelFile.__init__(self, filename)
        self.arr = self.get_area(row+"1", end+"30")





class ScheduleFragment(ExcelFile):
    """ A fragment of a schedule. Each fragment has assigned its own dictionary of programnames.
    When passed a time into __getitem__, it returns a list of program names, one for each group number."""
    def __init__(   self, 
                    filename, 
                    programnamecells_area,
                    datacells_area,
                    base_day,
                    format="%d-%m-%Y %H:%M", 
                    groupcount=28):

        ExcelFile.__init__(self, filename)

        self.base_day = base_day
        self.format = format
        self.groupcount = groupcount

        self.programtables = dict()
        self.programtables = self.get_area(*programnamecells_area)[0]

        self._database = self.get_area(*datacells_area)

        self._database = self.parse_cells(self._database)
 
    def query(self, querytime, groupnumber):
        #programtables is a dict mapping a (start, end)-tuple to an array of programnames
        rowno = self.find_row_for_time(querytime, self.format)
        row = self._database[rowno-1] #because row_for_time should skip the Skip the van/tot rows
        #print row

        for cellno, cell in enumerate(row): #Skip date and time cells
            if isinstance(cell, list):
                if groupnumber in cell:
                    #pass
                    
                    #print (rowno, cellno)
                    #TODO lookup top row activities
                    activity = self.programtables[cellno]
                    return activity
            elif isinstance(cell, str): #The cell is a string, so all groups have that activity now.
                #print (rowno, cellno), cell
                return cell

    def has_key(self, querytime):
        try:
            self[querytime]
            return True
        except RowNotFoundException:
            return False

    @staticmethod
    def parse_intlist(intliststr):
        """Parse a list of ints represented as string to a real list of ints
        >>> ScheduleFragment.parse_intlist("1 2 3 4 5")
        [1, 2, 3, 4, 5]"""
        parts = intliststr.split(" ")
        return [int(part) for part in parts]

    def __getitem__(self, querytime):
        try:
            return {groupnr:self.query(querytime, groupnr) for groupnr in xrange(1, self.groupcount+1)}
        except RowNotFoundException:
            # import pprint
            # pprint.pprint(self.arr)
            raise KeyError(querytime)

    def parse_cells(self, array):
        for rowno, row in enumerate(array):
            for collno, cell in enumerate(row):
                try:
                    numberlist = self.parse_intlist(cell)
                    if numberlist:
                        array[rowno][collno] = numberlist
                except ValueError:
                    #The cell did not contain only numbers.
                    continue
        return array

    @staticmethod
    def find_above(array, row, col):
        if not array[row-1][col]:
            ScheduleFragment.find_above(array, row-1, col)
        else:
            return array[row-1][col]

    @staticmethod
    def fill_blanks(array, start_yx=(0,0), end_yx=(65536, 65536)):
        for rowno, line in enumerate(array):
            if start_yx[1] < rowno < end_yx[1]:
                for cellno, cell in enumerate(line):
                    if start_yx[0] < cellno < end_yx[0]:
                        try:
                            if not cell:
                                #Cell is empty, so get value from ABOVE
                                backup = ScheduleFragment.find_above(array, rowno, cellno)
                                #TODO: store backup
                                array[rowno][cellno] = backup
                        except ValueError:
                            #The cell did not contain only numbers.
                            pass
        return array

    @staticmethod
    def crop(array, start_yx, end_yx):
        """The cell as indicated by start_yx will move to [0][0] in the array.
        Everything outside the range, limited by end_yx will not be in the resulting array. """
        orig_width = len(array[0])
        assert all([len(row) == orig_width for row in array])
        orig_height = len(array)

        new_height = end_yx[0] - start_yx[0]
        new_width = end_yx[1] - start_yx[1]
        y_shift = start_yx[0]
        x_shift = start_yx[1]

        new = [row[start_yx[1]:end_yx[1]] for row in array[start_yx[0]:end_yx[0]]]
        return new

    def find_row_for_time(self, querytime, format="%d-%m-%Y %H:%M"):
        for rowno, row in enumerate(self.arr[2:]): #Skip the van/tot rows
            #print row
            #import pdb; pdb.set_trace()
            starttime_cell = row[0]
            endtime_cell = row[1]
            if starttime_cell and endtime_cell:
                start = self.base_day+" "+starttime_cell
                end = self.base_day+" "+endtime_cell
                #print start, end
                try:
                    starttime = parser.parse(start)
                    endtime = parser.parse(end)
                    
                    #import ipdb; ipdb.set_trace()
                    if starttime <= querytime < endtime:
                        #import pdb; pdb.set_trace()
                        return rowno
                except ValueError:
                    #Could not parse cells to times, so move to the next row.
                    #print "Could not parse {0} and {1} to datetimes".format(start, end)
                    pass
        raise RowNotFoundException("No row found for querytime {0}".format(querytime))

    @staticmethod
    def find_key_by_time(dic, querytime, format="%d-%m-%Y %H:%M"):
        #dic is a dictionary with a (starttime,endtime)-tuple for its keys
        for key,value in dic.iteritems():
            #print row

            starttime = key[0]
            endtime = key[1]
            
            if starttime < querytime < endtime:
                return value

class Schedule(object):
    """Hosts a set of ScheduleFragments to become one large, complete Schedule"""
    def __init__(self, *fragments):
        self.fragments = fragments

    def has_key(self, querytime):
        return any([fragment.has_key(querytime) for fragment in self.fragments])

    def __getitem__(self, querytime):
        for fragment in self.fragments:
            if fragment.has_key(querytime):
                return fragment[querytime]

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
    path_klein = "data/planning_2013_klein.csv"
    path_groot = "data/planning_2013_groot.csv"

    saturday_prognames_klein = CellCoordParser.to_area("C3", "I3")
    saturday_data_area_klein = CellCoordParser.to_area("C4", "I32")

    sunday_prognames_klein = CellCoordParser.to_area("C44", "G44")
    sunday_data_area_klein = CellCoordParser.to_area("C35", "G54")

    saturday_prognames_groot_dag    = CellCoordParser.to_area("C7", "I7")
    saturday_data_area_groot_dag    = CellCoordParser.to_area("C3", "I34")

    sat_eve_prognames_groot          = CellCoordParser.to_area("C22", "I22")
    sat_eve_data_area_groot          = CellCoordParser.to_area("C23", "I34")

    sunday_prognames_groot          = CellCoordParser.to_area("C44", "H44")
    sunday_data_area_groot          = CellCoordParser.to_area("C37", "I56")


    zat_klein = ScheduleFragment(path_klein, 
            programnamecells_area=saturday_prognames_klein, 
            datacells_area=saturday_data_area_klein,
            base_day="19-10-2013")

    zon_klein = ScheduleFragment(path_klein, 
            programnamecells_area=sunday_prognames_klein, 
            datacells_area=sunday_data_area_klein, 
            base_day="20-10-2013")

    zat_groot_dag   = ScheduleFragment(path_groot, 
            saturday_prognames_groot_dag, 
            saturday_data_area_groot_dag,
            base_day="19-10-2013",
            groupcount=24)

    zat_groot_avond = ScheduleFragment(path_groot, 
            sat_eve_prognames_groot, 
            sat_eve_data_area_groot,
            base_day="19-10-2013",
            groupcount=24)

    zon_groot       = ScheduleFragment(path_groot, 
            sunday_prognames_groot, 
            sunday_data_area_groot, 
            base_day="20-10-2013", 
            groupcount=24)


    klein = Schedule(zat_klein, zon_klein)
    groot = Schedule(zat_groot_dag, zat_groot_avond, zon_groot)

    return klein, groot


def generate_times(start, end, step=datetime.timedelta(minutes=5)):
    now = start
    while now <= end:
        yield now
        now += step

def export_program(schedule, filename):

    start = parser.parse("19-10-2013 09:30")
    end = parser.parse("20-10-2013 15:00")

    before_jump = start
    previous = {}

    columns = ["start"]
    columns += schedule[start].keys()

    with open(filename, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, columns)
        writer.writeheader()

        for time in generate_times( start, end):
            try:
                current = schedule[time]
                if previous != current:
                    print time, current

                    previous = current
                    before_jump = time

                    to_write = current.copy()
                    to_write["start"] = time
                    writer.writerow(to_write)
            except KeyError:
                pass        

def test(klein, groot):
    t0 = parser.parse("19-10-2013 09:40")
    t1 = parser.parse("19-10-2013 14:35")
    t2 = parser.parse("19-10-2013 14:35")
    t3 = parser.parse("20-10-2013 08:15")
    t4 = parser.parse("20-10-2013 12:35")
    t5 = parser.parse("21-10-2013 14:35") #Monday after!
    t6 = parser.parse("20-10-2013 08:35")
    t7 = parser.parse("20-10-2013 13:35")
    t8 = parser.parse("19-10-2013 10:05")

    # print "1: ", klein[datetime.datetime(*time.strptime("19-10-2012 14:35", "%d-%m-%Y %H:%M")[:6])][5]
    # print "2: ", klein[datetime.datetime(*time.strptime("19-10-2012 17:35", "%d-%m-%Y %H:%M")[:6])][5]
    # print "3: ", klein[datetime.datetime(*time.strptime("19-10-2012 18:35", "%d-%m-%Y %H:%M")[:6])][5]
    # print "4: ", klein[datetime.datetime(*time.strptime("19-10-2012 23:35", "%d-%m-%Y %H:%M")[:6])][5]

    print "ZATERDAG:"
    import ipdb; ipdb.set_trace()
    for groupnumber, activity in klein[t8].iteritems():
        print "klein"+str(groupnumber), activity

    for groupnumber, activity in klein[t1].iteritems():
        print "klein"+str(groupnumber), activity

    print "ZONDAG:"
    for groupnumber, activity in klein[t4].iteritems():
        print "klein"+str(groupnumber), activity

    print "#" * 20
    print "Groot"

    print "ZATERDAG {0}:".format(t1)
    for groupnumber, activity in groot[t1].iteritems():
        print "groot"+str(groupnumber), activity

    print "ZONDAG: {0}".format(t7)
    for groupnumber, activity in groot[t7].iteritems():
        print "groot"+str(groupnumber), activity


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    klein, groot = build_interface()
    
    # try:
    #     test(klein, groot)
    # except:
    #     pass

    #import ipdb; ipdb.set_trace()
    print groot[parser.parse("19-10-2013 13:05")]

    # export_program(klein, "klein_export.csv")
    # print "#"*20
    export_program(groot, "groot_export.csv")


    


