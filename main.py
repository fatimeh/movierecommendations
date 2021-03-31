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
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Dict, Set

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
class _Vertex:
    """
    A vertex in the graph.
    
    Each vertex item is an instance of a Movie class.
    
    The neighbours is a dictionary which maps the _Vertex object to the set of the traits
    which this Vertex and its neighbour have in common.
    
    A Vertex is in the neighbours of this Vertex if it has at least one trait
    in common with this Vertex.

    Instance Attributes:
        - item: The data stored in this vertex, representing a movie.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - all(self.neighbours[v] != set() for v in self.neighbours)
    """
    
    item: Movie
    neighbours: Dict[_Vertex, Set[str]]

    def __init__(self, item: Movie, neighbours: Dict[_Vertex, Set[str]]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = neighbours

# Graph Class
