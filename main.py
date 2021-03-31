"""CSC111 Winter 2021 Final Project

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Fatimeh Hassan, Shilin Zhang,
Dorsa Molaverdikhani, and Nimit Bhanshali.
"""
from dataclasses import dataclass
from typing import Tuple

# Reading .csv files


# Movie Object Class
@dataclass
class Movie:
    """
    A data class representing a movie.

    Instance Attributes:
    - title: the title of the movie
    - release_year: the year the movie was released
    - genre: the genre(s) of the movie
    - duration: the length of the movie (in minutes)
    - country: the name of the country/countries the movie was originally released in
    - language: the language the movie was written in
    - director: the name of the person that directed the movie

    Representation Invariants:

    """
    title: str
    release_year: int
    genre: Tuple[str]
    duration: int
    country: Tuple[str]
    language: str
    director: str

    def __init__(self, title: str, release_year: int, genre: Tuple[str], duration: int,
                 country: Tuple[str], language: str, director: str):
        self.title = title
        self.release_year = release_year
        self.genre = genre
        self.duration = duration
        self.country = country
        self.language = language
        self.director = director


# Vertex Class

# Graph Class
