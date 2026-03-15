from bacon.database import add_actor, add_actor_in_movie, add_movie, get_actor_name, get_movie_name, initialize_connection, reset_tables


def generate_db() -> None:
    reset_tables()
    conn = initialize_connection()
    add_actor(1, "Ely", conn)
    add_actor(2, "Marik", conn)
    add_movie(1, "Pirates of the Carribiean", conn)
    add_actor_in_movie(1, 1, conn)
    add_actor_in_movie(2, 1, conn)
    print(get_actor_name(1, conn))
    print(get_actor_name(2, conn))
    print(get_movie_name(1, conn))
