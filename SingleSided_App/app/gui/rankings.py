import tkinter as tk
from tkinter import (ttk, N,S, W, CENTER, E, VERTICAL, NO, messagebox)

class RankingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__()
        self.controller = controller
        self['padx'] = 10
        self['pady'] = 10
        self.grid(column=2,row=3, rowspan=3,sticky=(N,S,E,W))
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        
        # f['padding'] = (10,5)

        #Making Treeview Table
        self.player_standings = ttk.Treeview(self,selectmode='browse')
        self.player_standings.grid(column=1,row=1, rowspan = 2, columnspan = 4)

        #Defining Columns
        self.player_standings['columns'] = ("Name", "Score", "SoS", "CID", "RID","SB")

        #Formatting
        self.player_standings.column("#0",width=0,stretch=NO)
        self.player_standings.column("Name",anchor=W)
        self.player_standings.column('Score',anchor=CENTER,width=60)
        self.player_standings.column('SoS',anchor=CENTER,width=60)
        self.player_standings.column('CID',anchor=W)
        self.player_standings.column('RID',anchor=W)
        self.player_standings.column('SB',anchor=CENTER,width=60)

        #Making headers
        self.player_standings.heading("#0",text='')
        self.player_standings.heading("Name",text='Name')
        self.player_standings.heading("Score",text="Score")
        self.player_standings.heading("SoS",text="SoS")
        self.player_standings.heading('CID',text='Corp')
        self.player_standings.heading('RID',text='Runner')
        self.player_standings.heading('SB',text='Side')

        #Scrollbar
        self.scrollbar = tk.Scrollbar(self,orient=VERTICAL,command=self.player_standings.yview)
        self.scrollbar.grid(column=5,row=1,rowspan=2, sticky=(N,S))

        #Buttons for Adding Player
        self.add_player_frame = tk.Frame(self)
        self.add_player_frame.grid(column=1, row=3)
        add_p_button = self.add_p_button = ttk.Button(self.add_player_frame,text="Add Player",command=self.add_player)
        add_p_button.state(['disabled'])
        add_p_button.grid(column=1, row=1)
        self.p_name = tk.StringVar(value="Name")
        name = ttk.Entry(self.add_player_frame,textvariable=self.p_name)
        name.grid(column=2, row=1)

        corp_ids = ["NA",'HB:EtF',"NBN:MN",'W:BABW',"J:PE"]
        runner_ids = ['NA',"Kate",'Noise','Gabe']
        
        self.sel_corp = tk.StringVar()
        self.sel_runner = tk.StringVar()

        self.combo_corp = ttk.Combobox(self.add_player_frame,textvariable=self.sel_corp)
        self.combo_corp['values'] = corp_ids
        self.combo_corp.set(corp_ids[0])

        self.combo_runner = ttk.Combobox(self.add_player_frame,textvariable=self.sel_runner)
        self.combo_runner['values'] = runner_ids
        self.combo_runner.set(runner_ids[0])

        self.combo_corp.state(['readonly'])
        self.combo_runner.state(['readonly'])

        self.combo_corp.grid(column=3, row=1)
        self.combo_runner.grid(column=4, row=1)

        self.drop_button = tk.Button(self.add_player_frame,text='Drop Selected Player',command=self.drop_player)
        self.drop_button.grid(column=5,row=1)

        for child in self.add_player_frame.winfo_children():
            child.grid_configure(padx=10)
    
    
    def add_player(self):
        try:
            plr = self.controller.manager.add_player(self.p_name.get(), corp_id = self.combo_corp.get(), runner_id = self.combo_runner.get())
            self.player_standings.insert('','end',iid=plr.id,values=(plr.name, plr.score, plr.sos, plr.corp_id, plr.runner_id, plr.side_balance))
        except AttributeError as e:
            messagebox.showerror(repr(e),f"Something went wrong. Most likey you have not made a Tournament yet\n{str(e)}")
        except ValueError as e:
            messagebox.showerror(repr(e),str(e))
    
    def update_rankings(self):
        self.player_standings.delete(*self.player_standings.get_children())
        for plr in self.controller.manager._gui_return_rankings():
            self.player_standings.insert('','end',iid=plr.id,values=(plr.name, plr.score, plr.sos, plr.corp_id, plr.runner_id, plr.side_balance))

    def start_tournament(self):
        self.update_rankings()
        self.add_player_frame.destroy()
        self.create_drop_option()

    def create_drop_option(self):
        # print("creating_drop_button")
        self.drop_button = drop_b = tk.Button(self,text='Drop Selected Player',command=self.drop_player)
        drop_b.grid(column = 1, row = 3)
        self.update()

    def drop_player(self):
        row = self.player_standings.selection()
        name = self.player_standings.item(row)['values'][0]
        if tk.messagebox.askyesno("Drop Player?",f"Drop {name}? This is irreversible",icon='warning'):
            print( self.controller.manager.drop_player(name))
