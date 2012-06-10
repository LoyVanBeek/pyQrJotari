#!/usr/bin/python
import pygame
import opencv
from opencv import highgui 
import Image
import zbar
import sys

from pygame.locals import *

print "zbar.version() = {0}.{1}".format(*zbar.version())

def main(impath):
	cv_im = highgui.cvLoadImage(impath)
	opencv.adaptors.Ipl2PIL(cv_im) 
	
	scanner = zbar.ImageScanner()
	scanner.parse_config('enable')
	
	fps = 30.0
	pygame.init()
	window = pygame.display.set_mode((640,480))
	pygame.display.set_caption("QR WebCam Demo")
	screen = pygame.display.get_surface()
	
	pil_im = opencv.adaptors.Ipl2PIL(cv_im)
	
	raw = pil_im.tostring()
	zbar_im = zbar.Image(pil_im.size[0], pil_im.size[1], 'Y800', raw)
	
	import pdb; pdb.set_trace()
	scanner.scan(zbar_im)
	print list(zbar_im)
	
	for symbol in zbar_im:
		# do something useful with results
		#print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
		print "decoded {0.type} : {0.data}, {0.location}".format(symbol, type=symbol.type, data=symbol.data)
		#If there are 4 point in the BB
		if len(symbol.location) >= 4:
			pygame.draw.lines(screen, (0,255,0), False, symbol.location, 2) #see http://www.cs.ucsb.edu/~pconrad/cs5nm/topics/pygame/drawing/
	
	#print "Blitting to screen"
	pg_img = pygame.image.frombuffer(pil_im.tostring(), pil_im.size, pil_im.mode)
	
	while True:
		try:
			events = pygame.event.get()
			for event in events:
				if event.type == QUIT or event.type == KEYDOWN:
					print "Exiting..."
					pygame.display.quit()
					#pygame.quit()
					#sys.exit(0)
					return
					
			screen.blit(pg_img, (0,0))
			pygame.display.flip()
			pygame.time.delay(int(1000 * 1.0/fps))
		except:
			#pygame.quit()
			#sys.exit(0)
			return

if __name__ == "__main__":
	impath = sys.argv[1]
	print "Displaying image '{0}'".format(impath)
	main(impath)
	#pygame.quit()
