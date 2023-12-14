from tkinter import ttk

class TFrame(ttk.Frame):
    def __init__(self,id:int,*args, **kwargs):
        super()
        self.id = id
        self.selected:bool = False

class SNotebook(ttk.Frame):
    def __init__(self):
        super()
        self.TabIdDict = {}
        self.Tabs = ttk.Frame(self)
        self.TabContent = ttk.Frame(self)
        self.Tabs.pack(anchor="N",expand=True,side="top")
        self.TabContent.pack(anchor="S",expand=True,side="bottom")
    
    def find_tab_by_id(self,id):
        for tab in self.TabIdDict:
            if tab.id == id:
                return [tab,self.TabIdDict[tab]]
        return None
    
    def add(self,id:int,content):
        temp = TFrame(id)
        self.TabIdDict[temp] = content
        
