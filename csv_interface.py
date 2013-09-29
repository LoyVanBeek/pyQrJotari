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

class ScheduleFragment(object):
    """ A fragment of a schedule. Each fragment has assigned its own dictionary of programnames.
    When passed a time into __getitem__, it returns a list of program names, one for each group number."""
    def __init__(self, 
        filename, 
        programnamecells_area,
        datacells_area,
        format="%d-%m-%Y %H:%M", 
        groupcount=28):
        self.format = format
        self.groupcount = groupcount

        f = open(filename)
        arr = ScheduleFragment.csv_to_array(csv.reader(f))
        arr = ScheduleFragment.fill_blanks(arr, start_yx=datacells_area[0], end_yx=datacells_area[1])

        self.programtables = dict()
        self.programtables = ScheduleFragment.crop(arr, 
                            programnamecells_area[0], 
                            programnamecells_area[1])[0] #saturday, klein

        self._database = ScheduleFragment.crop(arr, datacells_area[0], datacells_area[1]) #All these 2-tuples are linked to the csv-file. 
 
    def query(self, querytime, groupnumber):
        #programtables is a dict mapping a (start, end)-tuple to an array of programnames
        row = self.find_row_for_time(self._database, querytime, self.format)
        programnames = self.programtables
        
        for cellno, cell in enumerate(row[2:]): #Skip date and time cells
            if isinstance(cell, list):
                if groupnumber in cell:
                    #pass
                    
                    #print (rowno, cellno)
                    #TODO lookup top row activities
                    activity = programnames[cellno]
                    return activity
            elif isinstance(cell, str): #The cell is a string, so all groups have that activity now.
                #print (rowno, cellno), cell
                return cell

    def has_key(self, querytime):
        try:
            return bool(self.find_row_for_time(self._database, querytime, self.format))
        except RowNotFoundException:
            return False

    def __getitem__(self, querytime):
        try:
            return dict([(groupnr, self.query(querytime, groupnr)) for groupnr in xrange(1, self.groupcount+1)])
        except:
            raise KeyError(querytime)

    @staticmethod
    def csv_to_array(reader):
        lines = [line for line in reader]

        for rowno, line in enumerate(lines):
            for cellno, cell in enumerate(line):
                try:
                    itemlist = cell.split(' ')
                    numberlist = [int(item) for item in itemlist]
                    if numberlist:
                        lines[rowno][cellno] = numberlist
                except ValueError:
                    #The cell did not contain only numbers.
                    pass
        return lines

    @staticmethod
    def find_above(array, row, col):
        if not array[row-1][col]:
            ScheduleFragment.find_above(array, row-1, col)
        else:
            return array[row-1][col]

    @staticmethod
    def fill_blanks(array, start_yx=(0,0), end_yx=(65536, 65536)):
        for rowno, line in enumerate(array):
            if start_yx[0] < rowno < end_yx[0]:
                for cellno, cell in enumerate(line):
                    if start_yx[1] < cellno < end_yx[1]:
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

    @staticmethod
    def find_row_for_time(array, querytime, format="%d-%m-%Y %H:%M"):
        for rowno, row in enumerate(array):
            #print row
            #import pdb; pdb.set_trace()
            starttime_cell = row[0]
            endtime_cell = row[1]
            if starttime_cell and endtime_cell:
                #starttime = datetime.datetime(*time.strptime(starttime_cell, format)[:6])
                #endtime = datetime.datetime(*time.strptime(endtime_cell, format)[:6])
                starttime = parser.parse(starttime_cell)
                endtime = parser.parse(endtime_cell)
                
                if starttime < querytime < endtime:
                    #import pdb; pdb.set_trace()
                    return row
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
    start = datetime.datetime(*time.strptime("20-10-2012 09:31", "%d-%m-%Y %H:%M")[:6])
    end   = datetime.datetime(*time.strptime("21-10-2012 15:30", "%d-%m-%Y %H:%M")[:6])
    curr  = start+datetime.timedelta(minutes=interval)
    
    while start <= curr < end:
        if s.has_key(curr):
            if None in s[curr].values():
                print "Groups {0} have no activity at {1}".format([k for k, v in s[curr].iteritems() if v == None], curr)
        else:
            print "No program defined at {0}".format(curr)
        curr += datetime.timedelta(minutes=interval)

class CellCoordParser(object):
    """Parse Excel's A1 and C6 etc to coordinate tuples and areas."""

    letters = list("ABCDEFHHIJKLMNOPQRSTUVWXYZ")

    @staticmethod
    def to_coord(coordstr, is_end=False):
        """ Parse cell coords to a tuple
        >>> CellCoordParser.to_coord("A1")
        (0, 0)
        >>> CellCoordParser.to_coord("A2")
        (0, 1)
        >>> CellCoordParser.to_coord("B1")
        (1, 0)
        >>> CellCoordParser.to_coord("B2")
        (1, 1)

        >>> CellCoordParser.to_coord("A1", is_end=True)
        (0, 0)
        >>> CellCoordParser.to_coord("A2", is_end=True)
        (0, 1)
        >>> CellCoordParser.to_coord("B1", is_end=True)
        (1, 0)
        >>> CellCoordParser.to_coord("B2", is_end=True)
        (1, 1)
        """
        letter = coordstr[0]
        column = CellCoordParser.letters.index(letter)
        row = int(coordstr[1]) - 1
        return (column, row)

    @staticmethod
    def to_area(start, end):
        """
        >>> CellCoordParser.to_area("C3", "I3") 
        ((2, 2),(9, 3))"""
        startcoord  = CellCoordParser.to_coord(start)
        endcoord    = CellCoordParser.to_coord(end)

        return startcoord, endcoord

def build_interface():
    path_klein = "data/planning_2012_edit_klein_commonPrograms_fixed_2.csv"
    path_groot = "data/planning_2012_groot_1.csv"

    saturday_prognames_klein = ((2,2),(3,9)) #3C t/m 3I
    saturday_data_area_klein = ((3,0), (32,9)) #5A t/m 33I

    sunday_prognames_klein = ((43,2), (44,7))
    sunday_data_area_klein = ((34,0), (53,7))

    saturday_prognames_groot_dag    = ((8,2), (9,8)) #9C t/m 9H
    saturday_data_area_groot_dag    = ((3,0), (23,8)) #4A t/m 23H

    saturday_prognames_groot_avond  = ((23,2), (24,8)) #24C tm 24H
    saturday_data_area_groot_avond  = ((24,0), (35,8)) #25A tm 35H

    #TODO: Fix for groot
    sunday_prognames_groot          = ((42,2), (43,7)) #43C tm 43G
    sunday_data_area_groot          = ((37,0), (56,7)) #38A tm 57G


    zat_klein = ScheduleFragment(path_klein, 
            programnamecells_area=saturday_prognames_klein, 
            datacells_area=saturday_data_area_klein)
    zon_klein = ScheduleFragment(path_klein, 
            programnamecells_area=sunday_prognames_klein, 
            datacells_area=sunday_data_area_klein)

    zat_groot_dag   = ScheduleFragment(path_groot, 
            saturday_prognames_groot_dag, 
            saturday_data_area_groot_dag, 
            groupcount=24)
    zat_groot_avond = ScheduleFragment(path_groot, 
            saturday_prognames_groot_avond, 
            saturday_data_area_groot_avond, 
            groupcount=24)
    zon_groot       = ScheduleFragment(path_groot, 
        sunday_prognames_groot, 
        sunday_data_area_groot, 
        groupcount=24)


    klein = Schedule(zat_klein, zon_klein)
    groot = Schedule(zat_groot_dag, zat_groot_avond, zon_groot)

    t0 = datetime.datetime(*time.strptime("20-10-2012 09:40", "%d-%m-%Y %H:%M")[:6])
    t1 = datetime.datetime(*time.strptime("20-10-2012 14:35", "%d-%m-%Y %H:%M")[:6])
    t2 = datetime.datetime(*time.strptime("20-10-2012 14:35", "%d-%m-%Y %H:%M")[:6])
    t3 = datetime.datetime(*time.strptime("21-10-2012 08:15", "%d-%m-%Y %H:%M")[:6])
    t4 = datetime.datetime(*time.strptime("21-10-2012 12:35", "%d-%m-%Y %H:%M")[:6])
    t5 = datetime.datetime(*time.strptime("22-10-2012 14:35", "%d-%m-%Y %H:%M")[:6]) #Monday after!
    t6 = datetime.datetime(*time.strptime("21-10-2012 08:35", "%d-%m-%Y %H:%M")[:6])
    t7 = datetime.datetime(*time.strptime("21-10-2012 13:35", "%d-%m-%Y %H:%M")[:6])

    # print "1: ", klein[datetime.datetime(*time.strptime("20-10-2012 14:35", "%d-%m-%Y %H:%M")[:6])][5]
    # print "2: ", klein[datetime.datetime(*time.strptime("20-10-2012 17:35", "%d-%m-%Y %H:%M")[:6])][5]
    # print "3: ", klein[datetime.datetime(*time.strptime("20-10-2012 18:35", "%d-%m-%Y %H:%M")[:6])][5]
    # print "4: ", klein[datetime.datetime(*time.strptime("20-10-2012 23:35", "%d-%m-%Y %H:%M")[:6])][5]

    print "ZATERDAG:"
    for groupnumber, activity in klein[t0].iteritems():
        print "klein"+str(groupnumber), activity

    for groupnumber, activity in klein[t1].iteritems():
        print "klein"+str(groupnumber), activity

    #print zon_klein.query(t4, 5)

    print "ZONDAG:"
    for groupnumber, activity in klein[t4].iteritems():
        print "klein"+str(groupnumber), activity

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

    


