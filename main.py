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
from typing import Set, List, Any
import pandas as pd
import tkinter as tk

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


def runner4() -> Any:
    """spinbox"""
    ans = []
    window = tk.Tk()
    window.geometry("300x250")

    def submit() -> None:
        """Submit command."""
        ans.append(spinbox.get())
        window.destroy()

    option = ("Horror", "Classic")
    # spinbox = tk.Spinbox(window, from_=0, to=10, increment=2, font=('Helvetica', 20))
    spinbox = tk.Spinbox(window, values=option, font=('Helvetica', 20))
    spinbox.pack()

    label = tk.Label(window, text="Select")
    label.pack()

    btn1 = tk.Button(window, text='Submit', command=submit)
    btn1.pack(side='bottom')

    tk.Button(window, text="Quit", command=window.destroy).pack()
    window.mainloop()
    return ans[0]

def runner_questions() -> Dict:
    """
    Returns the input that was chosen by the user.
    """
    selected1 = []
    selected2 = []
    selected3 = []
    selected4 = []
    window = tk.Tk()
    frame1 = tk.LabelFrame(window, text="Movies", padx=15, pady=15)
    frame1.grid(row=0, column=0)
    listbox1 = tk.Listbox(frame1, height=5, selectmode='SINGLE')
    window.geometry("600x600")
    listbox1.insert(1, "Horror")
    listbox1.insert(2, "Classic")
    listbox1.insert(3, "Adventure")
    listbox1.insert(4, "Biography")
    listbox1.insert(5, "Animation")

    def submit1() -> None:
        """Collect user input and destroy the frame."""
        selected1.append(listbox1.curselection()[0])
        frame1.destroy()

    btn1 = tk.Button(frame1, text='Submit', command=submit1)
    btn1.pack(side='bottom')
    listbox1.pack()

    frame2 = tk.LabelFrame(window, text="Duration", padx=15, pady=15)
    frame2.grid(row=0, column=1)
    listbox2 = tk.Listbox(frame2, height=5, selectmode='SINGLE')
    listbox2.insert(1, "Short(<60 min)")
    listbox2.insert(2, "Medium (60-180 min)")
    listbox2.insert(3, "Long (>180 min)")

    def submit2() -> None:
        """Collect user input."""
        selected2.append(listbox2.curselection()[0])
        frame2.destroy()

    btn2 = tk.Button(frame2, text='Submit', command=submit2)
    btn2.pack(side='bottom')
    listbox2.pack()

    frame3 = tk.LabelFrame(window, text="Year", padx=15, pady=15)
    frame3.grid(row=1, column=0)
    decades = create_decade_options()
    listbox3 = tk.Listbox(frame3, height=len(decades), selectmode='SINGLE')
    for i in range(1, len(decades) + 1):
        listbox3.insert(i, decades[i - 1])

    def submit3() -> None:
        """Collect user input."""
        selected3.append(listbox3.curselection()[0])
        frame3.destroy()

    btn3 = tk.Button(frame3, text='Submit', command=submit3)
    btn3.pack(side='bottom')
    listbox3.pack()

    frame4 = tk.LabelFrame(window, text="Language", padx=15, pady=15)
    frame4.grid(row=1, column=1)
    listbox4 = tk.Listbox(frame4, height=5, selectmode='SINGLE')
    listbox4.insert(1, "Short(<60 min)")
    listbox4.insert(2, "Medium (60-180 min)")
    listbox4.insert(3, "Long (>180 min)")

    def submit4() -> None:
        """Collect user input."""
        selected4.append(listbox4.curselection()[0])
        frame4.destroy()

    btn4 = tk.Button(frame4, text='Submit', command=submit4)
    btn4.pack(side='bottom')
    listbox4.pack()

    window.mainloop()
    return {'genre': selected1, 'duration': selected2, 'year': selected3, 'language': selected4}


def runner_rankings() -> list:
    """Return the a list of rankings that the user chooses."""
    selected = []
    window = tk.Tk()
    listbox = tk.Listbox(window, height=5, selectmode='SINGLE')
    window.geometry("300x250")
    tk.Label(window, text="Ranking")
    listbox.insert(1, "Genre")
    listbox.insert(2, "Year")
    listbox.insert(3, "Duration")
    listbox.insert(4, "Release Year")
    listbox.insert(5, "Language")

    def submit() -> None:
        """Collect user selection and delete the option from listbox."""
        selected.append(listbox.curselection()[0])
        listbox.delete(listbox.curselection()[0])

    def finish() -> None:
        """Close the window."""
        window.destroy()

    btn1 = tk.Button(window, text='Submit', command=submit)
    btn2 = tk.Button(window, text='QUIT', command=finish)
    btn1.pack(side='bottom')
    btn2.pack()
    listbox.pack()
    window.mainloop()
    return selected


def main_runner() -> tuple:
    """Run the user interface functions."""
    a = runner_questions()
    b = runner_rankings()
    return (a, b)


def create_decade_options() -> list:
    """Return a tuple of decades."""
    decades = []
    for i in range(1960, 2020, 10):
        decades.append(f'{i}' + '-' + f'{i + 10}')

    return decades

