import tkinter as tk
from tkinter import (ttk, VERTICAL,N,S)
class PairingsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__()
        self.controller = controller
        self.grid(column=1,row=3)
        self['padx'] = 10
        self['pady'] = 10
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        # self.grid(column=1,row=3)
        
        #Buttons for round management
        self.top_buttons_frame = tk.Frame(self)
        self.top_buttons_frame.grid(column=1,row=1)

        self.pair_round_button = ttk.Button(self.top_buttons_frame, text="Pair Round",command=self.pair_round)
        self.pair_round_button.state(['disabled'])
        self.pair_round_button.grid(column=1,row=1)

        self.close_round_button = ttk.Button(self.top_buttons_frame, text="Close Round",command=self.close_round)
        self.close_round_button.state(['disabled'])
        self.close_round_button.grid(column=2,row=1)

        self.round_num = tk.StringVar()
        self.round_label = tk.Label(self.top_buttons_frame,textvariable=self.round_num)
        self.round_label.grid(column=3,row=1,padx=10)
        tk.Label(self.top_buttons_frame, text='Current Round').grid(column=4, row=1, padx=5)
        

        #Treeview for Displaying Pairings
        pairing_columns = ['Table','Corp Player','C Points','Runner Player','R Points','C_plr_obj','R_plr_obj']
        tree = self.pairings_table = ttk.Treeview(self,selectmode='browse')
        tree['columns'] = pairing_columns
        tree['displaycolumns']=pairing_columns[:5]
        
        for item in pairing_columns:
            tree.column(item,anchor=tk.W)
            tree.heading(item,text=item)
        tree.column('#0',width=0,stretch=tk.NO)
        tree.column('Table',width=60)
        tree.column('C Points',width=60)
        tree.column('R Points',width=60)
        
        self.pairings_table.grid(column=1,row=2)

        self.scrollbar = tk.Scrollbar(self,orient=VERTICAL,command=tree.yview)
        self.scrollbar.grid(column=5,row=1,rowspan=2, sticky=(N,S))

        #Buttons for score entry
        result_frame = self.result_entry_frame = tk.Frame(self)
        result_frame.grid(column=1,row=3)
        self.c_win_button = ttk.Button(result_frame, text='Corp Win',command=self.select_corp_win)
        self.r_win_button = ttk.Button(result_frame, text='Runner Win', command=self.select_runner_win)
        self.tie_button = ttk.Button(result_frame, text='Tie',command=self.select_tie)
        self.result_buttons = [self.c_win_button, self.r_win_button, self.tie_button]
        counter = 0
        for button in self.result_buttons:
            button.state(['disabled'])
            button.grid(column = counter, row =1)
            counter +=1 


    def update_pairings_display(self):
        m = self.controller.manager
        t = m.active_tournament
        self.pairings_table.delete(*self.pairings_table.get_children())
        for item in m._gui_return_pairings():
            self.pairings_table.insert('','end',values=(item[0], t.player_dict[item[1]].name,'', t.player_dict[item[2]].name,'',t.player_dict[item[1]].id,t.player_dict[item[2]].id))
        self.round_num.set(t.round)

    def start_tournament(self):
        for button in self.result_buttons:
            button.state(['!disabled'])
        self.close_round_button.state(['!disabled'])
        self.update_pairings_display()

    def pair_round(self):
        m = self.controller.manager
        for button in self.result_buttons:
            button.state(['!disabled'])
        self.close_round_button.state(['!disabled'])
        self.pair_round_button.state(['disabled'])
        m.pair_round(False)
        self.update_pairings_display()
    
    def close_round(self):
        m = self.controller.manager
        if not m.check_round_done():
            tk.messagebox.showerror('Round not Closed','Not all players have recorded results')
            return
        if tk.messagebox.askyesno("Close Round", "Do you want to close the round? this is irreverisble"):
            for button in self.result_buttons:
                button.state(['disabled'])
            self.pair_round_button.state(['!disabled'])
            self.close_round_button.state(['disabled'])
            m.finish_round(pair_next=False,display_rankings=False)
            self.controller.frames['RankingFrame'].update_rankings()
        

    def select_corp_win(self):
        m = self.controller.manager
        players = self.get_players()
        if self.is_ammend():
            m.ammend_result(players[0], players[1], 3, 0)
        else:
            m.record_result(players[0], players[1], 3, 0)
        self.update_row(3,0)

    def select_runner_win(self):
        m = self.controller.manager
        players = self.get_players()
        if self.is_ammend():
            m.ammend_result(players[0], players[1], 0, 3)
        else:
            m.record_result(players[0], players[1], 0, 3)
        self.update_row(0,3)

    def select_tie(self):
        m = self.controller.manager
        players = self.get_players()
        if self.is_ammend():
            m.ammend_result(players[0], players[1], 1, 1)
        else:
            m.record_result(players[0], players[1], 1, 1)
        self.update_row(1,1)

    def get_players(self):
        row = self.pairings_table.selection()
        corp_plr = self.pairings_table.item(row)['values'][5]
        run_plr = self.pairings_table.item(row)['values'][6]
        return (corp_plr, run_plr)

    def is_ammend(self):
        row = self.pairings_table.selection()
        c_score = self.pairings_table.item(row)['values'][2]
        r_score = self.pairings_table.item(row)['values'][4]
        try:
            return (c_score + r_score) > 0
        except:
            return False

    def update_row(self,c_score, r_score):
        row  = self.pairings_table.selection()
        pre_val = self.pairings_table.item(row)['values']
        self.pairings_table.item(row,values=(pre_val[0],pre_val[1],c_score,pre_val[3],r_score,pre_val[5],pre_val[6]))