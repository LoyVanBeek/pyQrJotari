import Tkinter as tk
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

    def __init__(self, master):
        frame = tk.Frame(master)
        frame.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.dateframe = tk.Frame(frame)
        #Build the datecontrol frame
        self.dateframe.grid(row=1)#pack())
        
        self.groupText = tk.StringVar()
        self.groupLabel = tk.Label(frame, textvariable=self.groupText)
        self.groupLabel.grid(row=2)#pack()#tk.TOP
                
        self.goto_firstLabel = tk.Label(frame, text="gaat naar")
        self.goto_firstLabel.grid(row=3)#pack(side=tk.LEFT)
        
        self.currentActivityFrame = tk.Frame(frame)
        
        self.activity_firstText = tk.StringVar()
        self.activity_firstLabel = tk.Label(self.currentActivityFrame, textvariable=self.activity_firstText)
        self.activity_firstLabel.pack(side=tk.LEFT)
        self.activity_firstImage = tk.PhotoImage("/home/loy/Development/pyQrJotari/images/tenten opzetten.GIF")
        self.activity_firstImLbl = tk.Label(self.currentActivityFrame, image=self.activity_firstImage)
        self.activity_firstImLbl.pack(side=tk.RIGHT)
        
        self.currentActivityFrame.grid(row=4,sticky=tk.N+tk.S+tk.E+tk.W)#pack()
        
        self.goto_secondLabel = tk.Label(frame, text="daarna")
        self.goto_secondLabel.grid(row=5)#pack()
        
        self.activity_secondText = tk.StringVar()
        self.activity_secondLabel = tk.Label(frame, textvariable=self.activity_secondText)
        self.activity_secondLabel.grid(row=6)#pack()
        
        self.groupText.set("Groep 1")
        self.activity_firstText.set("Avondspel")
        self.activity_secondText.set("Slapen")
    
    def update(self, age, group, group_activity, current_time, image):
        self.groupText.set(group)
        self.activity_firstText.set(group_activity)

def main(config):
    timeformat = [item['timeformat'] for item in config if item.has_key("timeformat")][0] #load timeformat markup
    schedules = [item['schedule'] for item in config if item.has_key("schedule")] #load schedule yaml-objects
    schedules = dict([ (sched["age"], CsvInterface.Schedule(sched["path"], timeformat)) for sched in schedules])
    
    def update(*args):
        print args
        
    root = tk.Tk()
    app = QrJotariGui(root)
    
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
