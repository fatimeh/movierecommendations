"""CSC111 Winter 2021 Final Project

Overview and Description
========================

This Python module contains the main runner function for the
movie recommendation system.

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
from entities import Movie, load_dataset
from visualization import main_runner, display_recommended_movies


def main() -> None:
    """"
    The main function that will recommend movies to the user based on their preferences.
    """
    # Call the user interface functions to get the user input
    # Create user vertex and movie graph based on input
    # Call the recommendation function and get the list of movies
    # Display the recommended movies
    user_preferences, user_input = main_runner()

    for i in range(len(user_preferences)):
        if user_preferences[i] == 'Genre':
            user_preferences[i] = 'genre'
        elif user_preferences[i] == 'Release Year':
            user_preferences[i] = 'release_year'
        elif user_preferences[i] == 'Language':
            user_preferences[i] = 'language'
        else:
            user_preferences[i] = 'duration'

    start_year = user_input['release_year'][0]
    stop_year = user_input['release_year'][1]
    year_range = {year for year in range(start_year, stop_year)}

    genre = user_input['genres']

    duration_str = user_input['duration']

    if duration_str == 'Short(<60 min)':
        duration_tpl = (0, 60)
    elif duration_str == 'Medium (60-180 min)':
        duration_tpl = (60, 181)
    else:
        duration_tpl = (181, 809)

    duration_range = {duration for duration in range(duration_tpl[0], duration_tpl[1])}

    language = user_input['language']

    user = Movie('user', 'User', year_range, {genre}, duration_range, {language}, 5.0)

    graph = load_dataset('IMDb movies.csv', user)
    movies = graph.recommend_movies(user.movie_id, user_preferences)
    display_recommended_movies(movies)


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
    #     'extra-imports': ['entities', 'visualization'],
    #     'allowed-io': []
    # })
