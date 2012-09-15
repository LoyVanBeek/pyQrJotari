#!/usr/bin/python
#csv_interface.py
#This program expects the schedule to have all common programms to be completely filled out, 
#   to all occupied times and columns. 
#Empty cells are filled from to next filled cell above, 
#   which automatically fills in group numbers.
#Times must be complete, date and time.

import csv, time, pprint

class RowNotFoundException(Exception):
    pass

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
        #arr = ScheduleFragment.fill_blanks(arr, start_yx=(4,3), end_yx=(32,10))

        self.programtables = dict()
        self.programtables[  (time.strptime("20-10-2012 09:30", "%d-%m-%Y %H:%M"), 
                            time.strptime("21-10-2012 00:00", "%d-%m-%Y %H:%M"))
                         ] = ScheduleFragment.crop(arr, 
                            programnamecells_area[0], 
                            programnamecells_area[1])[0] #saturday, klein
        # self.programtables[  (time.strptime("20-10-2012 09:30", "%d-%m-%Y %H:%M"), 
        #                     time.strptime("21-10-2012 00:00", "%d-%m-%Y %H:%M"))
        #                  ] = ScheduleFragment.crop(arr, (2,2),(3,9))[0] #saturday, klein

        self._database = ScheduleFragment.crop(arr, 
                                               datacells_area[0], datacells_area[1]) #All these 2-tuples are linked to the csv-file. 
        # self._database = ScheduleFragment.crop(arr, (4,0), (32,9)) #All these 2-tuples are linked to the csv-file. 
    def query(self, querytime, groupnumber):
        #programtables is a dict mapping a (start, end)-tuple to an array of programnames
        row = self.find_row_for_time(self._database, querytime, self.format)
        programnames = self.find_key_by_time(self.programtables, querytime, self.format)
        
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

    def has_key(self, time):
        try:
            return bool(self.find_row_for_time(self._database, time, self.format))
        except RowNotFoundException:
            return False

    def __getitem__(self, time):
        try:
            return dict([(groupnr, self.query(time, groupnr)) for groupnr in xrange(1, self.groupcount+1)])
        except:
            raise KeyError(time)

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

            starttime_cell = row[0]
            endtime_cell = row[1]

            starttime = time.strptime(starttime_cell, format)
            endtime = time.strptime(endtime_cell, format)
            
            if starttime < querytime < endtime:
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

def query(  arr, 
            querytime, 
            groupnumber,
            programtables,
            format="%d-%m-%Y %H:%M"):
    #programtables is a dict mapping a (start, end)-tuple to an array of programnames
    row = find_row_for_time(arr, querytime, format)
    programnames = find_key_by_time(programtables, querytime, format)
    
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


if __name__ == "__main__":
    path = "data/planning_2012_edit_klein_commonPrograms_fixed.csv"

    ZO_prognames = ((2,2),(3,9)) #3C t/m 3I
    ZO_data_area = ((4,0), (32,9)) #5A t/m 33I


    s = ScheduleFragment(path, 
            programnamecells_area=ZO_prognames, 
            datacells_area=ZO_data_area)
    print "1: ", s.query(time.strptime("20-10-2012 14:35", "%d-%m-%Y %H:%M"), 5)
    print "2: ", s.query(time.strptime("20-10-2012 17:35", "%d-%m-%Y %H:%M"), 5)
    print "3: ", s.query(time.strptime("20-10-2012 18:35", "%d-%m-%Y %H:%M"), 5)
    print "4: ", s.query(time.strptime("20-10-2012 23:35", "%d-%m-%Y %H:%M"), 5)

    t1 = time.strptime("20-10-2012 14:35", "%d-%m-%Y %H:%M")
    t5 = time.strptime("22-10-2012 14:35", "%d-%m-%Y %H:%M")
    for groupnumber, activity in s[t1].iteritems():
        print groupnumber, activity