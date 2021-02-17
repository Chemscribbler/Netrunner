import tkinter as tk
from tkinter import (ttk, N,S, W, CENTER, E, VERTICAL, NO, messagebox)
try:
    from app.util.id_importer import get_all_ids
except:
    pass

class RankingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__()
        self.controller = controller
        self['padx'] = 10
        self['pady'] = 10
        self.grid(column=2,row=3,sticky=(N,S,E,W))
        self.grid_columnconfigure(2,weight=1)
        self.grid_rowconfigure(1,weight=1)

        
        # f['padding'] = (10,5)

        #Making Treeview Table
        tree = self.player_standings = ttk.Treeview(self,selectmode='browse')
        tree.grid(column=1,row=1, rowspan = 2, columnspan = 4,sticky=(N,S,W,E))

        #Defining Columns
        tree['columns'] = ("Name", "Score", "SoS",'ESoS', "CID", "RID","SB")

        #Formatting
        tree.column("#0",width=0,stretch=NO)
        tree.column("Name",anchor=W)
        tree.column('Score',anchor=CENTER,width=60)
        tree.column('SoS',anchor=CENTER,width=60)
        tree.column('ESoS',anchor=CENTER,width=60)
        tree.column('CID',anchor=W)
        tree.column('RID',anchor=W)
        tree.column('SB',anchor=CENTER,width=60)

        #Making headers
        tree.heading("#0",text='')
        tree.heading("Name",text='Name')
        tree.heading("Score",text="Score")
        tree.heading("SoS",text="SoS")
        tree.heading("ESoS",text="Ext. SoS")
        tree.heading('CID',text='Corp')
        tree.heading('RID',text='Runner')
        tree.heading('SB',text='Side')

        #Scrollbar
        self.scrollbar = tk.Scrollbar(self,orient=VERTICAL,command=tree.yview)
        self.scrollbar.grid(column=5,row=1,rowspan=2, sticky=(N,S))

        #Buttons for Adding Player
        self.add_player_frame = tk.Frame(self)
        self.add_player_frame.grid(column=1, row=3,sticky=(S))
        add_p_button = self.add_p_button = ttk.Button(self.add_player_frame,text="Add Player",command=self.add_player)
        add_p_button.state(['disabled'])
        add_p_button.grid(column=1, row=1)
        self.p_name = tk.StringVar(value="Name")
        self.name = ttk.Entry(self.add_player_frame,textvariable=self.p_name)
        self.name.grid(column=2, row=1)


        try:
            ids = get_all_ids()
            corp_ids = ids[0]
            runner_ids = ids[1]
        except:
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
            child.grid_configure(padx=10, sticky=(S,E))
    
    
    def add_player(self):
        try:
            plr = self.controller.manager.add_player(self.p_name.get(), corp_id = self.combo_corp.get(), runner_id = self.combo_runner.get())
            self.player_standings.insert('','end',iid=plr.id,values=(plr.name, plr.score, plr.sos, plr.ext_sos, plr.corp_id, plr.runner_id, plr.side_balance))
        except AttributeError as e:
            messagebox.showerror(repr(e),f"Something went wrong. Most likey you have not made a Tournament yet\n Error: {str(e)}")
        except ValueError as e:
            messagebox.showerror(repr(e),str(e))
        self.name.delete(0,'end')
        self.name.focus()
        self.player_standings.yview_moveto(1)
        
    def update_rankings(self):
        self.player_standings.delete(*self.player_standings.get_children())
        for plr in self.controller.manager._gui_return_rankings():
            self.player_standings.insert('','end',iid=plr.id,values=(plr.name, plr.score, round(plr.sos,3), round(plr.ext_sos,4), plr.corp_id, plr.runner_id, plr.side_balance))

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
            if(self.controller.manager.active_tournament.round == 0):
                self.update_rankings()

