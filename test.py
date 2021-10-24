import tkinter as tk
import tkinter.ttk as ttk


class Example(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.frame = tk.Frame(self.canvas)

        self.vsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.vsb.grid(row=1, column=0, sticky="nsew")

        self.canvas.configure(xscrollcommand=self.vsb.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.create_window((3,2), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.frame_configure)
        self.populate()

    def populate(self):
        tabs = ttk.Notebook(self.frame, width=100, height=100)
        for tab in range(10):
            tabs.add(ttk.Frame(tabs), text=" Tab {}  ".format(tab+1))
        tabs.grid(row=0, column=0, sticky="ew")


    def frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    app = Example()
    app.mainloop()