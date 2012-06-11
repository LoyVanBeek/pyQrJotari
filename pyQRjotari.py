import yaml
import CsvInterface
import process_interface
import time

dummy_time_str = """15/10/11 9:40"""
time = time.strptime(dummy_time_str, CsvInterface.format)

class JotariQrBackend(object):
	def __init__(self, schedules, scannerClass, onScannedCB):
		self.schedules = schedules
		self.onScannedCB = onScannedCB
		
		self.scanner = scannerClass(callback=self.lookup) 
		
	def lookup(self, code):
		code = code.lower().strip()
		age = code[:5]
		group = code[5:]
		print "Code: {0} = {1}:{2}".format(code, age, group)
		
		try:
			age_sched = self.schedules[age]
			current_activities = age_sched[time]
			group_activity = current_activities[group]
			
			print age, group, group_activity, time, None
			#self.onScannedCB(age, group, activity, time, None) #age, group, activity, time, image
		except KeyError, ke:
			print ke
			self.wait_stop()
		except Exception, ex:
			print ex
	
	def start(self):
		self.scanner.start()
	
	def wait_stop(self):
		self.scanner.wait_stop()

def main(config):
	schedules = [item['schedule'] for item in config if item.has_key("schedule")] #load schedule yaml-objects
	schedules = dict([ (sched["age"], CsvInterface.Schedule(sched["path"])) for sched in schedules])
	
	def update(*args):
		print args
	
	backend = JotariQrBackend(schedules, process_interface.ZBarInterface, update)
	backend.start()
	backend.wait_stop()
	
if __name__ == "__main__":
	confpath = "configuration.yaml"
	conffile = open(confpath)
	config = yaml.load(conffile)
		
	main(config)
