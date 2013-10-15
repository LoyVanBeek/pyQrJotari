pyQrJotari
==========

Kids at http://www.scoutingboxtel.nl get a personal QR-code which they can scan during the Jotari-event. 
This program will look-up which activity is scheduled for each kid. 

TODO
----
- DONE: Make the UI blink when a new code is succesfully scanned
- DONE: Add images for this year's new activities
- DONE: Test this year's setup.
- Maybe do some refactoring in the event loop / polling of zbar
- DONE: Web interface! It reloads when I push to github using webhooks, really handy. Just adding more stuff to commit to test this out though :-(

Requirements
------------
- pip install PIL
- sudo apt-get install zbar*
