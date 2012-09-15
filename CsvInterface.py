import csv, time

class Schedule(object):
	def __init__(self, filename, format="%d/%m/%y %H:%M"):
		with file(filename) as f:
			rawreader = csv.reader(f)
			self._matrix = [row for row in rawreader]
		
		self.format = format
		self._column_names = self._matrix[0]
		self._database = []
		for row in self._matrix[1:]: #Skip headers
			d = dict([(column_name, value) for column_name, value in zip(self._column_names, row)])
			#import pdb; pdb.set_trace()
			d['Start'] = time.strptime(d['Start'], self.format)
			d['Eind'] = time.strptime(d['Eind'], self.format)
			self._database += [d]
	
	def __getitem__(self, time):
		"""Query the schedule: if given a time, __getitem__ returns a list of group activity names, which is indexed by group number"""
		selection = [row for row in self._database if row['Start'] <= time and row['Eind'] > time]
		return selection[0]

if __name__ == "__main__":
	path = """/home/loy/Development/pyQrJotari/data/planning jotari template.csv"""
	
	format = "%d/%m/%y %H:%M" #"""15/10/11 9:30"""
	sched = Schedule(path, format)
	
	current_time_str = """15/10/11 9:40"""
	current = time.strptime(current_time_str, format)
	
	print sched[current]['7']
