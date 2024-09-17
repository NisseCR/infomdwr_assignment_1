import pandas as pd
import sqlite3

from source.setup import create_connection


def read_test(connection: sqlite3.Connection) -> pd.DataFrame:
    query = """
    select
        id,
        name
    from assignment_1_test
    """

    df = pd.read_sql(query, con=connection)
    return df


def main():
    connection = create_connection("data/assignment_1.sqlite")
    df = read_test(connection)
    print(df.head())
