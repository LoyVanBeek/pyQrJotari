import Tkinter as tk

class App(object):
    def __init__(self, master):
        print "initing GUI"
        frame = tk.Frame(master)
        frame.pack()
        
        self.button = tk.Button(frame, text="Hai", command=self.set_text)
        self.button.pack(side=tk.LEFT)
        
        self.text = tk.StringVar()
        self.label = tk.Label(frame, textvariable=self.text)
        self.label.pack(side=tk.RIGHT)
    
    def set_text(self):
        self.text.set("Hello World")

root = tk.Tk()
app = App(root)
root.mainloop()
