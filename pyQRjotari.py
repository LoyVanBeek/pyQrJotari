import yaml
import CsvInterface
import process_interface
import time

dummy_time_str = """15/10/11 9:40"""
dummy = time.strptime(dummy_time_str, CsvInterface.format)

class JotariQrBackend(object):
	def __init__(self, schedules, scannerClass, onScannedCB):
		self.schedules = schedules
		self.onScannedCB = onScannedCB
		
		self.scanner = scannerClass(self.lookup) 
		
	def lookup(self, code):
		code = code.lower().strip()
		age = code[:5]
		group = code[5:]
		print "Code: {0} = {1}:{2}".format(code, age, group)
		
		try:
			age_sched = schedules[age]
		except KeyError:
			print "Key {0} does not exist in".format(age)
			print "schedules: {1}".format(schedules)
		try:
			current_activities = age_sched[dummy]
		except KeyError:
			print "Key {0} does not exist in".format(dummy) #TODO: make this the current time
			print "current_activities: {1}".format(age_sched)
		try:
			group_activity = current_activities[group]
		except KeyError:
			print "Key {0} does not exist in".format(group)
			print "current_activities: {1}".format(current_activities)
		
		self.onScannedCB(age, group, activity, time, None) #age, group, activity, time, image
	
	def start(self):
		self.scanner.start()
	
	def stop(self):
		self.scanner.wait_stop()

def main(config):
	schedules = [item['schedule'] for item in config if item.has_key("schedule")] #load schedule yaml-objects
	schedules = dict([ (sched["age"], CsvInterface.Schedule(sched["path"])) for sched in schedules])
	
	def lookup(code):
		code = code.lower().strip()
		age = code[:5]
		group = code[5:]
		print "Code: {0} = {1}:{2}".format(code, age, group)
		
		try:
			age_sched = schedules[age]
		except KeyError:
			print "Key {0} does not exist in".format(age)
			print "schedules: {1}".format(schedules)
		
		current_activities = age_sched[dummy]
		group_activity = current_activities[group]
		print group_activity
	
	#lookup("Groot4")
	#'''
	zbar = process_interface.ZBarInterface(callback=lookup)
	zbar.start()
	'''
	while True:
		try:
			pass
		except KeyboardInterrupt:
			break
	'''
	zbar.wait_stop()
	#'''
	
if __name__ == "__main__":
	confpath = "configuration.yaml"
	conffile = open(confpath)
	config = yaml.load(conffile)
		
	main(config)
