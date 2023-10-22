"""Code for the 2 embedded terminals. Unfinished/In Progress"""

import tkinter as tk
import sys,subprocess

class TerminalWindow:
    def __init__(self,parent):
        self.root = tk.Toplevel()
        self.parent = parent
        self.root.title('Run Output')
        self.text = tk.Text(self.root)
        self.text.pack(expand=True, fill=tk.BOTH)
        self.text.bind("<Button-1>", lambda e: "break")
        self.text.bind("<Key>", lambda e: "break")
        
        # create a scroll bar and attach it to the text widget
        scroll = tk.Scrollbar(self.root)
        scroll.pack(side='right', fill='y')
        scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=scroll.set)
        
        # create an entry widget to take user input
        self.entry = tk.Entry(self.root)
        self.entry.pack(side='bottom', fill='x')
        self.entry.bind('<Return>', self.on_return)
        self.entry.focus()
        
        self.print( ">>> ")
        
    def on_return(self, event):
        # get the user input and process it
        user_input = self.entry.get()
        self.print( user_input + '\n')
        self.entry.delete(0, tk.END)
        self.process_command(user_input)
        self.print( ">>> ")
    
    def print(self,value):
        self.text.insert(tk.END, value)
        
    def process_command(self, command:str):
        
        if command == "forcequit":
            sys.exit(0)
        
        if command.startswith("newtab"):
            try:
                z = command.removeprefix("newtab").strip()
                self.parent.NewTab(z)
                self.print(f"Created tab for file {z}\n")
            except Exception:
                self.print(f"Error, add a filename. Ex:newtab C:/Users/user/test.txt\n")
            return 0
        
        if command == "term":
            TrueTerminalWindow() 
            return 0

        if command.startswith("importcmd"):
            self.print(f"Not supported yet.\n")
            try:
                z = command.removeprefix("importcmd").strip()
            except Exception:
                self.print(f"Error, add a filename. Ex:importcmd C:/Users/user/cmd.json\n")
            return 0
        
        else:
            self.print( f"Error: command \"{command}\" not known \n")




class TrueTerminalWindow():
    def __init__(self):
        self.main = tk.Toplevel()
        self.main.title("Terminal Window (PLEASE NOTE, WON'T WORK WITH EVERYTHING!)")
        self.ttext = tk.Text(self.main)
        self.ttext.bind("<Button-1>", lambda e: "break")
        self.ttext.bind("<Key>", lambda e: "break")
        self.ttext.pack()

        

        self.cmdent = tk.Entry(self.main)
        self.cmdent.pack(anchor="s")
        self.cmdent.bind("<Return>",self.run_cmd)
    
    def run_cmd(self,e):
        cmd = self.cmdent.get()
        self.cmdent.delete("0","end")
        res = subprocess.run(cmd.split(" "),capture_output=True,text=True,shell=True)
        if res.stdout:
            self.ttext.insert("end","\n"+res.stdout)
        elif res.stderr:
            self.ttext.insert("end","\n"+res.stderr)
