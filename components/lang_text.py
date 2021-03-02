from typing import List, Set, Dict, Tuple, Optional, Any, Union

from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk

from knora.dsplib.models.helpers import BaseError
from knora.dsplib.models.langstring import Languages, LangString, LangStringIterator

class LangText(ttk.Frame):
    def __init__(self,
                 parent: Widget,
                 langstr: Optional[LangString] = None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.langstr = langstr
        self.lang_radios: List[ttk.Radiobutton] = []
        i = 1
        self.selected_lang = StringVar()
        for idx, l in enumerate(Languages):
            self.lang_radios.append(ttk.Radiobutton(self,
                                                    text=l.value,
                                                    variable=self.selected_lang,
                                                    value=l.value,
                                                    command=self.lang_changed))
            self.lang_radios[idx].grid(row=0, column=idx)
        self.selected_lang.set("en")
        self.txt_w = tk.Text(self, height=4)
        self.txt_w.grid(row=1, column=0, sticky=(N, W, S, E), columnspan=4, padx=2, pady=2)

        if self.langstr is not None:
            str = self.langstr.get_by_lang(self.selected_lang.get())
            if str is not None:
                self.txt_w.insert("1.0", str)

    def set_langstring(self, langstr: LangString) -> None:
        self.langstr = langstr
        self.txt_w.delete("1.0", END)
        if self.langstr is not None:
            str = self.langstr.get_by_lang(self.selected_lang.get())
            if str is not None:
                self.txt_w.insert("1.0", str)

    def lang_changed(self) -> None:
        self.txt_w.delete("1.0", END)
        if self.langstr is not None:
            str = self.langstr.get_by_lang(self.selected_lang.get())
            if str is not None:
                self.txt_w.insert("1.0", str)





