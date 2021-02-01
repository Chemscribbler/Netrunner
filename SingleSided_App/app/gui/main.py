from tkinter import *
from tkinter import ttk
from ..core import Manager  
from ..gui.new_tour_popup import New_Tournament_Popup as ntp

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

class MainApp(ttk.Frame):

    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.root = parent
        self.root.option_add('*tearOff',False)
        self.root.title(" Side Aware Swiss Software")
        self.manager = Manager.Manager()
        self.Toolbar()
        # self.roundButtons = Round_Buttons(self)
        self.t_name = StringVar(value="Test1")
        # self.pairings_display = self.Pairings(self)
        # self.standings_display = self.Standings(self)

        t_label = ttk.Label(self.root,textvariable=self.t_name).grid(column=1,row=1)
        update_button = ttk.Button(self.root,text="Update",command=self.update_text).grid(column=2,row=1)

    def new_t_window(self):
        ntp(self.root,self.manager,self.t_name)

    def Toolbar(self):
        menu_bar = Menu(self.root)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New",command=lambda: ntp(self.root, self.manager, self.t_name))
        file_menu.add_command(label="Open",command=donothing)
        file_menu.add_command(label='Save',command=donothing)
        file_menu.add_separator()
        file_menu.add_command(label='Quit',command=donothing)
        menu_bar.add_cascade(label="File",menu=file_menu)

        help_menu = Menu(menu_bar)
        help_menu.add_command(label="About...",command=donothing)
        help_menu.add_command(label='Help',command=donothing)
        menu_bar.add_cascade(label='Help',menu=help_menu)

        self.root.config(menu=menu_bar)

    def update_text(self):
        self.t_name.set(self.manager.active_tournament_key)

    def Round_Buttons(self):
        pass

    def Pairings(self):
        pass

    def Standings(self):
        pass

if __name__ == "__main__":
    root = Tk()
    root.option_add('*tearOff',False)
    root.title(" Side Aware Swiss Software")
    MainApp(root)
    root.mainloop()