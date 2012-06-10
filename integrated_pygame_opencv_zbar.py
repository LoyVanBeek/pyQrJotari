#!/usr/bin/python
import pygame
import opencv
from opencv import highgui 
import Image
import zbar
import sys

from pygame.locals import *

print "zbar.version() = {0}.{1}".format(*zbar.version())

def main():
	camera = highgui.cvCreateCameraCapture(0)
	
	scanner = zbar.ImageScanner()
	scanner.parse_config('enable')
	
	def get_image():
		#print "Quering camera"
		cv_im = highgui.cvQueryFrame(camera)
		# Add the line below if you need it (Ubuntu 8.04+)
		#im = opencv.cvGetMat(im)
		#convert Ipl image to PIL image
		#print "Converting to PIL"
		return opencv.adaptors.Ipl2PIL(cv_im) 

	fps = 30.0
	pygame.init()
	window = pygame.display.set_mode((640,480))
	pygame.display.set_caption("QR WebCam Demo")
	screen = pygame.display.get_surface()

	while True:
		try:
			#print "Starting new iteration"
			events = pygame.event.get()
			for event in events:
				if event.type == QUIT or event.type == KEYDOWN:
					print "Exiting..."
					pygame.quit()
					sys.exit(0)
			
			pil_im = get_image()
			
			raw = pil_im.tostring()
			zbar_im = zbar.Image(pil_im.size[0], pil_im.size[1], 'Y800', raw)
			#print "Scanning image..."
			scanner.scan(zbar_im)
			
			for symbol in zbar_im: 
				# do something useful with results
				#print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
				print "decoded {0.type} : {0.data}, {0.location}".format(symbol, type=symbol.type, data=symbol.data)
				#If there are 4 point in the BB
				if len(symbol.location) >= 4:
					pygame.draw.lines(screen, (0,255,0), False, symbol.location, 2) #see http://www.cs.ucsb.edu/~pconrad/cs5nm/topics/pygame/drawing/
			
			#print "Blitting to screen"
			pg_img = pygame.image.frombuffer(pil_im.tostring(), pil_im.size, pil_im.mode)
			screen.blit(pg_img, (0,0))
			pygame.display.flip()
			pygame.time.delay(int(1000 * 1.0/fps))
			#print "End of iteration"
		except Exception, e:
			pygame.quit()
			sys.exit(0)
	return 0

if __name__ == '__main__':
	main()
