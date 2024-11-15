import tkinter as tk
from tkinter import messagebox
import methods.game as game
from tkinter import ttk

class TkGame:
    def __init__(self, master):
        # init variables
        self.__init_variables__()
        self.__init_tk_styles__()

        # init game
        self.__init_game__()

        # init window
        self.master = master
        self.master.title(self.TITLE)
        self.__init_window__(self.board)

        # start game
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
        self.score = 0

    def __init_game__(self):
        # init game
        self.board = game.create_initial_board()
        self.board = game.generate_2_4(self.board)
        self.board = game.generate_2_4(self.board)


    def __init_tk_styles__(self):
        self.style = ttk.Style()
        self.style.configure('My.TEntry', foreground='black', background=self.BG_COLOR, fieldbackground=self.BG_COLOR, bordercolor=self.BG_COLOR, borderwidth=1, relief='flat', font=('Tahoma', self.FONTSIZE))
        self.style.configure('TButton', font = ('Tahoma', 20,'bold'), foreground = self.FG_COLOR, background = self.BG_COLOR, bordercolor=self.BG_COLOR)
        self.style.configure('My.TLabel', foreground=self.FG_COLOR, background=self.BG_COLOR, font=('Arial', 20, 'bold'))         
            
    def __init_window__(self, initial_board):
        # score
        self.score_label = ttk.Label(self.master, text=f" Score: {self.score}", font=("Arial", 20), style='My.TLabel')
        self.score_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, ipadx=10, ipady=10, sticky='nsew')

        # highscore
        self.highscore_label = ttk.Label(self.master, text=f" Highscore: {self.get_highscore()}", font=("Arial", 20), style='My.TLabel')
        self.highscore_label.grid(row=0, column=2, columnspan=2, padx=5, pady=5, ipadx=10, ipady=10, sticky='nsew')

        # grid 
        self.entries = []
        for i in range(4):
            row = []
            for j in range(4):              
                entry = ttk.Entry(self.master, font=("Arial", self.FONTSIZE), width=self.CELL_WIDTH, justify='center', style='My.TEntry')
                entry.insert(tk.END, initial_board[i][j])
                entry.state(['readonly'])
                entry.grid(row=i+1, column=j, padx=5, pady=5, ipadx=10, ipady=10, sticky='nsew')
                row.append(entry)
            self.entries.append(row)
        
        # new game button
        new_game_button = ttk.Button(self.master, text="New Game", command=self.new_game, style='My.TButton')
        new_game_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, ipadx=10, ipady=10, sticky='nsew')

        # quit button
        quit_button = ttk.Button(self.master, text="Quit", command=self.master.quit, style='My.TButton')
        quit_button.grid(row=5, column=2, columnspan=2, padx=5, pady=5, ipadx=10, ipady=10, sticky='nsew')


    def new_game(self):
        self.board = game.create_initial_board()
        self.board = game.generate_2_4(self.board)
        self.board = game.generate_2_4(self.board)
        self.update_grid(self.board)
        self.run_game()

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
        _grid = game.update_grid(self.board, self.control)
        if _grid is not None:
            self.board = _grid
        else:
            self.master.after(100, self.run_game) #invalid move
            return
 
        self.update_grid(self.board)
        self.master.update()

        # update score
        self.update_score()

        
        # generate new 2 or 4 and show
        self.board = game.generate_2_4(self.board)
        self.update_grid(self.board)
        
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
        
        # reset control
        self.control = None
        self.master.after(100, self.run_game)

        # update highscore
        self.set_highscore(self.score)


    def update_grid(self, board):
        for i in range(4):
            for j in range(4):
                self.entries[i][j].state(['!readonly'])
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(tk.END, board[i][j])
                self.entries[i][j].state(['readonly'])
    
    def update_score(self):
        self.score = self.board.sum()
        self.score_label.config(text=f"Score: {self.score}")

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

    def get_highscore(self):
        try:
            with open('config.txt', 'r') as file:
                return int(file.read())
        except:
            return 0
        
    def set_highscore(self, score):
        # check if highscore
        highscore = self.get_highscore()
        if score > highscore:
            with open('config.txt', 'w') as file:
                file.write(str(score))
            self.highscore_label.config(text=f"Highscore: {score}")


    def __del__(self):
        self.set_highscore(self.score)
        self.master.quit()
        self.master.destroy()
        print('Game closed')

