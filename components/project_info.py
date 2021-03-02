from typing import List, Set, Dict, Tuple, Optional, Any, Union

from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk

from knora.dsplib.models.project import Project
from knora.dsplib.models.langstring import Languages, LangString, LangStringIterator

from components.lang_text import LangText


class ProjectInfo(ttk.Frame):

    def __init__(self,
                 parent: Widget,
                 project: Optional[Project],
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._project = project

        row = 0
        self._shortcode_label = ttk.Label(self, text="Shortcode:")
        self._shortcode_label.grid(row=row, column=0, sticky=(E))
        self._shortcode_value = tk.StringVar()
        self._shortcode_entry = ttk.Entry(self, textvariable=self._shortcode_value, width=4)
        self._shortcode_entry.grid(row=row, column=1, sticky=(W))
        row += 1

        self._shortname_label = ttk.Label(self, text="Shortname:")
        self._shortname_label.grid(row=row, column=0, sticky=(E))
        self._shortname_value = tk.StringVar()
        self._shortname_entry = ttk.Entry(self, textvariable=self._shortname_value, width=32)
        self._shortname_entry.grid(row=row, column=1, sticky=(W))
        row += 1

        self._longname_label = ttk.Label(self, text="Longname:")
        self._longname_label.grid(row=row, column=0, sticky=(E))
        self._longname_value = tk.StringVar()
        self._longname_entry = ttk.Entry(self, textvariable=self._longname_value)
        self._longname_entry.grid(row=row, column=1, sticky=(E, W))
        row += 1

        gaga = LangString({"en": "gaga-en", "fr": "gaga-fr"})
        self._description_label = ttk.Label(self, text="Description:")
        self._description_label.grid(row=row, column=0, sticky=(E))
        self._description_entry = LangText(self, langstr=gaga)
        self._description_entry.grid(row=row, column=1, sticky=(E, W))
        row += 1

        self._keywords_label = ttk.Label(self, text="Keywords:")
        self._keywords_label.grid(row=row, column=0, sticky=(E, W))
        self._keywords_value = tk.StringVar()
        self._keywords_entry = ttk.Entry(self, textvariable=self._keywords_value)
        self._keywords_entry.grid(row=row, column=1, sticky=(E, W))
        row += 1

        if self._project is not None:
            self._shortcode_value = self._project.shortcode
            self._shortname_value = self._project.shortname
            self._longname_value = self._project.longname
            self._description_entry.set_langstring(self._project.description)

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, project: Project):
        self._project = project
        self._shortcode_value.set(self._project.shortcode)
        self._shortname_value.set(self._project.shortname)
        self._longname_value.set(self._project.longname)
        self._description_entry.set_langstring(project._description)
        self._keywords_value.set(", ".join(project._keywords))



