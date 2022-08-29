def reset_scheme_tables(conn) -> None:

    delete_tables = """
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
    """

    with conn.cursor() as cursor:
        cursor.execute(delete_tables)
        conn.commit()


def create_tables(conn) -> None:

    interests = """
        CREATE TABLE IF NOT EXISTS interests (
        ID SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL UNIQUE
        );
    """

    person = """
        CREATE TABLE IF NOT EXISTS person (
        ID SERIAL PRIMARY KEY,
        vk_id INT NOT NULL UNIQUE,
        name VARCHAR NOT NULL,
        city INT NOT NULL,
        bdate INT NOT NULL,
        sex INT NOT NULL
        );
    """

    user_favorite = """
        CREATE TABLE IF NOT EXISTS user_favorite (
        ID SERIAL PRIMARY KEY,
        personid INT NOT NULL,
        favorite_id INT NOT NULL
        );
    """

    user_viewed = """
        CREATE TABLE IF NOT EXISTS user_viewed (
        ID SERIAL PRIMARY KEY,
        personid INT NOT NULL,
        viewed_id INT NOT NULL
        );
    """

    person_int = """
        CREATE TABLE IF NOT EXISTS person_int (
        ID SERIAL PRIMARY KEY,
        personid INT NOT NULL references person(vk_id),
        intid INT NOT NULL references interests(ID)
        );
    """
    with conn.cursor() as cursor:
        cursor.execute(interests)
        cursor.execute(person)
        cursor.execute(user_favorite)
        cursor.execute(user_viewed)
        cursor.execute(person_int)
        conn.commit()
