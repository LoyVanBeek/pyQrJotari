#!/usr/bin/python
import opencv
from opencv import highgui 
import Image

import zbar

camera = highgui.cvCreateCameraCapture(0)

scanner = zbar.ImageScanner()
scanner.parse_config('enable')

while True:
	try:
		im = highgui.cvQueryFrame(camera)

		pil = opencv.adaptors.Ipl2PIL(im)
		raw = pil.tostring()

		image = zbar.Image(640, 480, 'Y800', raw)
		scanner.scan(image)

		for symbol in image:
			# do something useful with results
			#print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
			print symbol
		
		del(image)
		
	except KeyboardInterrupt:
		break
