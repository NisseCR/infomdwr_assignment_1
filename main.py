from typing import Callable

import pandas as pd
import sqlite3


def create_connection(db_file: str) -> sqlite3.Connection | None:
    """
    Create a database connection to the SQLite database specified by the db_file.

    :param db_file: Database file
    :return: Connection object or None
    """
    try:
        return sqlite3.connect(db_file)
    except Exception as e:
        print(e)
        return None


def read_customer(connection: sqlite3.Connection) -> pd.DataFrame:
    """
    Use the built-in `read_sql` function to read data from the `customer` table and cast the object to a dataframe.
    The `customer_id` attribute is set as the Dataframe index.

    :param connection: Database connection
    :return: DataFrame containing the customer data
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
    """
    Calculate the Jaccard similarity score over a pair of Dataframe records.

    :param r1: first record in pair
    :param r2: second record in pair
    :return: Similarity score
    """
    s1 = set(r1)
    s2 = set(r2)

    try:
        return len(s1.intersection(s2)) / len(s1.union(s2))
    except ZeroDivisionError:
        return 0


def pairwise_similarity(sim: Callable[[pd.Series, pd.Series], float], df: pd.DataFrame) -> pd.DataFrame:
    """
    Using the given similarity function, retrieve the pair-wise similarity score between records. This implementation
    can use any similarity function and is data-agnostic. The algorithm also avoids duplicate and identity comparisons.

    :param sim: Similarity function (e.g. Jaccard similarity)
    :param df: Dataframe containing the records
    :return: Dataframe with pairwise record similarities
    """

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
    # Establish database connection.
    connection = create_connection("data/assignment_1.sqlite")
    if connection is None:
        return

    # Retrieve the customer data.
    df = read_customer(connection)
    print(df)

    # Calculate pair-wise similarity score between customer records.
    sim_df = pairwise_similarity(jaccard_similarity, df)
    print(sim_df)

    print("\nSimilarity scores > 0.7")
    print(sim_df[sim_df["similarity_score"] >= 0.7])


if __name__ == '__main__':
    main()
