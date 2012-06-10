path = """/home/loy/Development/pyQrJotari/data/planning jotari template.csv"""
import csv
data = csv.reader(open(path))
timestrings = [row[0] for row in data][2:]#Remove the first 2 rows, as they contain stuff for humans

"""15/10/11 9:30"""
format = "%d/%m/%y %H:%M"
time.strptime(times[0], format)

timeslots = [time.strptime(time, format) for time in timestrings]
