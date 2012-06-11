import subprocess
import time
import threading

def main():
	zbar = subprocess.Popen('zbarcam', #['python', 'dummy.py'],#
							stdout=subprocess.PIPE,
							universal_newlines=True,
							#bufsize=20,
							shell=False)

	#for line in zbar.stdout:
	#	print line

	while zbar.poll() == None:
		try:
			out = zbar.stdout.readline()
			if "QR-Code:" in out:
				out = out.strip("QR-Code:")
				print out
		except KeyboardInterrupt:
			print "Breaking..."
			break
	else:
		print "ZBar exited with exitcode {0}".format(zbar.returncode)

class ZBarInterface(object):
	def __init__(self, command="zbarcam", callback=None):
		self.command = command
		self.process = None
		self.thread = None
		self.callback = callback
		
	def start(self):
		self.thread = threading.Thread(target=self.run)
		self.thread.start()
		
	def force_stop(self):
		try:
			self.process.terminate()
		except OSError:
			print "process termination failed"
			pass
		
		try:
			self.thread.join()
		except:
			#print "Joining thread failed"
			exit()
	
	def wait_stop(self):
		try:
			self.thread.join()
		except:
			#print "Joining thread failed"
			exit()
		
	def run(self):
		self.process = subprocess.Popen(self.command,
				stdout=subprocess.PIPE,
				universal_newlines=True,
				shell=False)
		
		while self.process.poll() == None:
			try:
				out = self.process.stdout.readline()
				if "QR-Code:" in out:
					out = out.strip("QR-Code:")
					#print out
					if self.callback:
						self.callback(out)
			except:
				print "Trying to read did not work"
				self.wait_stop()
				break
		else:
			print "ZBar exited with exitcode {0}".format(self.process.returncode)
			self.wait_stop()

def dummy_callback(data):
	print "CB: ",data.capitalize()

def main2():
	zbar = ZBarInterface(callback=dummy_callback)
	zbar.start()
	
	'''
	while True:
		try:
			pass
		except KeyboardInterrupt:
			break
	zbar.stop()
	'''
	zbar.wait_stop()

if __name__ == "__main__":
	main2()
