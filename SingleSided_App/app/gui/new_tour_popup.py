from tkinter import ttk
from tkinter import *


class New_Tournament_Popup(ttk.Frame):
    def __init__(self, root, manager, t_name):
        Frame.__init__(self,root)
        self.root = root
        self.manager = manager
        self.t_name = t_name
        self.window = Toplevel(root)
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.window.title("Make New Tournament")

        mainframe = ttk.Frame(self.window, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        #Score Factor Row
        self.score_factor = IntVar()
        valid_s_f = [1,3,5,10,50]
        score_factor_select = ttk.Combobox(mainframe, textvariable=self.score_factor)
        score_factor_select['values']= valid_s_f
        score_factor_select.state(['readonly'])
        score_factor_select.set(valid_s_f[1])
        score_factor_select.grid(column=2, row=1, sticky=(W, E))

        ttk.Label(mainframe, text="Score Factor").grid(column=1, row=1, sticky=W)
        ttk.Button(mainframe,command=self.score_factor_explainer, text="?").grid(column=3,row=1)
        
        #Tournament Type Selection
        self.t_type = BooleanVar()
        ttk.Label(mainframe,text="Single Sided or Doublesided (DSS not implemented)").grid(column=1,row=2)
        ttk.Checkbutton(mainframe,variable=self.t_type).grid(column=2,row=2,sticky=W)

        #Tournament Name
        self.t_name = StringVar(value="New Tournament")
        ttk.Label(mainframe,text='Tournment Name').grid(column=1,row=3,sticky=W)
        ttk.Entry(mainframe,textvariable=self.t_name,width=25).grid(column=2,row=3,sticky=W)

        #Create Button
        ttk.Button(mainframe,command=self.make_tournament,text='Create').grid(column=2,row=4,stick=S)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        # feet_entry.focus()
        root.bind("<Return>", self.donothing)

    def donothing(self):
        filewin = Toplevel(self.root)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    def make_tournament(self):
        self.manager.create_tournament(self.t_name.get())
        print(self.manager.active_tournament_key)
        self.manager.active_tournament.score_factor = self.score_factor.get()
        self.window.destroy()

    def score_factor_explainer(self):
        exp_win = Toplevel(self.root)
        text = Text(exp_win,wrap="word",width=120)
        text.grid(column=1, row=1)
        text.insert('1.0',
"Score factor affects how many prestige up/down the algorithm will\
look to avoid having someone play an additional game with the side they have played more.\
Another player in the same level will be prefered, though some configurations will have pair\
up/downs to minimize the overall parity\n\
 1: Most aggressive side parity (will search +/- 8 prestige levels)\n\
 3: Default, will search +/- two levels for side parity\n\
 5: Will search +/- one level\n\
10: Will search +/- 6 levels only if it avoids both players having 2 extra games on the same side\n\
50: Will search +/- 1 level only if it avoids both players having 2 extra games on the same side.")
        text['state']='disabled'
        