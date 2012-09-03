#csv_interface.py
#This program expects the schedule to have all common programms to be completely filled out, 
#   to all occupied times and columns. 
#Empty cells are filled from to next filled cell above, 
#   which automatically fills in group numbers.


import csv

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

def fill_blanks(array, startcell=(0,0), endcell=(65536, 65536)):
    for rowno, line in enumerate(array):
        if startcell[0] < rowno < endcell[0]:
            for cellno, cell in enumerate(line):
                if startcell[1] < cellno < endcell[1]:
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


if __name__ == "__main__":
    path = "data/planning_2012_edit_klein_commonPrograms_fixed.csv"
    arr = csv_to_array(csv.reader(open(path)))
    arr = fill_blanks(arr, startcell=(4,3), endcell=(32,10))
    for row in arr:
        print row