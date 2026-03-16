from pathlib import Path

import pandas as pd

from bacon.database import (
    add_actor,
    add_actor_in_movie,
    add_movie,
    initialize_connection,
)

conn = initialize_connection()

datasets_path = Path(__file__).parent / "IMDB_dataset"


def import_actors_to_db():
    database_path = datasets_path / "name.basics.tsv"
    df = pd.read_csv(database_path, sep="\t", nrows=1000)
    for _, actor_info in df.iterrows():
        if "actor" in actor_info["primaryProfession"]:
            print("adding actor: ", actor_info["nconst"][2:], actor_info["primaryName"])
            add_actor(int(actor_info["nconst"][2:]), actor_info["primaryName"], conn)


def import_movies_to_db():
    database_path = datasets_path / "title.basics.tsv"
    df = pd.read_csv(database_path, sep="\t", nrows=1000)
    for _, movie_info in df.iterrows():
        if movie_info["titleType"] == "movie":
            print("adding movie: ", movie_info["tconst"][2:], movie_info["primaryTitle"])
            add_movie(int(movie_info["tconst"][2:]), movie_info["primaryTitle"], conn)


def import_actors_in_movies():
    database_path = datasets_path / "title.principals.tsv"
    df = pd.read_csv(database_path, sep="\t", nrows=1000)
    for _, info in df.iterrows():
        if info["category"] == "actor":
            print("adding relation: ", info["tconst"][2:], info["nconst"])
            add_actor_in_movie(int(info["nconst"][2:]), int(info["tconst"][2:]), conn)


def import_imdb_data():
    import_actors_to_db()
    import_movies_to_db()
    import_actors_in_movies()
