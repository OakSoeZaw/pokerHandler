#!python3
'''
This file help you create the ranges 
and get the dict
'''

from tkinter import *
from tkinter import ttk
from functools import partial

rank = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
legend_items = [
    ("Raise for Value", "red"),
    ("Raise as Bluff", "#ab9b07"),
    ("Call", "green"),
    ("Fold", "#534682"),
]

root = Tk()
root.title("Range Editor")
root.update_idletasks()
width = 800
height = 600
x = (root.winfo_screenwidth() // 2) - (width //2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")


mainframe = Frame(root, padx =2, pady = 3)
mainframe.grid(column= 0, row=0, sticky=(N, W, E ,S))

legend_frame = Frame(root, padx=5, pady = 5 )
legend_frame.grid(row=1, column=0, sticky=(W, E))

"""
This is for making sure the button are evenly distributed
"""
for i in range(14):  # 14 = 1 label column + 13 rank columns
    mainframe.columnconfigure(i, weight=1)
    mainframe.rowconfigure(i, weight=1)


states= {}
buttons ={}

def on_click(hand, event):
    """
    This changes the range manually
    """
    if states[hand] == "fold":
        states[hand] = "call"
        buttons[hand].config(bg="green")
    elif states[hand] == "call":
        states[hand] = "raise_value"
        buttons[hand].config(bg="red")
    elif states[hand] == "raise_value":
        states[hand] = "raise_bluff"
        buttons[hand].config(bg="#ab9b07")
    else:
        states[hand] = "fold"
        buttons[hand].config(bg="#534682")

for i, r in enumerate(rank):
    ttk.Label(mainframe, text=r).grid(row=0, column=i+1)
    ttk.Label(mainframe, text=r).grid(row=i+1, column = 0)

for i in range(13):
    for j in range(13):
        if i == j:
            hand = rank[i] + rank[j]
        elif i < j:
            hand = rank[i] + rank[j] +'s'
        else:
            hand = rank[j] + rank[i] + 'o'
        
        states[hand] = "fold"

        btn = btn = Label(mainframe, text=hand, bg="#534682", width=3, height=1, relief="raised")
        btn.grid(row = i+1, column=j+1, sticky=(N, W, E, S))
        btn.bind("<Button-1>", partial(on_click, hand))
        buttons[hand] = btn

for i, (label, color) in enumerate(legend_items):
    Label(legend_frame, bg = color, width = 3, relief="raised").grid(row=0, column=i*2, padx= 2)
    Label(legend_frame, text=label).grid(row=0, column=i*2+1, padx=(0,10))

name_frame = Frame(root, padx=5, pady= 5)
name_frame.grid(row=2, column=0, sticky= (W, E))

Label(name_frame, text="Range Name:").grid(row=0, column=0, padx=5)
name_entry= Entry(name_frame, width= 20)
name_entry.grid(row=0, column=1, padx=5)

def export_range():
    range_name = name_entry.get().strip()
    if not range_name:
        print("Please enter a range name")
        return
    
    result= {}
    for hand, state in states.items():
        if state != "fold":
            result[hand] = state

    with open(f"ranges/{range_name}.py", "w") as f:
        f.write(f"{range_name}= {{\n")
        for hand, state in result.items():
            f.write(f'  "{hand}": "{state}",\n')
        f.write("}\n")

    print(f"Exported to /ranges/{range_name}.py")

Button(root, text="Export", command=export_range).grid(row=3, column = 0, pady=5)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight = 1)
root.mainloop()