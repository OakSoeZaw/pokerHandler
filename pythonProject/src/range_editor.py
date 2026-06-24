from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Range Editor")

mainframe = ttk.Frame(root, padding = (3, 3, 12, 12))
mainframe.grid(column= 0, row=0, sticky=(N, W, E ,S))