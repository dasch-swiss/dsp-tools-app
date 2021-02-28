import os

from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk

xpos = 0
ypos = 0
fposx = 10
fposy = 10

def bdown(event):
    global xpos, ypos, fposx, fposy
    xpos = event.x
    ypos = event.y
    frame.bind("<B1-Motion>", bmove)
    print(event)

def bmove(event):
    frame.bind("<ButtonRelease-1>", bup)
    global xpos, ypos, fposx, fposy
    fposx = fposx + event.x - xpos
    fposy = fposy + event.y - ypos
    xpos = event.x
    ypos = event.y
    canvas.move(id, fposx, fposy)
    print(event)

def bup(event):
    frame.bind("<Motion>")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("TESTING...")
    root.geometry("900x800+200+200")

    canvas = Canvas(root, background='gray75')
    canvas.pack(fill=BOTH, expand=True)

    frame = ttk.LabelFrame(canvas, text="move")
    frame.bind('<Button-1>', bdown)

    b1 = ttk.Button(frame, text="gaga 1")
    b1.pack(side=TOP, fill=X, expand=True)

    b2 = ttk.Button(frame, text="gaga 2")
    b2.pack(side=TOP, fill=X, expand=True)

    b3 = ttk.Button(frame, text="gaga 3")
    b3.pack(side=TOP, fill=X, expand=True)


    id = canvas.create_window(fposx, fposy, anchor='nw', window=frame)

    root.mainloop()