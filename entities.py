"""CSC111 Winter 2021 Final Project

Overview and Description
========================

This Python module contains the dataclasses and the function to read the
dataset. This includes the Movie class, the MovieGraph class, and the MovieVertex
class.

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
from typing import Set, List
import pandas as pd

RATING_BENCHMARK = 8.0


# Reading .csv files
def load_dataset(movies_file: str, user_movie: Movie) -> MovieGraph:
    """
    Return a MovieGraph based on the details regarding movies in the given datasets.

    The user_movie is a Movie object that represents the user preferences for a movie, which
    will be added as a vertex in the MovieGraph.

    Each vertex added in the MovieGraph will represent a movie and each edge added will
    represent the common traits between the user_movie and all of the other vertices.

    Preconditions:
        - movies_file is the path to a CSV file corresponding to the IMDb movies data.
    """
    movie_graph = MovieGraph()

    attributes = {'imdb_title_id', 'title', 'year', 'genre', 'duration', 'language', 'avg_vote'}
    movies = pd.read_csv(movies_file, usecols=lambda x: x in attributes)
    movie_graph.add_vertex(user_movie)

    for index in movies.index:
        title = str(movies['title'][index])
        release_year = {int(movies['year'][index])}
        genre = set(movies['genre'][index].split(','))
        duration = {int(movies['duration'][index])}
        language = set(str(movies['language'][index]).split(','))
        rating = float(movies['avg_vote'][index])
        movie = Movie(title, release_year, genre, duration, language, rating)
        movie_graph.add_vertex(movie)
        movie_graph.add_edge(user_movie.title, title)

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
        - language: the language the movie was written in
        - rating: the total average weighted rating the movie received
    """
    title: str
    release_year: Set[int]
    genre: Set[str]
    duration: Set[int]
    language: Set[str]
    rating: float

    def __init__(self, title: str, release_year: Set[int], genre: Set[str], duration: Set[int],
                 language: Set[str], rating: float):
        self.title = title
        self.release_year = release_year
        self.genre = genre
        self.duration = duration
        self.language = language
        self.rating = rating


# Vertex Class
class _MovieVertex:
    """
    A vertex in the movie graph.

    Each vertex item is an instance of a Movie class.

    The neighbours is a dictionary where the key is a _MovieVertex object and the value is
    a set of the traits that the vertex and its neighbours have in common.

    A Vertex is in the neighbours of this Vertex if it has at least one trait
    in common with this Vertex.

    Instance Attributes:
        - item: The data stored in this vertex, representing a Movie object.
        - neighbours: The vertices that are adjacent to this vertex.

    """

    item: Movie
    neighbours: dict[_MovieVertex, set]

    def __init__(self, item: Movie) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = {}


# Graph Class
class MovieGraph:
    """A weighted graph used to represent a movie network that keeps track of the common traits
    between movies.

    There will be an edge between 2 movies if and only if there is at least 1 trade in common.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps movie title to _MovieVertex object.
    _vertices: dict[str, _MovieVertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Movie) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        self._vertices[item.title] = _MovieVertex(item)

    def add_edge(self, item1: str, item2: str) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]
            common = [
                any(g1 == g2 for g1 in v1.item.release_year for g2 in v2.item.release_year),
                any(g1 == g2 for g1 in v1.item.genre for g2 in v2.item.genre),
                any(g1 == g2 for g1 in v1.item.duration for g2 in v2.item.duration),
                any(l1 == l2 for l1 in v1.item.language for l2 in v2.item.language)]
            if any(common):
                name = ['release_year', 'genre', 'duration', 'language']

                set_so_far = set()
                for i in range(len(common)):
                    if common[i]:
                        set_so_far.add(name[i])

                v1.neighbours[v2] = set_so_far
                v2.neighbours[v1] = set_so_far
        else:
            raise ValueError

    def get_common_trait(self, item1: str, item2: str) -> set:
        """Return a set of common traits between the given movies.

        Return an empty set if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        common = set()
        for vertex in v1.neighbours:
            if vertex == v2:
                common = v1.neighbours[vertex]

        return common

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

        Note that the titles of the neighbour movies are returned, not the _Vertex objects
        themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item.title for neighbour in v.neighbours}
        else:
            raise ValueError

    def similarity_score(self, movie: str, user: str, preferences: List[str]) \
            -> int:
        """Calculate the similarity score between a movie vertex and a user vertex, given
        the order of the user's preferences.

        Preconditions:
            - len(preferences) == 4
            - all({preferences[x] in {'genre', 'release_year', 'language', 'duration'}
            for x in range(0, 4)})

        """
        final_score = 0
        common_traits = self.get_common_trait(movie, user)

        totals = {0: 10, 1: 5, 2: 3, 3: 1}

        for i in range(0, 4):
            if preferences[i] == 'genre' and 'genre' in common_traits:
                final_score += totals[i]
            elif preferences[i] == 'release_year' and 'release_year' in common_traits:
                final_score += totals[i]
            elif preferences[i] == 'language' and 'language' in common_traits:
                final_score += totals[i]
            elif preferences[i] == 'duration' and 'duration' in common_traits:
                final_score += totals[i]

        return final_score

    def recommend_movies(self, user: str, preferences: List[str]) -> List[str]:
        """Return a list of recommended movies in order of highest similarity score to lowest,
        given a user vertex and a list of user preferences.

        In the case two movies have the same similarity score, the movies will be ranked in terms
        of the IMDb rating they received.
        """
        movies = {}
        final_movies = []

        for neighbour in self._vertices[user].neighbours:
            if neighbour.item.rating >= RATING_BENCHMARK:
                title = neighbour.item.title
                score = self.similarity_score(user, title, preferences)
                if score >= 10:
                    movies[title] = score + (neighbour.item.rating / 10)

        sorted_movies = sorted(movies.items(), key=lambda x: x[1], reverse=True)

        for movie in sorted_movies:
            final_movies.append(movie[0])

        return final_movies
