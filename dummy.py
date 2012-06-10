import sys
import time

for i in range(10):
	sys.stdout.write('Message {0}\n'.format(i))
	time.sleep(2)
