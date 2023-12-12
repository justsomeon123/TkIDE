import tkinter.messagebox as msgbox

from extapi import APIInstance


class Test(APIInstance):

    def window_OnFileOpen(self):
        msgbox.showerror("Info", f"File Opened,  tabs open.")

if __name__ == "__main__": #important for multiprocessing
    x = Test("Test",{"1":["window_OnFileOpen"]})