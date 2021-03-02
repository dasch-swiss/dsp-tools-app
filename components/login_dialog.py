from typing import List, Set, Dict, Tuple, Optional, Any, Union

from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from tkinter import simpledialog


class LoginDialog(tk.simpledialog.Dialog):

    def __init__(self, parent, title):
        self.iframe = None
        self.server = tk.StringVar()
        self.server.set("http://0.0.0.0:3333")
        self.server_w = None

        self.username = tk.StringVar()
        self.username.set("root@example.com")
        self.username_w = None
        self.password = tk.StringVar()
        self.password.set("test")
        self.password_w = None
        self.success = False

        super().__init__(parent, title)

    def body(self, frame):

        self.iframe = ttk.Frame(frame)

        server_l = ttk.Label(master=self.iframe, text="Server").grid(row=0, column=0)
        ttk.Label(master=self.iframe, text=":").grid(row=0, column=1)
        self.server_w = ttk.Entry(master=self.iframe, textvariable=self.server, style="BW.TEntry")
        self.server_w.grid(row=0, column=2)

        username_l = ttk.Label(master=self.iframe, text="Username/Email").grid(row=1, column=0)
        ttk.Label(master=self.iframe, text=":").grid(row=1, column=1)
        self.username_w = ttk.Entry(master=self.iframe, textvariable=self.username, style="BW.TEntry")
        self.username_w.grid(row=1, column=2)

        password_l = ttk.Label(master=self.iframe, text="Password").grid(row=2, column=0)
        ttk.Label(master=self.iframe, text=":").grid(row=2, column=1)
        self.password_w = ttk.Entry(master=self.iframe, show="*", textvariable=self.password, style="BW.TEntry")
        self.password_w.grid(row=2, column=2)

        self.iframe.pack(side=TOP, fill=BOTH, expand=True)

        return frame

    def buttonbox(self):
        self.ok_button = ttk.Button(self.iframe, text='OK', width=5, command=self.ok_pressed)
        #self.ok_button.pack(side="left", fill=X)
        self.ok_button.grid(row=3, column=0)
        cancel_button = ttk.Button(self.iframe, text='Cancel', width=5, command=self.cancel_pressed)
        #cancel_button.pack(side="right", fill=X)
        cancel_button.grid(row=3, column=2)
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())

    def ok_pressed(self):
        self.server = self.server_w.get()
        self.username = self.username_w.get()
        self.password = self.password_w.get()
        self.success = True
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

