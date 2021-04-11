"""CSC111 Winter 2021 Final Project

Overview and Description
========================

This Python module contains the functions for the user interface and
visualization.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Fatimeh Hassan, Shilin Zhang,
Dorsa Molaverdikhani, and Nimit Bhanshali.
"""
from __future__ import annotations
from typing import Any
import tkinter as tk


def runner4() -> Any:
    """spinbox"""
    ans = []
    window = tk.Tk()
    window.geometry("300x250")

    def submit() -> None:
        """Submit command."""
        ans.append(spinbox.get())
        window.destroy()

    option = ("Horror", "Classic")
    # spinbox = tk.Spinbox(window, from_=0, to=10, increment=2, font=('Helvetica', 20))
    spinbox = tk.Spinbox(window, values=option, font=('Helvetica', 20))
    spinbox.pack()

    label = tk.Label(window, text="Select")
    label.pack()

    btn1 = tk.Button(window, text='Submit', command=submit)
    btn1.pack(side='bottom')

    tk.Button(window, text="Quit", command=window.destroy).pack()
    window.mainloop()
    return ans[0]


def runner_questions() -> Dict:
    """
    Returns the input that was chosen by the user.
    """
    selected1 = []
    selected2 = []
    selected3 = []
    selected4 = []
    window = tk.Tk()
    frame1 = tk.LabelFrame(window, text="Movies", padx=15, pady=15)
    frame1.grid(row=0, column=0)
    listbox1 = tk.Listbox(frame1, height=5, selectmode='SINGLE')
    window.geometry("600x600")
    listbox1.insert(1, "Horror")
    listbox1.insert(2, "Classic")
    listbox1.insert(3, "Adventure")
    listbox1.insert(4, "Biography")
    listbox1.insert(5, "Animation")

    def submit1() -> None:
        """Collect user input and destroy the frame."""
        selected1.append(listbox1.curselection()[0])
        frame1.destroy()

    btn1 = tk.Button(frame1, text='Submit', command=submit1)
    btn1.pack(side='bottom')
    listbox1.pack()

    frame2 = tk.LabelFrame(window, text="Duration", padx=15, pady=15)
    frame2.grid(row=0, column=1)
    listbox2 = tk.Listbox(frame2, height=5, selectmode='SINGLE')
    listbox2.insert(1, "Short(<60 min)")
    listbox2.insert(2, "Medium (60-180 min)")
    listbox2.insert(3, "Long (>180 min)")

    def submit2() -> None:
        """Collect user input."""
        selected2.append(listbox2.curselection()[0])
        frame2.destroy()

    btn2 = tk.Button(frame2, text='Submit', command=submit2)
    btn2.pack(side='bottom')
    listbox2.pack()

    frame3 = tk.LabelFrame(window, text="Year", padx=15, pady=15)
    frame3.grid(row=1, column=0)
    decades = create_decade_options()
    listbox3 = tk.Listbox(frame3, height=len(decades), selectmode='SINGLE')
    for i in range(1, len(decades) + 1):
        listbox3.insert(i, decades[i - 1])

    def submit3() -> None:
        """Collect user input."""
        selected3.append(listbox3.curselection()[0])
        frame3.destroy()

    btn3 = tk.Button(frame3, text='Submit', command=submit3)
    btn3.pack(side='bottom')
    listbox3.pack()

    frame4 = tk.LabelFrame(window, text="Language", padx=15, pady=15)
    frame4.grid(row=1, column=1)
    listbox4 = tk.Listbox(frame4, height=5, selectmode='SINGLE')
    listbox4.insert(1, "Short(<60 min)")
    listbox4.insert(2, "Medium (60-180 min)")
    listbox4.insert(3, "Long (>180 min)")

    def submit4() -> None:
        """Collect user input."""
        selected4.append(listbox4.curselection()[0])
        frame4.destroy()

    btn4 = tk.Button(frame4, text='Submit', command=submit4)
    btn4.pack(side='bottom')
    listbox4.pack()

    window.mainloop()
    return {'genre': selected1, 'duration': selected2, 'year': selected3, 'language': selected4}


def runner_rankings() -> list:
    """Return the a list of rankings that the user chooses."""
    selected = []
    window = tk.Tk()
    listbox = tk.Listbox(window, height=5, selectmode='SINGLE')
    window.geometry("300x250")
    tk.Label(window, text="Ranking")
    listbox.insert(1, "Genre")
    listbox.insert(2, "Year")
    listbox.insert(3, "Duration")
    listbox.insert(4, "Release Year")
    listbox.insert(5, "Language")

    def submit() -> None:
        """Collect user selection and delete the option from listbox."""
        selected.append(listbox.curselection()[0])
        listbox.delete(listbox.curselection()[0])

    def finish() -> None:
        """Close the window."""
        window.destroy()

    btn1 = tk.Button(window, text='Submit', command=submit)
    btn2 = tk.Button(window, text='QUIT', command=finish)
    btn1.pack(side='bottom')
    btn2.pack()
    listbox.pack()
    window.mainloop()
    return selected


def main_runner() -> tuple:
    """Run the user interface functions."""
    a = runner_questions()
    b = runner_rankings()
    return (a, b)


def create_decade_options() -> list:
    """Return a tuple of decades."""
    decades = []
    for i in range(1960, 2020, 10):
        decades.append(f'{i}' + '-' + f'{i + 10}')

    return decades
