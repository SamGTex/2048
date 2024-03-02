from methods.tkinter import TkGame
import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedTk



DARK = '#17202a'
THEME = 'yaru'

def main():
    # start the GUI
    root = ThemedTk(theme=THEME)
    #root = tk.Tk()
    #root.configure(bg=DARK)

    Gui2024 = TkGame(root)

    root.mainloop()

if __name__ == '__main__':
    main()