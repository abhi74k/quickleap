"""
"""

import sys
from tkinter import *
from tkinter.ttk import *
import time

from fuzzystringmatch import fuzzy_regex_match_window_list
from windows_utils import get_all_windows


class EntryWithListBox(Entry):
    def __init__(self, autocompleteList, *args, **kwargs):

        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        # Custom matches function
        Entry.__init__(self, *args, **kwargs)
        self.focus()

        self.default_window_list = autocompleteList
        self.window_title_list = [window.title for window in self.default_window_list]

        self.default_text = 'Enter window title...'

        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar(value=self.default_text)

        self.selection_range(0, END)

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)

        self.root = args[0]
        self.item_height = 18  # Approximate pixel height of one item in the listbox
        self.extra_height = 5
        self.window_width = 500
        self.max_height = 16

        self.listboxUp = False

    def changed(self, name, index, mode):
        if self.var.get() == self.default_text:
            if self.listboxUp:
                self.listbox.destroy()
                self.listboxUp = False
        else:
            if self.var.get().strip() == '':
                print(f"Default window list")
                self.words = self.default_window_list
            else:
                print(f"Filtered window list")
                self.words = self.comparison()

            if self.words:
                if not self.listboxUp:
                    listbox_height = min(len(self.words), self.max_height)

                    self.scrollbar_x = Scrollbar(self.root)

                    self.listbox = Listbox(width=self["width"], height=listbox_height,
                                           xscrollcommand=self.scrollbar_x.set)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.bind("<Return>", self.selection)
                    self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True

                    self.scrollbar_x.config(command=self.listbox.xview)
                    self.scrollbar_x.grid(row=1, column=0)

                    root.geometry(f"{self.window_width}x{listbox_height * self.item_height + self.extra_height}")

                self.listbox.delete(0, END)
                for i, w in enumerate(self.words):
                    self.listbox.insert(END, w.title)
            else:
                if self.listboxUp:
                    self.listbox.destroy()
                    self.scrollbar_x.destroy()
                    self.listboxUp = False

    def selection(self, event):
        if self.listboxUp:
            window_title = self.listbox.get(ACTIVE)
            selected_index = self.listbox.curselection()[0]

            self.listbox.destroy()
            self.listboxUp = False
            # self.icursor(END)

            root.geometry(f"{self.window_width}x{self.winfo_height()}")

            window = self.words[selected_index]
            window.restore()
            window.activate()

            self.focus()
            self.var.set('')
            self.selection_range(0, END)

            time.sleep(2)
            sys.exit(0)

    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != '0':
                self.listbox.selection_clear(first=index)
                index = str(int(index) - 1)

                self.listbox.see(index)  # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '-1'
            else:
                index = self.listbox.curselection()[0]

            if index != END:
                self.listbox.selection_clear(first=index)
                index = str((int(index) + 1) % self.listbox.size())
                self.listbox.see(index)  # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def comparison(self):
        query_string = self.var.get()
        matched_list = fuzzy_regex_match_window_list(query_string, self.default_window_list)
        ret = [match[1] for match in matched_list]
        return ret


if __name__ == '__main__':
    autocompleteList = get_all_windows()
    autocompleteList = [window for window in autocompleteList if window.title.strip() != '']

    root = Tk()
    root.title('Quickleap')

    entry = EntryWithListBox(autocompleteList, root, listboxLength=6, width=100)
    entry.grid(row=0, column=0)

    root.mainloop()
