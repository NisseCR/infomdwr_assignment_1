import pandas as pd
import sqlite3

from source.setup import create_connection


def read_customer(connection: sqlite3.Connection) -> pd.DataFrame:
    query = """
    select *
    from customer
    """

    df = pd.read_sql(query, con=connection)
    return df


def jaccard(r1: pd.Series, r2: pd.Series) -> float:
    s1 = set(r1)
    s2 = set(r2)
    return len(s1.intersection(s2)) / len(s1.union(s2))


def cross_join_customer(df: pd.DataFrame) -> pd.DataFrame:
    df_temp = df.copy()
    df_temp["key"] = 1
    df_temp = pd.merge(left=df_temp, right=df_temp, on="key", how="outer")
    df_temp = df_temp.drop(columns="key")
    return df_temp


def main():
    connection = create_connection("data/assignment_1.sqlite")
    df = read_customer(connection)
    cross_df = cross_join_customer(df)
    print(df)
    print(cross_df)
