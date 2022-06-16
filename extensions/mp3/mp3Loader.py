# Example extension, follow the same format, using a class, __name__ == "__main__", and always make sure gui apps use a 
# command argument and also, pygame and mutagen are included with the compile of the exe, for other extensions, 
# you will need to put them in as folders, MAKE SURE TO CHECK WITH THE CREATORS OF THE EXTERNAL MODULES YOU ARE USING 
#

import os,sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

with open(os.devnull, 'w') as f:
    oldstdout = sys.stdout
    sys.stdout = f
    import pygame.mixer as music
    sys.stdout = oldstdout

from mutagen.mp3 import MP3
from extensions.stdlibrary import changedir
music.init()


def test():
    print("mp3Loader.py initizalized and working")

class app:
    def __init__(self,command=False):
        if command:
            self.root = tk.Tk()
        else:
            self.root = tk.Toplevel()
        
        self.MP3File = tk.StringVar()
        self.Length = tk.IntVar()
        self.root.title("mp3Loader")


        
        ttk.Button(self.root,text="Open mp3 file",command=lambda:self.Load()).pack(side=tk.TOP,padx=5,pady=5)
        
        self.MusicProg = ttk.Progressbar(self.root,mode="determinate",maximum=self.Length.get())
        self.LengthLabel = ttk.Label(self.root,textvariable=self.Length)
        self.NameLabel = ttk.Label(self.root,textvariable=self.MP3File)
        self.NameLabel.pack(side=tk.TOP,padx=5,pady=5)
        self.MusicProg.pack(side=tk.BOTTOM)
        self.LengthLabel.pack(side=tk.BOTTOM)
        self.root.protocol("WM_DELETE_WINDOW",self.WindowClose)
        self.root.after(1,self.GetPos())
        
        self.root.mainloop()

    def Load(self):
        self.MP3File.set(filedialog.askopenfile(defaultextension=".mp3",filetypes=[('mp3 File','*.mp3')]).name)

        prevdir = os.getcwd()
        with changedir("/"):
            music.music.load((self.MP3File.get()))
        music.music.play()

        changedir(prevdir)
        
        x = MP3(self.MP3File.get())
        self.Length.set(int(str(round(x.info.length)) +"000"))
        print(self.Length.get())
        self.MusicProg.config(maximum=self.Length.get())

        
        del x
    
    def GetPos(self):
        if music.music.get_busy():
            print("updating")
            self.MusicProg["value"] = music.music.get_pos()
        else:
            pass

    
    def WindowClose(self):
        self.root.destroy()
        music.quit()    
        

if __name__ == "__main__":
    app()