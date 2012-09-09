#!/usr/bin/python
#csv_interface.py
#This program expects the schedule to have all common programms to be completely filled out, 
#   to all occupied times and columns. 
#Empty cells are filled from to next filled cell above, 
#   which automatically fills in group numbers.
#Times must be complete, date and time.


import csv, time, pprint

class Schedule(object):
    """When passed a time into __get_item__, it returns a list of program names, one for each group number."""
    def __init__(self, filename, format="%d-%m-%Y %H:%M"):
        self.format = format

        f = open(filename)
        arr = csv_to_array(csv.reader(f))
        arr = fill_blanks(arr, start_yx=(4,3), end_yx=(32,10))

        self.programtables = dict()
        self.programtables[  (time.strptime("20-10-2012 09:30", "%d-%m-%Y %H:%M"), 
                            time.strptime("21-10-2012 00:00", "%d-%m-%Y %H:%M"))
                         ] = crop(arr, (2,2), (3,9))[0] #saturday, klein

        self._database = crop(arr, (4,0), (32,9)) #All these 2-tuples are linked to the csv-file. 

    def query(self,
                querytime, 
                groupnumber):
        #programtables is a dict mapping a (start, end)-tuple to an array of programnames
        row = find_row_for_time(self._database, querytime, self.format)
        programnames = find_key_by_time(self.programtables, querytime, self.format)
        
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

def find_above(array, row, col):
    if not array[row-1][col]:
        find_above(array, row-1, col)
    else:
        return array[row-1][col]

def fill_blanks(array, start_yx=(0,0), end_yx=(65536, 65536)):
    for rowno, line in enumerate(array):
        if start_yx[0] < rowno < end_yx[0]:
            for cellno, cell in enumerate(line):
                if start_yx[1] < cellno < end_yx[1]:
                    try:
                        if not cell:
                            #Cell is empty, so get value from ABOVE
                            backup = find_above(array, rowno, cellno)
                            #TODO: store backup
                            array[rowno][cellno] = backup
                    except ValueError:
                        #The cell did not contain only numbers.
                        pass
    return array

def crop(array, start_yx, end_yx):
    orig_width = len(array[0])
    assert all([len(row) == orig_width for row in array])
    orig_height = len(array)

    new_height = end_yx[0] - start_yx[0]
    new_width = end_yx[1] - start_yx[1]
    y_shift = start_yx[0]
    x_shift = start_yx[1]

    new = [row[start_yx[1]:end_yx[1]] for row in array[start_yx[0]:end_yx[0]]]
    return new

def find_row_for_time(array, querytime, format="%d-%m-%Y %H:%M"):
    for rowno, row in enumerate(arr):
        #print row

        starttime_cell = row[0]
        endtime_cell = row[1]

        starttime = time.strptime(starttime_cell, format)
        endtime = time.strptime(endtime_cell, format)
        
        if starttime < querytime < endtime:
            return row

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

    arr = csv_to_array(csv.reader(open(path)))
    # print "Orig:"
    # for index, row in enumerate(arr):
    #     print index, ":", row#pprint.pprint(row)

    program_names_saturday_klein = crop(arr, (2,2), (3,9))[0]
    # print "program_names_saturday_klein: "
    # pprint.pprint(program_names_saturday_klein)

    programnames = dict()
    programnames[(time.strptime("20-10-2012 09:30", "%d-%m-%Y %H:%M"), time.strptime("21-10-2012 00:00", "%d-%m-%Y %H:%M"))] = program_names_saturday_klein

    arr = fill_blanks(arr, start_yx=(4,3), end_yx=(32,10))
    # print "Filled blanks:"
    # for index, row in enumerate(arr):
    #     print index, ":", row#pprint.pprint(row)

    arr = crop(arr, (4,0), (32,9))
    # print "Cropped:"
    # for index, row in enumerate(arr):
    #     print index, ":", row#pprint.pprint(row)

    s = Schedule(path)
    print "1: ", s.query(time.strptime("20-10-2012 14:35", "%d-%m-%Y %H:%M"), 5)
    print "2: ", s.query(time.strptime("20-10-2012 17:35", "%d-%m-%Y %H:%M"), 5)
    print "3: ", s.query(time.strptime("20-10-2012 18:35", "%d-%m-%Y %H:%M"), 5)
    print "4: ", s.query(time.strptime("20-10-2012 23:35", "%d-%m-%Y %H:%M"), 5)