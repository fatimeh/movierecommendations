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
from typing import Tuple, Dict, Set, Any
import pandas as pd


# Reading .csv files
def load_datasets(movies_file: str) -> Graph:
    """
    Return a Movie object based on the details regarding movies in the given datasets.

    The Movie object class has multiple attributes that give information regarding the movies
    and information regarding this attributes will be derived from the two input datasets.

    Preconditions:
        - movies_file is the path to a CSV file corresponding to the IMDb movies data.
        - ratings_file is the path to a CSV file corresponding to the IMDb movie ratings data.
    """
    movie_graph = Graph()

    attributes = {'title', 'year', 'genre', 'duration', 'country', 'language', 'director'}
    movies = pd.read_csv(movies_file, usecols=lambda x: x in attributes)
    # breakpoint()
    for index in movies.index:
        title = str(movies['title'][index])
        release_year = int(movies['year'][index])
        genre = tuple(movies['genre'][index].split(','))
        duration = int(movies['duration'][index])
        country = tuple(movies['country'][index].split(','))
        language = str(movies['language'][index])
        director = str(movies['director'][index])
        movie = Movie(title, release_year, genre, duration, country, language, director)
        movie_graph.add_vertex(movie)

    return movie_graph


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

    The neighbours is a set of tuples where the first element of tuple is a vertex object and the second element 
    is a set of the traits that the vertices have in common.

    A Vertex is in the neighbours of this Vertex if it has at least one trait
    in common with this Vertex.

    Instance Attributes:
        - item: The data stored in this vertex, representing a movie.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - 
    
    """

    item: Movie
    neighbours: Set[Tuple[_Vertex, set]]

    def __init__(self, item: Movie, neighbours: Set[Tuple[_Vertex, set]]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = neighbours


# Graph Class
class Graph:
    """A weighted graph used to represent a movie network that keeps track of what trade each movie
    have in similar.
    There will be an edge between 2 movies if and only if there is at least 1 trade in common.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _WeightedVertex object.
    _vertices: dict[str, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Movie) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        self._vertices[item.title] = _Vertex(item, dict())

    def add_edge(self, item1: str, item2: str) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]
            common = [v1.item.release_year == v2.item.release_year, v1.item.genre == v2.item.genre,
                      v1.item.duration == v2.item.duration, v1.item.country == v2.item.country,
                      v1.item.language == v2.item.language, v1.item.director == v2.item.director]
            if any(common):
                name = ['release_year', 'genre', 'duration', 'country', 'language', 'director']
                for i in range(0, 6):
                    if not common[i]:
                        name.remove(name[i])

                v1.neighbours[v2] = set(name)
                v2.neighbours[v1] = set(name)
                return
            else:
                return
        else:
            raise ValueError

    def get_common_trade(self, item1: str, item2: str) -> set:
        """Return the common trade between the 2 movies.

        Return an empty set if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.neighbours.get(v2, set())

    def adjacent(self, item1: str, item2: str) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item.title == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: str) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* which is the movie data type are returned, not the _Vertex objects
        themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError
