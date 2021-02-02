import tkinter as tk
# from tkinter import ttk
from ..core import Manager  
from ..gui.new_tour_popup import New_Tournament_Popup as ntp

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)

        self.container = tk.Frame(self)
        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)
        self.frames = {}
        self.manager = Manager.Manager()

        self.Toolbar()

        # for F in (Mainpage, PairingsFrame, StandingsFrame, TNameFrame):
        for F in (TNameFrame, PairingsFrame):
            page_name = F.__name__            
            frame = F(self.container, self)
            self.frames[page_name] = frame
        # self.T_Name = tk.StringVar(value="Test")
        # t_name = tk.Label(self,textvariable= self.T_Name)
        # t_name.grid(column=1,row=1)

    # def __init__(self, parent, **kwargs):
    #     ttk.Frame.__init__(self, parent, **kwargs)
    #     self.root = parent
    #     self.root.option_add('*tearOff',False)
    #     self.root.title(" Side Aware Swiss Software")
    #     self.manager = Manager.Manager()
    #     self.Toolbar()
    #     # self.roundButtons = Round_Buttons(self)
    #     self.t_name = StringVar(value="Test1")
    #     # self.pairings_display = self.Pairings(self)
    #     # self.standings_display = self.Standings(self)

    #     t_label = ttk.Label(self.root,textvariable=self.t_name).grid(column=1,row=1)
        # update_button = ttk.Button(self.root,text="Update",command=self.update_text).grid(column=2,row=1)

    def new_t_window(self):
        ntp(self.container, self)

    def Toolbar(self):
        menu_bar = tk.Menu(self.container)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New",command=lambda: ntp(self.container, self))
        file_menu.add_command(label="Open",command=donothing)
        file_menu.add_command(label='Save',command=donothing)
        file_menu.add_separator()
        file_menu.add_command(label='Quit',command=donothing)
        menu_bar.add_cascade(label="File",menu=file_menu)

        help_menu = tk.Menu(menu_bar)
        help_menu.add_command(label="About...",command=donothing)
        help_menu.add_command(label='Help',command=donothing)
        menu_bar.add_cascade(label='Help',menu=help_menu)

        self.config(menu=menu_bar)

class PairingsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__()
        self.controller = controller
        self.grid(column=1,row=3)
        # self.grid(column=1,row=3)
        p_label=tk.Label(self,text="Pairings Here")
        p_label.grid(column=1,row=3)

class TNameFrame(tk.Frame):
    def __init__(self,parent, controller):
        super().__init__()
        self.controller = controller
        self.grid(column=1,row=1)
        self.T_Name = tk.StringVar(value="Test")
        t_name = tk.Label(self,textvariable= self.T_Name)
        t_name.grid(column=1,row=1)

if __name__ == "__main__":
    # root = tk.Tk()
    # root.option_add('*tearOff',False)
    # root.title(" Side Aware Swiss Software")
    # MainApp()
    # root.mainloop()
    app = MainApp()
    app.mainloop()