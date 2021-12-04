from tkinter import Tk,Label
from PIL import Image, ImageTk
def Splash():
    splash = Tk()
    splash.image = ImageTk.PhotoImage(Image.open('assets/alticon.png').resize((128,128),Image.NEAREST))
    splash.wm_attributes("-transparentcolor", "white")
    label = Label(splash, image=splash.image, bg='white')
    splash.overrideredirect(True)
    splash.lift()
    splash.wm_attributes("-topmost", True)
    splash.wm_attributes("-disabled", True)
    splash.eval('tk::PlaceWindow . center')
    label.pack()
    splash.after(1000, lambda: splash.destroy())
    splash.mainloop()
if __name__ == '__main__':
    Splash()