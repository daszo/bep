from database import write_to_db
import pandas as pd
from typing import Optional


def tsv_to_db(
    name: str = "data/N10k_text_rank_and_subject_msmarco.tsv",
    table_name: Optional[str] = None,
):

    if table_name is None:
        table_name = "_".join(name.split("/")[-1].split("_")[:-1])
        print(f"Table name has become{table_name}")

    df = pd.read_csv(name, sep="\t")

    write_to_db(df, table_name)


if __name__ == "__main__":
    tsv_to_db()
