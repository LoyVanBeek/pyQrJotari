#!/usr/bin/python
import Tkinter as tk
import tkFont
import yaml
import pyQRjotari
import csv_interface
from PIL import Image, ImageTk
import logging

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

        self.customFont = tkFont.Font(family="Helvetica", size=50)
        
        self.dateframe = tk.Frame(frame, background='white')
        #Build the datecontrol frame
        self.dateframe.grid(row=1)#pack())
        
        self.groupText = tk.StringVar()
        self.groupLabel = tk.Label(frame, textvariable=self.groupText, font=self.customFont, background='white')
        self.groupLabel.grid(row=2)#pack()#tk.TOP
                
        self.goto_firstLabel = tk.Label(frame, text="gaat naar", font=self.customFont, background='white')
        self.goto_firstLabel.grid(row=3)#pack(side=tk.LEFT)
        
        self.currentActivityFrame = tk.Frame(frame, background='white', width=600)
        
        self.activity_firstText = tk.StringVar()
        self.activity_firstLabel = tk.Label(self.currentActivityFrame, textvariable=self.activity_firstText, font=self.customFont, background='white')
        self.activity_firstLabel.pack(side=tk.LEFT,
            padx=20, pady=20)

        self.activity_firstImage = tk.PhotoImage(file="/home/loy/Development/pyQrJotari/images/tenten opzetten.GIF", height=200)
        self.activity_firstImLbl = tk.Label(self.currentActivityFrame, 
            image=self.activity_firstImage, 
            background='white')
        self.activity_firstImLbl.pack(side=tk.RIGHT,
            padx=20, pady=20)
        
        self.currentActivityFrame.grid(row=4,sticky=tk.N+tk.S+tk.E+tk.W)#pack()
        
        self.goto_secondLabel = tk.Label(frame, text="daarna", font=self.customFont, background='white')
        self.goto_secondLabel.grid(row=5)#pack()
        
        self.activity_secondText = tk.StringVar()
        self.activity_secondLabel = tk.Label(frame, textvariable=self.activity_secondText, font=self.customFont, background='white')
        self.activity_secondLabel.grid(row=6)#pack()
        
        self.groupText.set("Groep 1")
        self.activity_firstText.set("Avondspel")
        self.activity_secondText.set("Slapen")
        self.activity_firstImLbl.configure(image=self.act2img['opening'])
    
    @staticmethod
    def load_images(activities):
        map = dict()#dict([(name, tk.PhotoImage(Image.open(props['image']), height=200)) for name, props in activities.iteritems()])
        for name, props in activities.iteritems():
            im = Image.open(props['image'])
            im = im.resize((300,300))
            try:
                #pi = tk.PhotoImage(file=props['image'])
                pi = ImageTk.PhotoImage(im)
                map[name] = pi
            except:
                pass
        return map

    def update(self, age, group, group_activity, current_time, image, next_activity=None, next_start="wat"):
        print "START update"
        print age, group, group_activity, current_time, image

        logging.info("\t{0}:{1} scanned at {3} for activity '{2}'".format(age, group, group_activity, current_time))

        self.activity_firstImLbl.bell()

        self.groupText.set("Groep "+str(group))
        self.activity_firstText.set(str(group_activity.capitalize()))
        self.activity_secondText.set("{0}, {1} minuten later".format(str(next_activity).capitalize(), next_start))

        #import pdb; pdb.set_trace()
        if self.act2img.has_key(group_activity):
            img = self.act2img[group_activity]
            print img
            self.activity_firstImLbl.configure(image=img)
        else: 
            print "No image defined for %s" % group_activity
        print "END update"

def main(config):
    timeformat = [item['timeformat'] for item in config if item.has_key("timeformat")][0] #load timeformat markup
    schedules = [item['schedule'] for item in config if item.has_key("schedule")] #load schedule yaml-objects
    zbarcommand = str([item['zbarcommand'] for item in config if item.has_key("zbarcommand")][0]) #load schedule yaml-objects
    
    #import ipdb; ipdb.set_trace()
    path_klein = [schedule["path"] for schedule in schedules if schedule["age"] == "klein"][0]#"data/planning_2012_edit_klein_commonPrograms_fixed_2.csv"
    path_groot = [schedule["path"] for schedule in schedules if schedule["age"] == "groot"][0]#"data/planning_2012_groot_1.csv"

    saturday_prognames_klein = ((2,2),(3,9)) #3C t/m 3I
    saturday_data_area_klein = ((3,0), (32,9)) #5A t/m 33I

    sunday_prognames_klein = ((43,2), (44,7))
    sunday_data_area_klein = ((34,0), (53,7))

    saturday_prognames_groot_dag    = ((8,2), (9,8)) #9C t/m 9H
    saturday_data_area_groot_dag    = ((2,0), (23,8)) #4A t/m 23H

    saturday_prognames_groot_avond  = ((23,2), (24,8)) #24C tm 24H
    saturday_data_area_groot_avond  = ((24,0), (35,8)) #25A tm 35H

    sunday_prognames_groot          = ((42,2), (43,7)) #43C tm 43G
    sunday_data_area_groot          = ((37,0), (56,7)) #38A tm 57G


    zat_klein = csv_interface.ScheduleFragment(path_klein, 
            programnamecells_area=saturday_prognames_klein, 
            datacells_area=saturday_data_area_klein)
    zon_klein = csv_interface.ScheduleFragment(path_klein, 
            programnamecells_area=sunday_prognames_klein, 
            datacells_area=sunday_data_area_klein)

    zat_groot_dag   = csv_interface.ScheduleFragment(path_groot, 
            saturday_prognames_groot_dag, 
            saturday_data_area_groot_dag, 
            groupcount=24)
    zat_groot_avond = csv_interface.ScheduleFragment(path_groot, 
            saturday_prognames_groot_avond, 
            saturday_data_area_groot_avond, 
            groupcount=24)
    zon_groot       = csv_interface.ScheduleFragment(path_groot, 
        sunday_prognames_groot, 
        sunday_data_area_groot, 
        groupcount=24)

    klein = csv_interface.Schedule(zat_klein, zon_klein)
    groot = csv_interface.Schedule(zat_groot_dag, zat_groot_avond, zon_groot)


    schedules = {'klein':klein, "groot":groot}

    activities = dict([(item['activity']['name'], item['activity']) for item in config if item.has_key("activity")])

    #print activities
    
    def update(*args):
        print args
        
    root = tk.Tk()
    
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),
                                       root.winfo_screenheight()))
    root.configure(background='white')
    app = QrJotariGui(root, activities)
    
    backend = pyQRjotari.JotariQrBackend(schedules, app.update, command=zbarcommand)
    backend.start()
    
    root.mainloop()
    print "Mainloop ended"
    backend.force_stop()
    
if __name__ == "__main__":
    confpath = "configuration.yaml"
    conffile = open(confpath)
    config = yaml.load(conffile)
        
    main(config)