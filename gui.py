import Tkinter as tk
import tkFont
import yaml
import pyQRjotari
import CsvInterface
from PIL import Image, ImageTk

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
        print self.act2img

        frame = tk.Frame(master)
        frame.grid(sticky=tk.N+tk.S+tk.E+tk.W)

        self.customFont = tkFont.Font(family="Helvetica", size=50)
        
        self.dateframe = tk.Frame(frame)
        #Build the datecontrol frame
        self.dateframe.grid(row=1)#pack())
        
        self.groupText = tk.StringVar()
        self.groupLabel = tk.Label(frame, textvariable=self.groupText, font=self.customFont)
        self.groupLabel.grid(row=2)#pack()#tk.TOP
                
        self.goto_firstLabel = tk.Label(frame, text="gaat naar", font=self.customFont)
        self.goto_firstLabel.grid(row=3)#pack(side=tk.LEFT)
        
        self.currentActivityFrame = tk.Frame(frame)
        
        self.activity_firstText = tk.StringVar()
        self.activity_firstLabel = tk.Label(self.currentActivityFrame, textvariable=self.activity_firstText, font=self.customFont)
        self.activity_firstLabel.pack(side=tk.LEFT)
        self.activity_firstImage = tk.PhotoImage(file="/home/loy/Development/pyQrJotari/images/tenten opzetten.GIF", height=200)
        self.activity_firstImLbl = tk.Label(self.currentActivityFrame, image=self.activity_firstImage)
        self.activity_firstImLbl.pack(side=tk.RIGHT)
        
        self.currentActivityFrame.grid(row=4,sticky=tk.N+tk.S+tk.E+tk.W)#pack()
        
        self.goto_secondLabel = tk.Label(frame, text="daarna", font=self.customFont)
        self.goto_secondLabel.grid(row=5)#pack()
        
        self.activity_secondText = tk.StringVar()
        self.activity_secondLabel = tk.Label(frame, textvariable=self.activity_secondText, font=self.customFont)
        self.activity_secondLabel.grid(row=6)#pack()
        
        self.groupText.set("Groep 1")
        self.activity_firstText.set("Avondspel")
        self.activity_secondText.set("Slapen")
    
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

    def update(self, age, group, group_activity, current_time, image):
        print "START update"
        print age, group, group_activity, current_time, image

        self.groupText.set("Groep "+str(group))
        self.activity_firstText.set(str(group_activity))

        #import pdb; pdb.set_trace()
        if self.act2img.has_key(group_activity):
            img = self.act2img[group_activity]
            print img
            self.activity_firstImLbl.configure(image=img)
        else: 
            print "No image defined for %s"%group_activity
        print "END update"

def main(config):
    timeformat = [item['timeformat'] for item in config if item.has_key("timeformat")][0] #load timeformat markup
    schedules = [item['schedule'] for item in config if item.has_key("schedule")] #load schedule yaml-objects
    schedules = dict([ (sched["age"], CsvInterface.Schedule(sched["path"], timeformat)) for sched in schedules])
    activities = dict([(item['activity']['name'], item['activity']) for item in config if item.has_key("activity")])

    print activities
    
    def update(*args):
        print args
        
    root = tk.Tk()
    
    # root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),
    #                                    root.winfo_screenheight()))
    app = QrJotariGui(root, activities)
    
    backend = pyQRjotari.JotariQrBackend(schedules, app.update)
    backend.start()
    
    root.mainloop()
    print "Mainloop ended"
    backend.force_stop()
	
if __name__ == "__main__":
	confpath = "configuration.yaml"
	conffile = open(confpath)
	config = yaml.load(conffile)
		
	main(config)
