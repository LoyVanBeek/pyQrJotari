#!/usr/bin/python
import Tkinter as tk
import tkFont
import yaml
import pyQRjotari
import csv_interface


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
        self.act2loc = dict([(name, props['location']) for name, props in activities.iteritems()])
        #print self.act2img

        master.title("JOTARI QR-codescanner")

        frame = tk.Frame(master, background='white')
        frame.pack(fill=tk.BOTH, expand=1)

        self.frame = frame

        self.customFont = tkFont.Font(family="Helvetica", size=50)
        
        self.dateframe = tk.Frame(frame, background='white')
        #Build the datecontrol frame
        self.dateframe.grid(row=1)#pack())
        
        self.groupText = tk.StringVar()
        self.groupLabel = tk.Label(frame, textvariable=self.groupText, font=self.customFont, background='white')
        self.groupLabel.grid(row=2)#pack()#tk.TOP
                
        self.goto_firstLabel = tk.Label(frame, text="nu:", font=self.customFont, background='white')
        self.goto_firstLabel.grid(row=3)#pack(side=tk.LEFT)
        
        self.currentActivityFrame = tk.Frame(frame, background='white', width=600)
        
        self.activity_firstText = tk.StringVar()
        self.activity_firstLabel = tk.Label(self.currentActivityFrame, textvariable=self.activity_firstText, font=self.customFont, background='white')
        self.activity_firstLabel.pack(side=tk.LEFT,
            padx=20, pady=20)

        self.activity_firstImage = tk.PhotoImage(file="images/opening.gif", height=200)
        self.activity_firstImLbl = tk.Label(self.currentActivityFrame, 
            image=self.activity_firstImage, 
            background='white')
        self.activity_firstImLbl.pack(side=tk.RIGHT,
            padx=20, pady=20)
        
        self.currentActivityFrame.grid(row=4,sticky=tk.N+tk.S+tk.E+tk.W)#pack()
        
        self.goto_secondLabel = tk.Label(frame, text="", font=self.customFont, background='white')
        self.goto_secondLabel.grid(row=5)#pack()
        
        self.activity_secondText = tk.StringVar()
        self.activity_secondLabel = tk.Label(frame, textvariable=self.activity_secondText, font=self.customFont, background='white')
        self.activity_secondLabel.grid(row=6)#pack()
        
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
                     self.currentActivityFrame,self.activity_firstLabel,self.goto_secondLabel,self.activity_secondLabel]:
            item.config(background=color)

    def update(self, age, group, group_activity, current_time, image, next_activity=None, next_start=0):
        print "START update"
        print age, group, group_activity, current_time, image

        self.set_backgrounds('black')

        logging.info("\t{0}:{1} scanned at {3} for activity '{2}'".format(age, group, group_activity, current_time))

        self.activity_firstImLbl.bell()

        self.groupText.set("Groep "+str(group))
        self.activity_firstText.set(str(group_activity.capitalize()) + "\n (" + self.act2loc[group_activity]+")")

        hours = next_start // 60
        minutes = next_start - (hours * 60)
        next_start_str = "{h} uur en {m} minuten".format(h=hours, m=minutes)
        next_loc_str = ", "+self.act2loc[next_activity] if self.act2loc[next_activity] else ""

        self.activity_secondText.set("(over {1}: {0}{2})".format(str(next_activity).capitalize(), next_start_str, next_loc_str))

        #import pdb; pdb.set_trace()
        if self.act2img.has_key(group_activity):
            img = self.act2img[group_activity]
            print img
            self.activity_firstImLbl.configure(image=img)
        else: 
            print "No image defined for %s" % group_activity

        time.sleep(0.3)
        self.set_backgrounds('white')
        print "END update"

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
    
    from csv_interface import build_interface

    klein, groot = build_interface()
    schedules = {"klein":klein, "groot":groot}

    activities = dict([(item['activity']['name'], item['activity']) for item in config if item.has_key("activity")])

    #print activities
    print check_images(activities, klein) | check_images(activities, groot)
    
    def update(*args):
        print args
        
    root = tk.Tk()
    
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),
                                       root.winfo_screenheight()))
    root.configure(background='white')
    app = QrJotariGui(root, activities)
    
    backend = pyQRjotari.JotariQrBackend(schedules, app.update, command=zbarcommand, datetimeOverrule=datetimeOverrule)
    backend.start()
    
    root.mainloop()
    print "Mainloop ended"
    backend.force_stop()
    
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