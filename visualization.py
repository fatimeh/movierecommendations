"""CSC111 Winter 2021 Final Project: Visualization

Overview and Description
========================

This Python module contains the functions for the user interface and
visualization of the movie recommender system.

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
from typing import Dict, List, Any, Tuple
import tkinter as tk
import pandas as pd


def load_genres_and_languages(movies_file: str) -> Tuple[List, List]:
    """
    Return a tuple of two lists, Genres and Languages.

    The Genres list will be an alphabetically sorted list containing all the genres available
    in our dataset.

    The Language list will be an alphabetically sorted list containing all the languages
    available in our dataset.

    Preconditions:
        - movies_file is the path to a CSV file corresponding to the IMDb movies data.
    """
    genres = set()
    languages = set()
    movies = pd.read_csv(movies_file, usecols={'genre', 'language'})

    for index in movies.index:
        genres.update(set(movies['genre'][index].split(', ')))
        languages.update(set(movies['language'][index].split(', ')))

    genres_lst = list(genres)
    languages_lst = list(languages)

    genres_lst.sort()
    languages_lst.sort()

    return (genres_lst, languages_lst)


def runner_questions(genres: List, languages: List) -> Dict[str, Any]:
    """
    Returns a dictionary where the keys are the 4 attributes that we asked the user to choose
    and the values are the user inputs for the 4 questions that we asked.

    The genres list contains all genres in the dataset and the languages list contains all
    languages in the dataset
    """
    answers_so_far = {}
    duration = ['Short(<60 min)', 'Medium (60-180 min)', 'Long (>180 min)']
    window = tk.Tk()
    window.geometry("600x600")
    window.configure(bg="black")
    create_genres_listbox(window, answers_so_far, genres)
    create_duration_listbox(window, answers_so_far, duration)
    create_year_listbox(window, answers_so_far)
    create_language_listbox(window, answers_so_far, languages)

    window.mainloop()
    return answers_so_far


def create_decade_options(start_year: int, end_year: int) -> tuple:
    """Return a tuple where the first element is a list containing the string representation of
     all the decades between the starting year and ending yearand the second element is a list
     containing the same decades except that each item is a tuple of integers where the first
     integer is the starting year of that decade and the second number
     is the ending year of that decade.

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


def create_genres_listbox(window: tk.Tk, user_answer: dict, genres: List[str]) -> None:
    """Create the listbox that allows user to choose their favourite genres.

     This method will mutate the user_answer dictionary when the submit button is clicked
     to add the user's answer to user_answer dictionary.

     The user_answer dictionary is a dictionary that contains all of the answers that
     the user has given so far and the genres list contains all of the genres in the dataset.

     Preconditions:
        - 0 <= len(user_answer) < 5

     """
    genre_frame = tk.LabelFrame(window, text="What genre do you prefer?", bg="black", fg="white",
                                padx=15, pady=15)
    genre_frame.grid(row=0, column=0)
    genre_listbox = tk.Listbox(genre_frame, fg="white", bg="blue", height=5, selectmode='SINGLE')
    for i in range(len(genres)):
        genre_listbox.insert(i + 1, genres[i])

    def submit() -> None:
        """Collect the user's choice for the genres and close the window if
        user answers all the question on the window."""
        user_answer['genres'] = genres[genre_listbox.curselection()[0]]
        genre_frame.destroy()
        if len(user_answer) == 4:
            window.destroy()

    submit_button = tk.Button(genre_frame, fg="black", text='Submit', command=submit)
    submit_button.pack(side='bottom')
    genre_listbox.pack()


def create_duration_listbox(window: tk.Tk, user_answer: dict, duration: List) -> None:
    """Create the listbox that allows user to choose their movie duration preference.

        This method will mutate the user_answer dictionary when the submit button is clicked
        to add the user's answer to the user_answer dictionary.

        The user_answer dictionary is the dictionary that contains all of the answers that
        the user has given so far.

     Preconditions:
        - len(duration) == 3
        - 0 <= len(user_answer) < 5

    """
    duration_frame = tk.LabelFrame(window, text="What duration do you want?", bg="black",
                                   fg="white", padx=15, pady=15)
    duration_frame.grid(row=0, column=1)
    duration_listbox = tk.Listbox(duration_frame, height=5, selectmode='SINGLE',
                                  fg="white", bg="blue")
    duration_listbox.insert(1, duration[0])
    duration_listbox.insert(2, duration[1])
    duration_listbox.insert(3, duration[2])

    def submit() -> None:
        """Collect the user's choice for the movie duration and close the
        window if user answers all the question on the window."""
        user_answer['duration'] = duration[duration_listbox.curselection()[0]]
        duration_frame.destroy()
        if len(user_answer) == 4:
            window.destroy()

    submit_button = tk.Button(duration_frame, text='Submit', fg="black", command=submit)
    submit_button.pack(side='bottom')
    duration_listbox.pack()


def create_year_listbox(window: tk.Tk, user_answer: dict) -> None:
    """Create the listbox that allows user to choose their release year preference.

     This method will mutate the user_answer dictionary when the submit button is clicked
     to add the user's answer to user_answer dictionary.

     The user_answer dictionary is the dictionary that contains all of the answers that
     the user has given so far.

     Preconditions:
        - 0 <= len(user_answer) < 5

    """
    year_frame = tk.LabelFrame(window, text="Which decade do you prefer?", fg="white", bg="black",
                               padx=15, pady=15)
    year_frame.grid(row=1, column=0)
    decades_string = create_decade_options(1890, 2020)[0]
    decades_tuples = create_decade_options(1890, 2020)[1]
    year_listbox = tk.Listbox(year_frame, height=10, selectmode='SINGLE', fg="white", bg="blue")
    for i in range(1, len(decades_string) + 1):
        year_listbox.insert(i, decades_string[i - 1])

    def submit() -> None:
        """Collect the user's choice for release year and close
        the window if user answers all the question on the window."""
        user_answer['release_year'] = decades_tuples[year_listbox.curselection()[0]]
        year_frame.destroy()
        if len(user_answer) == 4:
            window.destroy()

    submit_button = tk.Button(year_frame, text='Submit', fg="black", command=submit)
    submit_button.pack(side='bottom')
    year_listbox.pack()


def create_language_listbox(window: tk.Tk, user_answer: dict, languages: List) -> None:
    """Create the listbox that allows user to choose their language preference.

     This method will mutate the user_answer dictionary when the submit button is clicked
     to add the user's answer to the user_answer dictionary.

     The user_answer dictionary is the dictionary that contains all of the answers that
     the user has given so far and the language list is a list that has all languages
     in the dataset.

     Preconditions:
        - 0 <= len(user_answer) < 5

     """
    language_frame = tk.LabelFrame(window, text="Which language do you want?", fg="white",
                                   bg="black", padx=15, pady=15)
    language_frame.grid(row=1, column=1)
    language_listbox = tk.Listbox(language_frame, height=10, selectmode='SINGLE', fg="white",
                                  bg="blue")
    for j in range(0, len(languages)):
        language_listbox.insert(j + 1, languages[j])

    def submit() -> None:
        """Collect the user's choice for language and close the window if
        user answers all the question on the window."""
        user_answer['language'] = languages[language_listbox.curselection()[0]]
        language_frame.destroy()
        if len(user_answer) == 4:
            window.destroy()

    submit_button = tk.Button(language_frame, text='Submit', command=submit, fg="black")
    submit_button.pack(side='bottom')
    language_listbox.pack()


def runner_rankings() -> list:
    """Return the a list of rankings that the user chooses.
    The first item is the attributes that the user ranks first which is the most important, and
    the second item is the second most important attribute that the user ranks and so on.

    The ranking parameter is a list with the 4 attributes that the users will rank.

    """
    ranking = ['Genre', 'Release Year', 'Language', 'Duration']
    user_ranking = []
    window = tk.Tk()
    window.geometry("800x600")
    window.configure(bg="black")
    tk.Label(window, text="Ranking", fg="white", bg="black").pack()
    tk.Label(window, text="Please take a look at the following 4 attributes "
                          "and rank them in order of importance to you.", fg="white",
             bg="black").pack()
    tk.Label(window, text="First, select the most important attribute and click submit.",
             fg="white", bg="black").pack()
    tk.Label(window, text="Then, select the next attribute in your rankings and click "
                          "submit.", fg="white", bg="black").pack()
    tk.Label(window, text="Repeatedly select and click submit in your chosen order of importance"
                          " until you have submitted all four attributes.", fg="white",
             bg="black").pack()
    ranking_listbox = tk.Listbox(window, height=5, selectmode='SINGLE', fg="white", bg="blue")
    ranking_listbox.insert(1, ranking[0])
    ranking_listbox.insert(2, ranking[1])
    ranking_listbox.insert(3, ranking[2])
    ranking_listbox.insert(4, ranking[3])

    def submit() -> None:
        """Collect user selection and delete the option from listbox."""
        user_ranking.append(ranking[ranking_listbox.curselection()[0]])
        ranking_listbox.delete(ranking_listbox.curselection()[0])
        if ranking_listbox.size() == 0:
            window.destroy()

    submit_button = tk.Button(window, text='Submit', command=submit, fg="black")
    submit_button.pack()
    ranking_listbox.pack()
    window.mainloop()
    return user_ranking


def main_runner() -> Tuple[list, dict]:
    """Display the ranking and the questions window to get the user input and return
    the output as a tuple where the first element is the ranking output and
    the second element is a dictionary containing the user's answers to the four questions."""
    rankings = runner_rankings()
    genres, languages = load_genres_and_languages('IMDb movies.csv')
    questions = runner_questions(genres, languages)
    return (rankings, questions)


def display_recommended_movies(recommended_movies: List) -> None:
    """Display all the recommended movies for the particular user input in order of how much
    we recommend the movie.
    The first movie that is displayed on the screen is the most recommended movie and
    the second movie is the second most recommended and so on.

    The recommended_movies are the list of recommended movies.

    Preconditions:
        - len(recommended_movies) <= 10

    """
    window = tk.Tk()
    window.geometry("500x500")
    window.configure(bg="black")

    i = len(recommended_movies)

    if recommended_movies == []:
        tk.Label(window, text="We were unable to find movies that match your preferences.",
                 fg="white", bg="black").pack()
    else:
        tk.Label(window, text='The ' + f'{i}' + ' recommended movies are listed below:',
                 fg="white", bg="black").pack()

        for index in range(0, len(recommended_movies)):
            tk.Label(window, text=recommended_movies[index], fg="white", bg="black").pack()

    window.mainloop()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # import python_ta.contracts
    # python_ta.contracts.DEBUG_CONTRACTS = False
    # python_ta.contracts.check_all_contracts()
    #
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'extra-imports': ['typing', 'tkinter', 'pandas'],
    #     'allowed-io': []
    # })
