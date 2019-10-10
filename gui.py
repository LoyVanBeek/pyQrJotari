#!/usr/bin/python
import Tkinter as tk
import tkFont
import yaml
import pyQRjotari
from schedule_reading import csv_interface
from qr_reading import cv_scanner
import cv2


try:
    from PIL import Image, ImageTk
except ImportError:
    import Image, ImageTk #Works on windows
import logging
import profile

import sys
import platform

import time

logging.basicConfig(filename='qr.log', level=logging.DEBUG)

#GUI:
'''
----------------------------------
- [day][hour][minute][auto]
- Group <age><number>
- 'gaat naar'
- #<ActivityName><Image>#
- 'daarna'
- <NextActivityName>
- 
----------------------------------
'''

class QrJotariGui(object):

    def __init__(self, master, activities):
        self.act2img = self.load_images(activities)#dict([(name, tk.PhotoImage(Image.open(props['image']), height=200)) for name, props in activities.iteritems()])
        #print self.act2img

        master.title("JOTARI QR-codescanner")

        frame = tk.Frame(master, background='white')
        frame.pack(fill=tk.BOTH, expand=1)

        self.frame = frame

        self.customFont = tkFont.Font(family="Helvetica", size=50)
        
        self.dateframe = tk.Frame(frame, background='white')
        #Build the datecontrol frame
        self.dateframe.grid(row=1, columnspan=2, sticky=tk.E+tk.W)
        
        self.groupText = tk.StringVar()
        self.groupLabel = tk.Label(frame, textvariable=self.groupText, font=self.customFont, background='white')
        self.groupLabel.grid(row=2, columnspan=2, sticky=tk.E+tk.W)
                
        self.goto_firstLabel = tk.Label(frame, text="nu:", font=self.customFont, background='white')
        self.goto_firstLabel.grid(row=3, columnspan=2, sticky=tk.E+tk.W)
        
        # self.currentActivityFrame = tk.Frame(frame, background='white', width=600)
        
        self.activity_firstText = tk.StringVar()
        self.activity_firstLabel = tk.Label(frame, textvariable=self.activity_firstText, font=self.customFont, background='white')
        self.activity_firstLabel.grid(row=4, column=1, sticky=tk.W)#.pack(side=tk.LEFT, padx=20, pady=20)

        self.activity_firstImage = tk.PhotoImage(file="images/opening.gif", height=200)
        self.activity_firstImLbl = tk.Label(frame,  image=self.activity_firstImage, background='white')
        self.activity_firstImLbl.grid(row=4, column=2, sticky=tk.E)

        
        self.goto_secondLabel = tk.Label(frame, text="", font=self.customFont, background='white')
        self.goto_secondLabel.grid(row=5, columnspan=2, sticky=tk.E+tk.W)
        
        self.activity_secondText = tk.StringVar()
        self.activity_secondLabel = tk.Label(frame, textvariable=self.activity_secondText, font=self.customFont, background='white')
        self.activity_secondLabel.grid(row=6, column=1, sticky=tk.E+tk.W)

        self.cameraImage = tk.PhotoImage(file="images/opening.gif", height=180, width=240)
        self.cameraImLbl = tk.Label(frame,  image=self.cameraImage, background='white')
        self.cameraImLbl.grid(row=6, column=2, sticky=tk.E)

        self.first_activity()

    def first_activity(self):
        self.groupText.set("Iedereen")
        self.activity_firstText.set("Opening")
        self.activity_secondText.set("?")
        # import ipdb; ipdb.set_trace()
        self.activity_firstImLbl.configure(image=self.act2img['opening'])
    
    @staticmethod
    def load_images(activities):
        act2image_map = dict()#dict([(name, tk.PhotoImage(Image.open(props['image']), height=200)) for name, props in activities.iteritems()])
        # import ipdb; ipdb.set_trace()
        for name, props in activities.iteritems():
            path = props['image']
            try:
                im = Image.open(path)
                logging.debug("Loaded image for {}: {}".format(name, path))
            except IOError:
                print "Kon {0} niet laden".format(path)
                im = Image.open("images/onbekend.png")

            try:
                im = im.resize((300,300))
                logging.debug("Resized image for {}: {}".format(name, path))
            except IOError, ioe:
                print "Could not resize image {}".format(path)
                im = Image.open("images/onbekend.png")   

            try:
                #pi = tk.PhotoImage(file=path)
                pi = ImageTk.PhotoImage(im)
                act2image_map[name] = pi
                logging.debug("Added image for {}: {} to act2image_map".format(name, path))
            except Exception, e:
                print e
                print "Could not add image for {}".format(name)

        return act2image_map

    def set_backgrounds(self, color):
        for item in [self.frame, self.groupLabel,self.dateframe,self.goto_firstLabel,
                     self.activity_firstLabel,self.goto_secondLabel,self.activity_secondLabel]:
            item.config(background=color)

    def update(self, age, group, group_activity, current_time, image, next_activity=None, next_start=0):
        print "START update"
        print age, group, group_activity, current_time, image

        self.set_backgrounds('black')

        logging.info("\t{0}:{1} scanned at {3} for activity '{2}'".format(age, group, group_activity, current_time))

        hours = next_start // 60
        minutes = next_start - (hours * 60)
        next_start_str = "{h} uur en {m} minuten".format(h=hours, m=minutes)

        self.activity_firstImLbl.bell()

        self.groupText.set("Groep "+str(group))

        if hours == 0 and minutes > 5:
            self.activity_firstText.set(str(group_activity.capitalize()))
            self.activity_secondText.set("(over {1}:\n {0})".format(str(next_activity).capitalize(), next_start_str))

            if self.act2img.has_key(group_activity):
                img = self.act2img[group_activity]
                print img
                self.activity_firstImLbl.configure(image=img)
            else:
                print "No image defined for %s" % group_activity
        else:
            self.activity_firstText.set(str(next_activity.capitalize()))
            self.activity_secondText.set("(Begint over {0} minuten, \n NA {1})".format(minutes, group_activity))

            if self.act2img.has_key(next_activity):
                img = self.act2img[next_activity]
                print img
                self.activity_firstImLbl.configure(image=img)
            else:
                print "No image defined for %s" % next_activity


        time.sleep(0.3)
        self.set_backgrounds('white')
        print "END update"

    def update_camera(self, cv_bgr_img):
        # print "Got image: {}".format(cv_bgr_img.shape)
        cv_bgr_flipped_img = cv2.flip(cv_bgr_img, 1)
        cv_rgba_flipped_img = cv2.cvtColor(cv_bgr_flipped_img, cv2.COLOR_BGR2RGBA)

        dim = (self.cameraImage.width(), self.cameraImage.height())
        cv_resized = cv2.resize(cv_rgba_flipped_img, dim, interpolation=cv2.INTER_AREA)
        img_for_tk = Image.fromarray(cv_resized)
        imgtk = ImageTk.PhotoImage(image=img_for_tk)

        self.cameraImage.imgtk = imgtk
        self.cameraImLbl.configure(image=imgtk)


def check_images(activities, schedule):
    programs = []
    for time in schedule.schedule:
        programs += [prog.lower() for prog in time.values() if isinstance(prog, str)]

    unique_programs = set(programs)

    missing = unique_programs - set(activities.keys())
    return missing


def main(config, datetimeOverrule=None):
    schedules = [item['schedule'] for item in config if item.has_key("schedule")] #load schedule yaml-objects
    zbarcommands = [item['zbarcommand'] for item in config if item.has_key("zbarcommand")][0] #load schedule
    # import ipdb; ipdb.set_trace()
    zbarcommand = zbarcommands[platform.system()]

    klein, groot = csv_interface.build_interface()
    schedules = {"klein":klein, "groot":groot}

    activities = dict([(item['activity']['name'], item['activity']) for item in config if item.has_key("activity")])

    #print activities
    missing_images = check_images(activities, klein) | check_images(activities, groot)
    print "There is no image defined for activities" + "\n".join(missing_images)

    def update(*args):
        print args

    root = tk.Tk()

    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),
                                       root.winfo_screenheight()))
    root.configure(background='white')
    app = QrJotariGui(root, activities)

    backend = pyQRjotari.JotariQrBackend(schedules, app.update, datetimeOverrule=datetimeOverrule)
    scanner = cv_scanner.CvInterface(data_callback=backend.lookup)
    scanner.video_callback = app.update_camera
    scanner.start()

    def scan_update():
        scanner.tick()
        root.after(30, scan_update)
    root.after(10, scan_update)

    root.mainloop()
    print "Mainloop ended"
    scanner.force_stop()
    
if __name__ == "__main__":
    confpath = "configuration.yaml"
    conffile = open(confpath)
    config = yaml.load(conffile)

    datetimeOverrule = None
    try:
        datetimeOverrule = sys.argv[1] + " " + sys.argv[2]
        print "Override current_time with {0}".format(datetimeOverrule)
    except IndexError:
        print "You can optionally override the datetime for testing by passing a date: ./gui.py 18-10-2015 10:00"
        
    #profile.run("main(config)")
    main(config, datetimeOverrule)