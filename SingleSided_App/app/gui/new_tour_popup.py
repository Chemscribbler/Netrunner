from tkinter import ttk
import tkinter as tk
from tkinter import (N, W, E, S, BooleanVar, StringVar, IntVar)
from ..gui.pairings import PairingsFrame
from ..gui.rankings import RankingFrame

class New_Tournament_Popup(ttk.Frame):
    def __init__(self, root, content_manager):
        tk.Frame.__init__(self,root)
        self.root = root
        self.content_manager = content_manager
        self.tour_manager = self.content_manager.manager
        self.window = tk.Toplevel(root)
        self.window.title("Make New Tournament")

        mainframe = ttk.Frame(self.window, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))    
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        #Score Factor Row
        self.score_factor = IntVar()
        valid_s_f = [1,2,3,5,10,50]
        score_factor_select = ttk.Combobox(mainframe, textvariable=self.score_factor)
        score_factor_select['values']= valid_s_f
        score_factor_select.state(['readonly'])
        score_factor_select.set(valid_s_f[1])
        score_factor_select.grid(column=2, row=1, sticky=(W, E))

        ttk.Label(mainframe, text="Score Factor").grid(column=1, row=1, sticky=W)
        ttk.Button(mainframe,command=self.score_factor_explainer, text="?").grid(column=3,row=1)
        
        #Tournament Type Selection
        self.t_type = BooleanVar(value=True)
        ttk.Label(mainframe,text="Single Sided (DSS not implemented)").grid(column=1,row=2)
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
        filewin = tk.Toplevel(self.root)
        button = ttk.Button(filewin, text="Do nothing button")
        button.pack()

    def make_tournament(self):
        cmf = self.content_manager.frames
        self.tour_manager.create_tournament(self.t_name.get())
        print(f"Key: {self.tour_manager.active_tournament_key}, Score Factor: {self.tour_manager.active_tournament.score_factor}")
        self.tour_manager.active_tournament.score_factor = self.score_factor.get()
        cmf["TNameFrame"].T_Name.set(self.t_name.get())
        cmf["TNameFrame"].start_button.state(['!disabled'])
        cmf['RankingFrame'] = RankingFrame(self.root, self.content_manager)
        cmf['PairingsFrame'] = PairingsFrame(self.root, self.content_manager)
        cmf['PairingsFrame'].round_num.set(0)
        cmf['RankingFrame'].add_p_button.state(['!disabled'])
        # cmf['RankingFrame'].player_standings.delete(*cmf['RankingFrame'].player_standings.get_children())
        # cmf['PairingsFrame'].pairings_table.delete(*cmf['PairingsFrame'].pairings_table.get_children())
        self.window.destroy()

    def score_factor_explainer(self):
        exp_win = tk.Toplevel(self.root)
        text = tk.Text(exp_win,wrap="word",width=120)
        text.grid(column=1, row=1)
        text.insert('1.0',
"Score factor affects how many prestige (perfect score groups) up/down the algorithm will\
look to avoid having someone play an additional game with the side they have played more.\
Another player in the same level will be prefered, though some configurations will have pair\
up/downs to minimize the overall parity\n\
Each option has two numbers, the amount of prestige it will search to prevent pairing two players\
who have a side bias (i.e. both players have played 2 corp games and 1 runner game) of one\
and the amount of prestige needed when both players have a side bias of two.\n\
 1: 3, 10\n\
 2: 2, 7\n\
 3: 1, 6\n\
 5: 1, 4\n\
10: 0, 3\n\
50: 0, 1.")
        text['state']='disabled'
        