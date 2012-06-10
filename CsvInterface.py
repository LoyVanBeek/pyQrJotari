import csv, time

"""15/10/11 9:30"""
format = "%d/%m/%y %H:%M"

class Schedule(object):
	def __init__(self, filename):
		with file(filename) as f:
			rawreader = csv.reader(f)
			self._matrix = [row for row in rawreader]
		
		self._column_names = self._matrix[0]
		self._database = []
		for row in self._matrix[1:]: #Skip headers
			d = dict([(column_name, value) for column_name, value in zip(self._column_names, row)])
			#import pdb; pdb.set_trace()
			d['Start'] = time.strptime(d['Start'], format)
			d['Eind'] = time.strptime(d['Eind'], format)
			self._database += [d]
	
	def __getitem__(self, time):
		selection = [row for row in self._database if row['Start'] <= time and row['Eind'] > time]
		return selection[0]

if __name__ == "__main__":
	path = """/home/loy/Development/pyQrJotari/data/planning jotari template.csv"""
	
	sched = Schedule(path)
	
	current_time_str = """15/10/11 9:40"""
	current = time.strptime(current_time_str, format)
	
	print sched[current]['7']
