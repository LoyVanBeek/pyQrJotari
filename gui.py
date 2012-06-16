import Tkinter as tk
import tkFont
import yaml
import pyQRjotari
import CsvInterface

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

    def __init__(self, master, activity2img_map):
        self.act2img = dict([(act, tk.PhotoImage(file=path, height=200)) for act, path in activity2img_map.iteritems()])

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
    
    def update(self, age, group, group_activity, current_time, image):
        self.groupText.set("Groep "+str(group))
        self.activity_firstText.set(group_activity)
        self.activity_firstImLbl.configure(image=self.act2img['jota'])

def main(config):
    timeformat = [item['timeformat'] for item in config if item.has_key("timeformat")][0] #load timeformat markup
    schedules = [item['schedule'] for item in config if item.has_key("schedule")] #load schedule yaml-objects
    schedules = dict([ (sched["age"], CsvInterface.Schedule(sched["path"], timeformat)) for sched in schedules])
    
    def update(*args):
        print args
        
    root = tk.Tk()
    
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),
                                       root.winfo_screenheight()))
    app = QrJotariGui(root, {"jota":"/home/loy/Development/pyQrJotari/images/jota.gif"})
    
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
