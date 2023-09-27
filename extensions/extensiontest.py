import tkinter.messagebox as msgbox

import extapi as api


class Test(api.APIInstance):

    def window_OnFileOpen(self):
        msgbox.showinfo("Info", "File Opened")
    
x = Test("Test",{"001":["window_OnFileOpen"]})