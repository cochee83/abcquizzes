"""Program quizzes children on identifying their abc's.

This program outputs a random letter from the alphabet and allows the client
to respond with a 'y' if the child answered correctly.  Score and time results
are persisted in an SQLite database.
"""
import argparse
import sqlite3
import sys
import random
import time

ALPHABET = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    9: 'J',
    10: 'K',
    11: 'L',
    12: 'M',
    13: 'N',
    14: 'O',
    15: 'P',
    16: 'Q',
    17: 'R',
    18: 'S',
    19: 'T',
    20: 'U',
    21: 'V',
    22: 'W',
    23: 'X',
    24: 'Y',
    25: 'Z',
}


def create_connection(path: str) -> sqlite3.Connection:
    """Connect, create and return database connection object.

    Args:
        path:
            Filename path to the database

    Returns:
        Return database connection
    """
    connection = None

    try:
        connection = sqlite3.connect(path)
    except sqlite3.Error as err:
        print(f"The error '{err}' occurred")

    return connection


def execute_query(connection: sqlite3.Connection, query: str) -> None:
    """Execute input query and commit.

    Args:
        conn:
            Database connection object
        query:
            SQL query
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except sqlite3.Error as err:
        print(f"The error '{err}' occurred")


def exec_run(conn, user_id: int, num_of_letters: int, loops: int) -> int:
    """Ask if user correctly answered the random letter and persist results.

    Args:
        user_id:
            User unique identifier
        num_of_letters:
            Number of letters to randomly select
        loops:
            Number of loops to randomly select a letter and ask

    Returns:
        Return code 0 if successful
    """
    count = 0
    tic = time.perf_counter()

    for i in range(loops):
        rand = random.randint(0, num_of_letters-1)
        letter = ALPHABET[rand]

        is_correct = input(f"What letter is this '{letter}'?\n")

        if is_correct.lower() == 'y':
            count += 1

        print("")

    time_in_secs = time.perf_counter()-tic

    print(f"Score: {count}")
    print(f"Time: {time_in_secs:0.4f}")

    execute_query(conn, f"""
        INSERT INTO runs (
            run_date,
            user_id,
            num_of_letters,
            num_of_loops,
            score,
            time
        ) VALUES (
            datetime('now', 'localtime'),
            {user_id},
            {num_of_letters},
            {loops},
            {count},
            {time_in_secs}
        ); """)


def main() -> int:
    """Parse command-line arguments for input to executing the run.

    Returns:
        Return code 0 if successful.
    """
    # Get command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("user_id")
    parser.add_argument("num_of_letters")
    parser.add_argument("--loops")
    args = parser.parse_args()

    user_id = int(args.user_id)
    num_of_letters = int(args.num_of_letters)
    loops = int(args.loops) if args.loops else 10

    # Get database connection
    conn = create_connection("abcquiz_app.sqlite3")

    # Create tables
    execute_query(conn, """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        nationality TEXT
    ); """)

    execute_query(conn, """
    CREATE TABLE IF NOT EXISTS runs(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      run_date TEXT NOT NULL,
      user_id INTEGER NOT NULL,
      num_of_letters INTEGER NOT NULL,
      num_of_loops INTEGER NOT NULL,
      score INTEGER NOT NULL,
      time REAL NOT NULL,
      FOREIGN KEY (user_id) REFERENCES users (id)
    ); """)

    # Todo: check if user_id exists in database

    return exec_run(conn, user_id, num_of_letters, loops)


if __name__ == '__main__':
    RC = main()
    sys.exit(RC)
