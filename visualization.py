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
from typing import Dict, List, Any
import tkinter as tk

DURATIONS = ['Short(<60 min)', 'Medium (60-180 min)', 'Long (>180 min)']
RANKINGS = ['genre', 'release_year', 'language', 'duration']
GENRES = ['Western', 'Family', 'Adventure', 'War', 'Fantasy', 'History', 'Music', 'Documentary',
          'Reality-TV', 'Animation', 'Sport', 'Action', 'Mystery', 'Crime', 'Drama', 'Horror',
          'Film-Noir', 'Musical', 'Comedy', 'Adult', 'Romance', 'Sci-Fi', 'Biography', 'News',
          'Thriller']
LANGUAGES = ['Quechua', 'Gujarati', 'Kabyle', 'Mari', 'Filipino', 'Mongolian', 'Aramaic', 'Songhay',
             'Afrikaans', 'English', 'Crimean Tatar', 'Sicilian', 'American Sign Language']


def runner_questions(genres: List, languages: List) -> Dict[str, Any]:
    """
    Returns a dictionary where the keys are the 4 attributes that we asked the user to choose
    and the values are the user inputs for the 4 questions that we asked.

    The genres list contains all genres in our dataset and the languages list contains all
    languages in our dataset
    """
    answers_so_far = {}
    duration = ['Short(<60 min)', 'Medium (60-180 min)', 'Long (>180 min)']
    window = tk.Tk()
    window.geometry("600x600")
    create_genres_listbox(window, answers_so_far, genres)
    create_duration_listbox(window, answers_so_far, duration)
    create_year_listbox(window, answers_so_far)
    create_language_listbox(window, answers_so_far, languages)

    window.mainloop()
    return answers_so_far


def create_decade_options(start_year: int, end_year: int) -> tuple:
    """Return a tuple of list where the first list contains all the decades between the
    starting year and ending year that we asked the user to choose (starting year is 1960
    to end year is 2020) as texts and the second list contains the same decades except
    that each item are a tuple of integers where the first integer is the starting
    year of that decade and the second number is the ending year of that decade.

    Preconditions:
        - start_year >= 0
        - end_year >= 0
    """
    decades_string = []
    decades_tuple = []
    for i in range(start_year, end_year, 10):
        decades_string.append(f'{i}' + '-' + f'{i + 10}')
        decades_tuple.append((i, i + 10))

    return (decades_string, decades_tuple)


def create_genres_listbox(window: tk.Tk, user_answer: dict, genres: List) -> None:
    """Create the listbox that allows user to choose their genres preference
     and a button to submit their input

     This method will mutate the user_answer dictionary when the submit button is clicked
     to add the user's answer to the current attribute

     The user_answer dictionary is the collection that contains all answers that
     the user give so far and the genres list contains all the genres in our dataset

     Preconditions:
        - 0 <= len(user_answer) < 5

     """
    genre_frame = tk.LabelFrame(window, text="What genre do you prefer?", padx=15, pady=15)
    genre_frame.grid(row=0, column=0)
    genre_listbox = tk.Listbox(genre_frame, height=5, selectmode='SINGLE')
    for i in range(len(genres)):
        genre_listbox.insert(i + 1, genres[i])

    def submit() -> None:
        """Collect whatever user choose for their preference for genres and close the window if
        user answers all the question on the window."""
        user_answer['genres'] = genres[genre_listbox.curselection()[0]]
        genre_frame.destroy()
        if len(user_answer) == 4:
            window.destroy()

    submit_button = tk.Button(genre_frame, text='Submit', command=submit)
    submit_button.pack(side='bottom')
    genre_listbox.pack()


def create_duration_listbox(window: tk.Tk, user_answer: dict, duration: List) -> None:
    """Create the listbox that allows user to choose their movie duration preference
        and a button to submit their input

        This method will mutate the user_answer dictionary when the submit button is clicked
        to add the user's answer to the current attribute

        The user_answer dictionary is the collection that contains all answers that
        the user give so far and the duration list contains our way of dividing the
        duration into range

     Preconditions:
        - len(duration) == 3
        - 0 <= len(user_answer) < 5

    """
    duration_frame = tk.LabelFrame(window, text="What duration do you want?", padx=15, pady=15)
    duration_frame.grid(row=0, column=1)
    duration_listbox = tk.Listbox(duration_frame, height=5, selectmode='SINGLE')
    duration_listbox.insert(1, duration[0])
    duration_listbox.insert(2, duration[1])
    duration_listbox.insert(3, duration[2])

    def submit() -> None:
        """Collect whatever user choose for their preference for movie duration and close the
        window if user answers all the question on the window."""
        user_answer['duration'] = duration[duration_listbox.curselection()[0]]
        duration_frame.destroy()
        if len(user_answer) == 4:
            window.destroy()

    submit_button = tk.Button(duration_frame, text='Submit', command=submit)
    submit_button.pack(side='bottom')
    duration_listbox.pack()


def create_year_listbox(window: tk.Tk, user_answer: dict) -> None:
    """Create the listbox that allows user to choose their release year preference
     and a button to submit their input

     This method will mutate the user_answer dictionary when the submit button is clicked
     to add the user's answer to the current attribute

     The user_answer dictionary is the collection that contains all answers that
     the user give so far

     Preconditions:
        - 0 <= len(user_answer) < 5

    """
    year_frame = tk.LabelFrame(window, text="Which decade do you prefer?", padx=15, pady=15)
    year_frame.grid(row=1, column=0)
    decades_string = create_decade_options(1960, 2020)[0]
    decades_tuples = create_decade_options(1960, 2020)[1]
    year_listbox = tk.Listbox(year_frame, height=len(decades_string), selectmode='SINGLE')
    for i in range(1, len(decades_string) + 1):
        year_listbox.insert(i, decades_string[i - 1])

    def submit() -> None:
        """Collect whatever user choose for their preference for release year and close
        the window if user answers all the question on the window."""
        user_answer['release_year'] = decades_tuples[year_listbox.curselection()[0]]
        year_frame.destroy()
        if len(user_answer) == 4:
            window.destroy()

    submit_button = tk.Button(year_frame, text='Submit', command=submit)
    submit_button.pack(side='bottom')
    year_listbox.pack()


def create_language_listbox(window: tk.Tk, user_answer: dict, languages: List) -> None:
    """Create the listbox that allows user to choose their language preference
     and a button to submit their input.

     This method will mutate the user_answer dictionary when the submit button is clicked
     to add the user's answer to the current attribute

     The user_answer dictionary is the collection that contains all answers that
     the user give so far and the language list is a list with all languages in our dataset

     Preconditions:
        - 0 <= len(user_answer) < 5

     """
    language_frame = tk.LabelFrame(window, text="Which language do you want?", padx=15, pady=15)
    language_frame.grid(row=1, column=1)
    language_listbox = tk.Listbox(language_frame, height=5, selectmode='SINGLE')
    for j in range(0, len(languages)):
        language_listbox.insert(j + 1, languages[j])

    def submit() -> None:
        """Collect whatever user choose for their preference for language and close the window if
        user answers all the question on the window."""
        user_answer['language'] = languages[language_listbox.curselection()[0]]
        language_frame.destroy()
        if len(user_answer) == 4:
            window.destroy()

    submit_button = tk.Button(language_frame, text='Submit', command=submit)
    submit_button.pack(side='bottom')
    language_listbox.pack()


def runner_rankings(ranking: List) -> list:
    """Return the a list of rankings that the user chooses.
    The first item is the attributes that the user rank first which is the most important
    The second item is the second most important attributes that the user rank and so on.

    The parameter ranking is a list with the 4 attributes that we ask users to rank

    Preconditions:
        - len(ranking) == 4

    """
    rank = []
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
    ranking_listbox = tk.Listbox(window, height=5, selectmode='SINGLE')
    ranking_listbox.insert(1, ranking[0])
    ranking_listbox.insert(2, ranking[1])
    ranking_listbox.insert(3, ranking[2])
    ranking_listbox.insert(4, ranking[3])

    def submit() -> None:
        """Collect user selection and delete the option from listbox."""
        rank.append(ranking[ranking_listbox.curselection()[0]])
        ranking.remove(ranking[ranking_listbox.curselection()[0]])
        ranking_listbox.delete(ranking_listbox.curselection()[0])
        if ranking_listbox.size() == 0:
            window.destroy()

    submit_button = tk.Button(window, text='Submit', command=submit)
    submit_button.pack(side='bottom')
    ranking_listbox.pack()
    window.mainloop()
    return rank


def main_runner() -> tuple:
    """Display the ranking and the questions window to get the user input and return
    the output of the 2 methods as a tuple where the first is the ranking output and
    the second is their answers to the fours question that we ask."""
    rankings = runner_rankings(RANKINGS)
    questions = runner_questions(GENRES, LANGUAGES)
    return (rankings, questions)


def display_recommended_movies(recommended_movies: List) -> None:
    """Display all the recommended movies for the particular user input in order of how much
    we recommend the movie.
    The first movie that is displayed on the screen is the most recommended movie and
    the second movie is the second most recommended and so on.

    The recommended_movies are the list of recommended movies

    Preconditions:
        - len(recommended_movies) == 10

    """
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
