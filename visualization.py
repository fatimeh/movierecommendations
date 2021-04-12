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
from typing import Dict, List
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
    window.geometry("600x600")
    create_genres_listbox(window, options)
    create_duration_listbox(window, options)
    create_year_listbox(window, options)
    create_language_listbox(window, options)

    window.mainloop()
    return options


def create_decade_options(start_year: int, end_year: int) -> tuple:
    """Return a tuple of decades."""
    decades = []
    decades_tuple = []
    for i in range(start_year, end_year, 10):
        decades.append(f'{i}' + '-' + f'{i + 10}')
        decades_tuple.append((i, i + 10))

    return (decades, decades_tuple)


def create_genres_listbox(window: tk.Tk, options: dict) -> None:
    """Create listbox"""
    genre_frame = tk.LabelFrame(window, text="What genre do you prefer?", padx=15, pady=15)
    genre_frame.grid(row=0, column=0)
    genre_listbox = tk.Listbox(genre_frame, height=5, selectmode='SINGLE')
    for i in range(len(GENRES)):
        genre_listbox.insert(i + 1, GENRES[i])

    def submit() -> None:
        """Collect user input and destroy the frame."""
        options['genres'] = GENRES[genre_listbox.curselection()[0]]
        genre_frame.destroy()

    button = tk.Button(genre_frame, text='Submit', command=submit)
    button.pack(side='bottom')
    genre_listbox.pack()


def create_duration_listbox(window: tk.Tk, options: dict) -> None:
    """Create listbox2."""
    duration_frame = tk.LabelFrame(window, text="What duration do you want?", padx=15, pady=15)
    duration_frame.grid(row=0, column=1)
    duration_listbox = tk.Listbox(duration_frame, height=5, selectmode='SINGLE')
    duration_listbox.insert(1, "Short(<60 min)")
    duration_listbox.insert(2, "Medium (60-180 min)")
    duration_listbox.insert(3, "Long (>180 min)")

    def submit() -> None:
        """Collect user input."""
        options['duration'] = DURATIONS[duration_listbox.curselection()[0]]
        duration_frame.destroy()

    button = tk.Button(duration_frame, text='Submit', command=submit)
    button.pack(side='bottom')
    duration_listbox.pack()


def create_year_listbox(window: tk.Tk, options: dict) -> None:
    """Create listbox2."""
    year_frame = tk.LabelFrame(window, text="Which decade do you prefer?", padx=15, pady=15)
    year_frame.grid(row=1, column=0)
    decades = create_decade_options(1960, 2020)[0]
    decades_tuples = create_decade_options(1960, 2020)[1]
    year_listbox = tk.Listbox(year_frame, height=len(decades), selectmode='SINGLE')
    for i in range(1, len(decades) + 1):
        year_listbox.insert(i, decades[i - 1])

    def submit() -> None:
        """Collect user input."""
        options['release_year'] = decades_tuples[year_listbox.curselection()[0]]
        year_listbox.destroy()

    button = tk.Button(year_frame, text='Submit', command=submit)
    button.pack(side='bottom')
    year_listbox.pack()


def create_language_listbox(window: tk.Tk, options: dict) -> None:
    """Create listbox4."""
    language_frame = tk.LabelFrame(window, text="Which language do you want?", padx=15, pady=15)
    language_frame.grid(row=1, column=1)
    language_listbox = tk.Listbox(language_frame, height=5, selectmode='SINGLE')
    for j in range(0, len(LANGUAGES)):
        language_listbox.insert(j + 1, LANGUAGES[j])

    def submit() -> None:
        """Collect user input."""
        options['language'] = LANGUAGES[language_listbox.curselection()[0]]
        language_frame.destroy()

    button = tk.Button(language_frame, text='Submit', command=submit)
    button.pack(side='bottom')
    language_listbox.pack()


def runner_rankings() -> list:
    """Return the a list of rankings that the user chooses."""
    selected = []
    window = tk.Tk()
    window.geometry("800x800")
    tk.Label(window, text="Ranking").pack()
    tk.Label(window, text="Please think about the following 4 attributes "
                          "and see which one you cares the most").pack()
    tk.Label(window, text="Select the one that is the most important and click submit").pack()
    tk.Label(window, text="Then select the one that is the second most important and click "
                          "submit").pack()
    tk.Label(window, text="Repeatedly select and click submit in order of importance"
                          " until you select all four").pack()
    listbox = tk.Listbox(window, height=5, selectmode='SINGLE')
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


def display_recommended_movies(recommended_movies: List) -> None:
    """Display the recommended movies"""
    window = tk.Tk()
    window.geometry("500x500")

    tk.Label(window, text="The 10 recommended movies are listed below").pack()

    for i in range(0, 10):
        tk.Label(window, text=recommended_movies[i]).pack()

    window.mainloop()


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
