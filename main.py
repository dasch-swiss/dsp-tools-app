from typing import List, Set, Dict, Tuple, Optional, Any, Union

import os
import json

from pprint import pprint

from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter import filedialog


from knora.dsplib.models.connection import Connection
from knora.dsplib.models.helpers import BaseError
from knora.dsplib.models.user import User
from knora.dsplib.models.project import Project
from knora.dsplib.models.listnode import ListNode

from knora.dsplib.models.langstring import Languages, LangString, LangStringIterator

from knora.dsplib.utils.onto_validate import validate_ontology, validate_ontology_from_string
from knora.dsplib.utils.onto_create_ontology import create_ontology, create_ontology_from_string
from knora.dsplib.utils.onto_commons import list_creator, validate_list_from_excel, json_list_from_excel

from components.login_dialog import LoginDialog
from components.project_info import ProjectInfo
from components.lists_info import ListsInfo


class TaskBar(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(relief=GROOVE, borderwidth=2)


class TextScrollCombo(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ensure a consistent GUI size
        #self.grid_propagate(False)
        # implement stretchability
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create a Text widget
        self.txt = tk.Text(self)
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # create a Scrollbar and associate it with txt
        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set

    def insert(self, *args, **kwargs):
        self.txt.insert(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.txt.get(*args, **kwargs)


class Onto(ttk.Frame):
    def __init__(self, parent,
                 the_app: 'App',
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.ontoobj = None
        self.the_app = the_app
        self.pack(side=TOP, fill=X)

        hframe1_w = ttk.Frame(self)
        label_w = ttk.Label(hframe1_w, text="Data model (JSON) file:")
        label_w.pack(side=LEFT, anchor=CENTER)
        self.filepath = tk.StringVar()
        self.file_field_w = ttk.Entry(hframe1_w, textvariable=self.filepath, style="BW.TEntry")
        self.file_field_w.pack(side=LEFT, anchor="center", fill=X, expand=True)
        open_button_w = ttk.Button(hframe1_w, text="...", command=self.open_json)
        open_button_w.pack(side=RIGHT, anchor="center")
        hframe1_w.pack(side=TOP, fill=X, expand=True)

        hframe2_w = ttk.Frame(self)
        self.validate_button_w = ttk.Button(hframe2_w, text="Validate", state=DISABLED, command=self.validate_json)
        self.validate_button_w.pack(side=LEFT, anchor=CENTER)
        hframe2_w.pack(side=TOP, fill=X, expand=True)

        self.upload_button_w = ttk.Button(hframe2_w, text="Upload", state=DISABLED, command=self.upload_json)
        self.upload_button_w.pack(side=LEFT, anchor=CENTER)

        sep = ttk.Separator(self, orient=HORIZONTAL).pack(side=TOP, fill=X, expand=True, pady=5)

        tabControl = ttk.Notebook(self)
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text='DataModel')

        self.jsonview = TextScrollCombo(tab1)
        self.jsonview.pack(side=TOP, anchor=S, fill=BOTH, expand=True)

        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text='Project')
        self.project_info = ProjectInfo(tab2, None)
        self.project_info.pack(side=TOP, anchor=N, fill=BOTH, expand=True)

        tab3 = ttk.Frame(tabControl)
        tabControl.add(tab3, text='Lists')
        self.lists = ListsInfo(tab3)
        self.lists.pack(side=TOP, anchor=N, fill=BOTH, expand=True)

        tabControl.pack(side=TOP, fill=BOTH, expand=TRUE, padx=2, pady=2)

    def open_json(self):
        json_file_path = filedialog.askopenfile(mode="r", filetypes=(("JSON files", "*.json"), ("Any file", "*")))
        self.filepath.set(json_file_path.name)
        with json_file_path as reader:
            self.jsonstr = reader.read()
            #self.jsonview.delete("1.0", END)
            self.jsonview.insert(END, self.jsonstr)
        self.validate_button_w.configure(state=NORMAL)
        self.upload_button_w.configure(state=NORMAL)

        datapath = os.path.dirname(json_file_path.name)
        datamodel = json.loads(self.jsonstr)

        project = Project(
            con=Connection("https://www.gaga.com"),
            shortcode=datamodel["project"]["shortcode"],
            shortname=datamodel["project"]["shortname"],
            longname=datamodel["project"]["longname"],
            description=LangString(datamodel["project"].get("descriptions")),
            keywords=set(datamodel["project"].get("keywords")),
            selfjoin=False,
            status=True
        )
        self.project_info.project = project

        listobj = datamodel["project"].get('lists')
        newlists: [] = []
        for rootnode in listobj:
            if rootnode.get("nodes") is not None and isinstance(rootnode["nodes"], dict) and rootnode["nodes"].get("file") is not None:
                newroot = {
                    "name": rootnode.get("name"),
                    "labels": rootnode.get("labels"),
               }
                if rootnode.get("comments") is not None:
                    newroot["comments"] = rootnode["comments"]

                startrow = 1 if rootnode["nodes"].get("startrow") is None else rootnode["nodes"]["startrow"]
                startcol = 1 if rootnode["nodes"].get("startcol") is None else rootnode["nodes"]["startcol"]
                #
                # determine where to find the excel file...
                #
                excelpath = rootnode["nodes"]["file"]
                if excelpath[0] != '/' and datapath is not None:
                    excelpath = os.path.join(datapath, excelpath)

                json_list_from_excel(rootnode=newroot,
                                     filepath=excelpath,
                                     sheetname=rootnode["nodes"]["worksheet"],
                                     startrow=startrow,
                                     startcol=startcol)
                newlists.append(newroot)
            else:
                newlists.append(rootnode)
        listobj = None
        gagas: List[ListNode] = []
        for list in newlists:
            listtree = ListNode.readDefinitionFileObj(con=Connection("https://www.gaga.com"),
                                                      project=project,
                                                      rootnode=list)
            listtree.print()
            gagas.append(listtree)
        pprint(gagas)
        self.lists.add_lists(gagas)

    def validate_json(self):
        exeldir = os.path.dirname(os.path.realpath(self.filepath.get()))
        validate_ontology_from_string(self.jsonview.get("1.0", END), exeldir)

    def upload_json(self):
        if self.the_app.server is None:
            self.the_app.connect()
        exeldir = os.path.dirname(os.path.realpath(self.filepath.get()))
        create_ontology_from_string(con=self.the_app.con,
                                    jsonstr=self.jsonview.get("1.0", END),
                                    exceldir=exeldir,
                                    lists_file=None,
                                    verbose=True,
                                    dump=False)

    def get_json(self):
        pass


class App(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.pack(side=TOP, fill=BOTH, expand=True)

        self.con = None
        self.token = None
        self.server = None
        self.user = None

        self.parent = parent
        self.create_menubar()

        taskbar = TaskBar(self, style="TB.TFrame", padding=10)
        self.connect_w = ttk.Button(taskbar, text="Connect...", command=self.connect)
        self.connect_w.pack(side=LEFT)

        self.user_info_w = ttk.Label(taskbar, text="User: -")
        self.user_info_w.pack(side=RIGHT)
        self.server_info_w = ttk.Label(taskbar, text="Server: -")
        self.server_info_w.pack(side=RIGHT)

        tabControl = ttk.Notebook(self)
        tab1 = ttk.Frame(tabControl)
        #tab1.configure(style="YY.TFrame")
        tabControl.add(tab1, text='DSP-tools')
        self.onto = Onto(tab1, the_app=self)


        #gaga = ttk.Frame(self, style="YY.TFrame")
        taskbar.pack(side=TOP, fill=X, anchor=N, expand=False)
        tabControl.pack(side=TOP, fill=BOTH, expand=TRUE, padx=2, pady=2)
        #taskbar.grid(column=0, row=0, sticky=NSEW)
        #tabControl.pack(side=TOP, expand=True, fill=BOTH)

    def create_menubar(self):
        menubar = Menu(self.parent)
        self.parent.configure(menu=menubar)
        menu_connect = Menu(menubar)
        menu_edit = Menu(menubar)
        menubar.add_cascade(menu=menu_connect, label='Connect')
        menubar.add_cascade(menu=menu_edit, label='Edit')

        menu_connect.add_command(label='Connect...', command=self.connect)
        menu_connect.add_command(label='Disconnect', command=self.disconnect)

    def connect(self):
        if self.con is None:
            dialog = LoginDialog(parent=self.parent, title="Login to server")
            if dialog.success:
                self.con = Connection(dialog.server)
                try:
                    self.con.login(dialog.username, dialog.password)
                    self.token = self.con.get_token()
                    self.server = dialog.server
                    self.connect_w.configure(text="Disconnect...")
                    self.server_info_w.configure(text=f"Server: {self.server}")
                    self.user = User(con=self.con, email=dialog.username).read()
                    self.user_info_w.configure(text=f"User: {self.user.username}")
                    self.user.print()
                except BaseError as err:
                    tk.messagebox.showerror("Login failed", err.message)
        else:
            self.con.logout()
            self.con = None
            self.connect_w.configure(text="Connect...")
            self.server_info_w.configure(text="Server: -")
            self.user_info_w.configure(text="User: -")


    def disconnect(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("DSP-tools-app")
    root.geometry("700x500+200+200")
    root.option_add('*tearOff', FALSE)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TB.TFrame")
    style.configure("XX.TFrame")
    style.configure("YY.TFrame")
    #style.configure("BW.TEntry", foreground="black", background="white")
    #style.configure("TB.TFrame", background="light blue")


    app = App(root)
    #app.pack(fill=BOTH, expand=True)
    app.pack_propagate(True)
    root.mainloop()

