import pandas as pd
import sqlite3


def create_connection(db_file) -> sqlite3.Connection | None:
    """
    Create a database connection to the SQLite database specified by the db_file.
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        return sqlite3.connect(db_file)
    except Exception as e:
        print(e)
        return None