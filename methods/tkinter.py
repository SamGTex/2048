import tkinter as tk
from tkinter import messagebox
import methods.game as game
from tkinter import ttk

class TkGame:
    def __init__(self, master):
        self.__init_variables__()
        self.__init_game__(master)

        self.run_game()

    # init methods
    def __init_variables__(self):
        # graphic
        self.FONTSIZE = 50
        self.TITLE = "2048"
        self.CELL_WIDTH = 4
        self.BG_COLOR = '#17202a'
        self.FG_COLOR = '#d35400'

        # game
        self.board = None
        self.control = None

    def __init_game__(self, master):
        # init game
        self.board = game.create_initial_board()
        self.board = game.generate_2_4(self.board)
        self.board = game.generate_2_4(self.board)

        # init tkwindow
        self.master = master
        self.master.title(self.TITLE)

        self.create_grid(self.board)

    def __init_tk_styles__(self):
        self.style = ttk.Style()
        self.style.configure('My.TEntry', foreground=self.FG_COLOR, background=self.BG_COLOR, fieldbackground=self.BG_COLOR, bordercolor=self.BG_COLOR, borderwidth=1)

    def create_grid(self, initial_board):
        self.entries = []
        for i in range(4):
            row = []
            for j in range(4):              
                entry = ttk.Entry(self.master, font=("Arial", self.FONTSIZE), width=self.CELL_WIDTH, justify='center', style='My.TEntry')
                entry.insert(tk.END, initial_board[i][j])
                entry.state(['readonly'])
                entry.grid(row=i, column=j, padx=5, pady=5, ipadx=10, ipady=10, sticky='nsew')
                row.append(entry)
            self.entries.append(row)

    # ---- game methods ----   
    def run_game(self):
        # show grid
        self.update_grid(self.board)

        # user input
        self.get_input()

        if self.control is None:
            self.master.after(100, self.run_game)
            return
        
        # update grid and show
        self.board = game.update_grid(self.board, self.control)
        self.update_grid(self.board)
        self.master.update()

        # check if game is over
        if game.check_game_over(self.board):
            print('Game Over!')
            messagebox.showinfo("You lost!", f"Score: {self.board.sum()}")
            return
        
        # check if game is won
        if game.check_game_won(self.board):
            print('You won!')
            messagebox.showinfo("You won!", f"Score: {self.board.sum()}")
            return
        
        # generate new 2 or 4 and show
        self.board = game.generate_2_4(self.board)
        self.update_grid(self.board)
        
        # reset control
        self.control = None
        self.master.after(100, self.run_game)


    def update_grid(self, board):
        for i in range(4):
            for j in range(4):
                self.entries[i][j].state(['!readonly'])
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(tk.END, board[i][j])
                self.entries[i][j].state(['readonly'])

     # user input
    def check_input_valid(self, event):
        if event.char in ['w', 'a', 's', 'd']:
            return True
        return False
    
    def get_input(self):
        self.master.focus_set()
        self.master.bind('<Key>', self.key_pressed)

    def key_pressed(self, event):
        if self.check_input_valid(event):
            self.control = event.char
        else:
            self.control = None
