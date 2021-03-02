from typing import List, Set, Dict, Tuple, Optional, Any, Union

from pprint import pprint

from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk

from knora.dsplib.models.langstring import Languages, LangString, LangStringIterator
from knora.dsplib.models.listnode import ListNode

from components.lang_text import LangText

class ListsInfo(ttk.Frame):
    def __init__(self,
                 parent: Widget,
                 lists: Optional[List[ListNode]] = None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._lists = lists

        self._lists = ttk.Treeview(self)
        self._lists.grid(row=0, column=0, sticky=(N, W, S, E))
        self.add_lists(lists)

    def _add_sublists(self, id: str, children: Optional[List[ListNode]]):
        if children is None:
            return None
        for node in children:
            id = self._lists.insert(id, 'end', text=node.name)
            if node.children is not None:
                self._add_sublists(id, node.children)

    def add_lists(self, lists: List[ListNode]) -> None:
        if lists is not None:
            for list in lists:
                id = self._lists.insert('', 'end', text=list.name)
                self._add_sublists(id, list.children)
