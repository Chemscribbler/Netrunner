import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile, asksaveasfilename, askopenfilename
from ..core import Manager  
from ..gui.new_tour_popup import New_Tournament_Popup as ntp
from ..gui.pairings import PairingsFrame
from ..gui.rankings import RankingFrame
import json
import csv

def donothing():
    pass

class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        self.title("SASS")
        self.container = tk.Frame(self)
        self.container.grid(column=0,row=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        self.grid_rowconfigure(1,weight=0)
        self.grid_rowconfigure(3,weight=10)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)
        self.frames = {}
        self.manager = Manager.Manager()
        self.option_add('*tearOff',False)

        self.Toolbar()

        for F in (TNameFrame, PairingsFrame, RankingFrame):
            page_name = F.__name__            
            frame = F(self.container, self)
            self.frames[page_name] = frame

    def new_t_window(self):
        ntp(self.container, self)

    def Toolbar(self):
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New",command=lambda: ntp(self.container, self))
        # file_menu.add_command(label="Open",command=donothing)
        file_menu.add_command(label='Export Json',command=self.json_export)
        file_menu.add_command(label='Export CSV',command=self.csv_export)
        file_menu.add_command(label='Save Tournament',command=self.save_tournament)
        file_menu.add_command(label='Export pairings csv',command=self.pairings_csv_export)
        file_menu.add_separator()
        file_menu.add_command(label='Load Tournament',command=self.load_tournament)
        file_menu.add_command(label='Import Players',command=self.import_players)
        file_menu.add_separator()
        file_menu.add_command(label='Quit',command=self.destroy)
        menu_bar.add_cascade(label="File",menu=file_menu)

        help_menu = tk.Menu(menu_bar)
        help_menu.add_command(label="About...",command=donothing)
        help_menu.add_command(label='Help',command=donothing)
        menu_bar.add_cascade(label='Help',menu=help_menu)

        self.config(menu=menu_bar)

    def start_tournament(self):
        self.manager.start_tournament()
        self.frames['PairingsFrame'].start_tournament()
        self.frames['RankingFrame'].start_tournament()

    def json_export(self):
        files = [('JSON JavaScript Object Notation', '*.json')]
        outfile = asksaveasfile(filetypes=files,defaultextension=files)
        with outfile as outfile:
            json.dump(self.manager.export_json(),outfile)

    def csv_export(self):
        files = [('CSV Comma-Seperated Values', '*.csv'),
                 ('TXT Text File','*.txt')]
        outfile = asksaveasfilename(filetypes=files,defaultextension='.csv')
        self.manager.export_standings_csv(file_path=outfile)

    def pairings_csv_export(self):
        files = [('CSV Comma-Seperated Values', '*.csv'),
                 ('TXT Text File','*.txt')]
        default_text = f"{self.manager.active_tournament_key}_round_{self.manager.active_tournament.round}"
        outfile = asksaveasfilename(filetypes=files,defaultextension='.csv',initialfile=default_text)
        self.manager.export_pairings_csv(file_path=outfile)

    def save_tournament(self):
        files= [('Savefile','*.pkl')]
        outfile = asksaveasfilename(filetypes=files,defaultextension='.pkl')
        self.manager.save_tournament(outfile)
    
    def load_tournament(self):
        infile = askopenfilename()
        self.manager.open_tournament(infile)
        self.refresh_screen()

    def refresh_screen(self):
        self.frames['TNameFrame'].T_Name.set(self.manager.active_tournament_key)
        self.frames['RankingFrame'].update_rankings()
        self.frames['PairingsFrame'].update_pairings_display()
        pf = self.frames['PairingsFrame']
        if self.manager.check_round_done():
            for button in pf.result_buttons:
                button['state'] = tk.DISABLED
            pf.pair_round_button['state'] = tk.NORMAL
            pf.close_round_button['state'] = tk.DISABLED
        else:
            for button in pf.result_buttons:
                button["state"] = tk.NORMAL
            pf.pair_round_button['state'] = tk.DISABLED
            pf.close_round_button["state"] = tk.NORMAL

    def import_players(self):
        pass


class TNameFrame(tk.Frame):
    def __init__(self,parent, controller):
        super().__init__()
        self.controller = controller
        self.grid(column=1,row=1)
        self.frame = tk.Frame(self)
        self.frame.grid(column=0,row=0,sticky=(tk.S,tk.E))
        self.frame.grid_rowconfigure(0,weight=1)
        self.frame.grid_columnconfigure(0,weight=1)
        
        self.T_Name = tk.StringVar(value="Create a Tournament")
        t_name = tk.Label(self.frame,textvariable= self.T_Name)
        t_name.grid(column=1,row=1)
        self.start_button = ttk.Button(self.frame,text="Start Tournament", command=self.start_tournament)
        self.start_button.grid(column=2,row=1)
        self.start_button.state(['disabled'])


    def start_tournament(self):
        if not tk.messagebox.askyesno(title='Start Tournament',message='Do you want to start the tournament? You will not be able to add players once you do'):
            return
        self.start_button.state(['disabled'])
        self.controller.start_tournament()

if __name__ == "__main__":
    # root = tk.Tk()
    # root.option_add('*tearOff',False)
    # root.title(" Side Aware Swiss Software")
    # MainApp()
    # root.mainloop()
    app = MainApp()
    app.mainloop()