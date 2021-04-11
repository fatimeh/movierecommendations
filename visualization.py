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
from typing import Any, Dict
import tkinter as tk

DURATIONS = ['Short(<60 min)', 'Medium (60-180 min)', 'Long (>180 min)']
RANKINGS = ['genre', 'release_year', 'language', 'duration']
GENRES = ['Western', 'Family', 'Adventure', 'War', 'Fantasy', 'History', 'Music', 'Documentary',
          'Reality-TV', 'Animation', 'Sport', 'Action', 'Mystery', 'Crime', 'Drama', 'Horror',
          'Film-Noir', 'Musical', 'Comedy', 'Adult', 'Romance', 'Sci-Fi', 'Biography', 'News',
          'Thriller']
LANGUAGES = ['Quechua', 'Gujarati', 'Kabyle', 'Mari', 'Filipino', 'Mongolian', 'Aramaic', 'Songhay',
             'Afrikaans', 'English', 'Crimean Tatar', 'Sicilian', 'American Sign Language']

def runner_questions() -> Dict:
    """
    Returns the input that was chosen by the user.
    """
    options = {}
    window = tk.Tk()
    frame1 = tk.LabelFrame(window, text="What genre do you prefer?", padx=15, pady=15)
    frame1.grid(row=0, column=0)
    listbox1 = tk.Listbox(frame1, height=5, selectmode='SINGLE')
    window.geometry("600x600")
    for i in range(len(GENRES)):
        listbox1.insert(i + 1, GENRES[i])

    def submit1() -> None:
        """Collect user input and destroy the frame."""
        options['genres'] = GENRES[listbox1.curselection()[0]]
        frame1.destroy()

    btn1 = tk.Button(frame1, text='Submit', command=submit1)
    btn1.pack(side='bottom')
    listbox1.pack()

    frame2 = tk.LabelFrame(window, text="What duration do you want?", padx=15, pady=15)
    frame2.grid(row=0, column=1)
    listbox2 = tk.Listbox(frame2, height=5, selectmode='SINGLE')
    listbox2.insert(1, "Short(<60 min)")
    listbox2.insert(2, "Medium (60-180 min)")
    listbox2.insert(3, "Long (>180 min)")

    def submit2() -> None:
        """Collect user input."""
        options['duration'] = DURATIONS[listbox2.curselection()[0]]
        frame2.destroy()

    btn2 = tk.Button(frame2, text='Submit', command=submit2)
    btn2.pack(side='bottom')
    listbox2.pack()

    frame3 = tk.LabelFrame(window, text="Which decade do you prefer?", padx=15, pady=15)
    frame3.grid(row=1, column=0)
    decades = create_decade_options()[0]
    decades_tuples = create_decade_options()[1]
    listbox3 = tk.Listbox(frame3, height=len(decades), selectmode='SINGLE')
    for i in range(1, len(decades) + 1):
        listbox3.insert(i, decades[i - 1])

    def submit3() -> None:
        """Collect user input."""
        options['release_year'] = decades_tuples[listbox3.curselection()[0]]
        frame3.destroy()

    btn3 = tk.Button(frame3, text='Submit', command=submit3)
    btn3.pack(side='bottom')
    listbox3.pack()

    frame4 = tk.LabelFrame(window, text="Which language do you want?", padx=15, pady=15)
    frame4.grid(row=1, column=1)
    listbox4 = tk.Listbox(frame4, height=5, selectmode='SINGLE')
    for j in range(0, len(LANGUAGES)):
        listbox4.insert(j + 1, LANGUAGES[j])

    def submit4() -> None:
        """Collect user input."""
        options['language'] = LANGUAGES[listbox4.curselection()[0]]
        frame4.destroy()

    btn4 = tk.Button(frame4, text='Submit', command=submit4)
    btn4.pack(side='bottom')
    listbox4.pack()

    window.mainloop()
    return options


def runner_rankings() -> list:
    """Return the a list of rankings that the user chooses."""
    selected = []
    selected = []
    window = tk.Tk()
    listbox = tk.Listbox(window, height=5, selectmode='SINGLE')
    window.geometry("300x300")
    listbox.insert(1, 'genre')
    listbox.insert(2, 'release_year')
    listbox.insert(3, 'language')
    listbox.insert(4, 'duration')

    def submit() -> None:
        """Collect user selection and delete the option from listbox."""
        selected.append(RANKINGS[listbox.curselection()[0]])
        RANKINGS.remove(RANKINGS[listbox.curselection()[0]])
        listbox.delete(listbox.curselection()[0])
        if listbox.size() == 0:
            window.destroy()

    btn1 = tk.Button(window, text='Submit', command=submit)
    btn1.pack(side='bottom')
    listbox.pack()
    window.mainloop()
    return selected




if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['typing', 'tkinter'],
        'allowed-io': []
    })
