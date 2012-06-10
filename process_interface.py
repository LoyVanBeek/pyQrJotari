import subprocess
import time

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
