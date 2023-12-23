from tkinter import *

import time
import sys

from fuzzystringmatch import fuzzy_regex_match_window_list
from windows_utils import get_all_windows


class TextAsListBox(Entry):

    def __init__(self, *args, **kwargs):
        self.default_text = 'Enter window title...'
        self.var = kwargs['textvariable'] = StringVar(value=self.default_text)

        Entry.__init__(self, *args, **kwargs)

        self.default_window_list = None

        self.item_height = 18  # Approximate pixel height of one item in the listbox
        self.extra_height = 5
        self.window_width = 700
        self.max_height = 16

        self.current_row_index = None

        self.listboxUp = False
        self.root = args[0]

        self.focus()
        self.selection_range(0, END)

        self.var.trace('w', self.on_entry_change)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)
        self.bind("<Return>", self.switch_to_selected_window)

    def on_entry_change(self, name, index, mode):
        print(f"on_entry_change")

        matches = []

        if self.var.get() == self.default_text:
            if self.listboxUp:
                self.textbox.destroy()
                self.listboxUp = False
        else:
            # Display all open windows when no text is entered
            if self.var.get().strip() == '':
                if self.default_window_list is None:
                    autocompleteList = get_all_windows()
                    autocompleteList = [window for window in autocompleteList if window.title.strip() != '']
                    self.default_window_list = autocompleteList

                print(f"Default window list")
                self.words = self.default_window_list
            else:
                print(f"Filtered window list")
                matches, self.words = self.comparison()

        print(f"# selected links: {len(self.words)}")

        if self.words:

            if not self.listboxUp:
                self.create_textbox()

        self.clear_textbox()

        for i, w in enumerate(self.words):
            self.textbox.insert(END, "*) " + w.title + "\n")

            if len(matches) > 0:
                for match in matches[i]:
                    for w in match:
                        offset = 3
                        row_start = w.start() + offset
                        row_end = w.end() + offset
                        print(f"match: {w}")
                        print(f"row_start: {row_start}")
                        print(f"row_end: {row_end}")

                        self.textbox.tag_add("start", f"{i + 1}.{row_start}", f"{i + 1}.{row_end}")
                        self.textbox.tag_config("start", foreground="red")

        self.textbox.config(state=DISABLED)

    def create_textbox(self):
        textbox_height = min(len(self.words), self.max_height)

        self.scrollbar_x = Scrollbar(self.root)

        self.textbox = Text(width=self["width"], height=textbox_height,
                            xscrollcommand=self.scrollbar_x.set)

        self.textbox.bind("<Return>", self.switch_to_selected_window)
        self.textbox.bind("<Up>", self.moveUp)
        self.textbox.bind("<Down>", self.moveDown)
        self.textbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
        self.textbox.tag_configure("highlight", background="LightSkyBlue1")
        self.listboxUp = True

        self.scrollbar_x.config(command=self.textbox.xview)
        self.scrollbar_x.grid(row=1, column=0)

        root.geometry(f"{self.window_width}x{textbox_height * self.item_height + self.extra_height}")

    def clear_textbox(self):

        if self.current_row_index is not None:
            self.remove_highlight(self.current_row_index)

        self.current_row_index = None

        self.textbox.config(state=NORMAL)

        self.textbox.delete("1.0", END)

    def switch_to_selected_window(self, event):
        print(f"switch to selected window")

        if self.listboxUp:
            selected_index = self.current_row_index - 1

            self.textbox.destroy()
            self.listboxUp = False

            root.geometry(f"{self.window_width}x{self.winfo_height()}")

            window = self.words[selected_index]
            window.restore()
            window.activate()

            self.focus()
            self.var.set('')
            self.selection_range(0, END)

            time.sleep(2)
            sys.exit(0)

        print(f"index: {self.textbox.index(INSERT)}")
        row_index = int(self.textbox.index(INSERT).split('.')[0])
        print(f"row_index: {row_index}")
        self.highlight(row_index)

    def selection(self, event):
        print(f"selection")

        print(f"index: {self.textbox.index(INSERT)}")
        row_index = int(self.textbox.index(INSERT).split('.')[0])
        print(f"row_index: {row_index}")
        self.highlight(row_index)

    def highlight(self, n):
        if self.current_row_index is not None:
            self.remove_highlight(self.current_row_index)

        self.textbox.tag_add("highlight", "{}.0".format(n), "{}.0+1lines".format(n))
        self.current_row_index = n
        self.textbox.mark_set("current", "{}.0".format(n))
        self.textbox.see("current")

    def remove_highlight(self, n):
        self.textbox.tag_remove("highlight", "{}.0".format(n), END)

    def moveUp(self, event):
        if self.current_row_index is None or self.current_row_index == 1:
            next_index = len(self.words)
        else:
            next_index = self.current_row_index - 1

        self.highlight(next_index)

    def moveDown(self, event):
        print(f"moveDown")

        if self.current_row_index is None or self.current_row_index == len(self.words):
            next_index = 1
        else:
            next_index = self.current_row_index + 1

        print(f"next_index: {next_index}")
        self.highlight(next_index)

    def comparison(self):
        query_string = self.var.get()
        print("Query string: " + query_string)

        matched_list = fuzzy_regex_match_window_list(query_string, self.default_window_list)
        matches = [[match[0]] for match in matched_list]
        windows = [match[1] for match in matched_list]
        return matches, windows


if __name__ == '__main__':
    root = Tk()
    root.title('Quickleap')

    root.geometry(f"700x200")

    entry = TextAsListBox(root, width=700)
    entry.grid(row=0, column=0)

    root.mainloop()
