from typing import Callable

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


def read_customer(connection: sqlite3.Connection) -> pd.DataFrame:
    """

    :param connection:
    :return:
    """
    query = """
    select
        *
    from customer
    """

    # Use 'customer_id' as index column, to prevent calculating the similarity over this attribute.
    df = pd.read_sql(query, con=connection, index_col='customer_id')
    return df


def jaccard_similarity(r1: pd.Series, r2: pd.Series) -> float:
    s1 = set(r1)
    s2 = set(r2)
    return len(s1.intersection(s2)) / len(s1.union(s2))


def pairwise_similarity(sim: Callable[[pd.Series, pd.Series], float], df: pd.DataFrame) -> pd.DataFrame:
    data = []
    for i, r1 in df.iterrows():
        for j, r2 in df.iterrows():
            if j <= i:
                continue

            similarity_score = sim(r1, r2)
            data.append([i, j, r1["first_name"], r2["first_name"], similarity_score])

    return pd.DataFrame(
        data,
        columns=["customer_id_x", "customer_id_y", "first_name_x", "first_name_y", "similarity_score"]
    )



def main():
    connection = create_connection("data/assignment_1.sqlite")
    df = read_customer(connection)
    print(df)

    sim_df = pairwise_similarity(jaccard_similarity, df)
    print(sim_df)

    # Similarities higher than 0.7
    print("\nSimilarity scores > 0.7")
    print(sim_df[sim_df["similarity_score"] >= 0.7])


if __name__ == '__main__':
    main()
