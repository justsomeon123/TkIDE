import os,sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import os, sys
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
    def __init__(self):
        self.root = tk.Toplevel()
        self.MP3File = tk.StringVar()
        self.Length = tk.IntVar()
        self.root.title("mp3Loader")
        self.root.geometry("500x500")
        ttk.Button(self.root,text="Open mp3 file",command=lambda:self.Load()).pack()
        self.MusicProg = ttk.Progressbar(self.root,mode="determinate",maximum=self.Length.get())
        self.MusicProg.pack()
        self.root.mainloop()

    def Load(self):
        self.MP3File.set(filedialog.askopenfile(defaultextension=".mp3",filetypes=[('mp3 File','*.mp3')]))
        prevdir = os.getcwd()
        with changedir("/"):
            music.music.load((self.MP3File.get()))
            music.music.get_pos()
        changedir(prevdir)
        x = MP3(self.MP3File.get())
        self.Length.set(x.info.length)
        
        del x
        

if __name__ == "__main__":
    app()