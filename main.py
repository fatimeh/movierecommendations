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
class _Graph:
    """A weighted graph used to represent a movie network that keeps track of what trade each movie
    have in similar.
    There will be an edge between 2 movies if and only if there is at least 1 trade in common.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _WeightedVertex object.
    _vertices: dict[Movie, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Movie) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        self._vertices[item] = _Vertex(item, dict())

    def add_edge(self, item1: Movie, item2: Movie) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            common = [item1.release_year == item2.release_year, item1.genre == item2.genre,
                      item1.duration == item2.duration, item1.country == item2.country,
                      item1.language == item2.language, item1.director == item2.director]
            if any(common):
                v1 = self._vertices[item1]
                v2 = self._vertices[item2]
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

    def get_common_trade(self, item1: Movie, item2: Movie) -> set:
        """Return the common trade between the 2 movies.

        Return an empty set if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.neighbours.get(v2, set())

    def adjacent(self, item1: Movie, item2: Movie) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Movie) -> set:
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
