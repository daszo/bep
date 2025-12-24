from utils.database import load_db, write_to_db


def main():

    experiments = True

    if experiments == True:
        sql_table_name = "N10k_text_rank"
    else:
        sql_table_name = "N100k_text_rank"

    df = load_db(sql_table_name)

    # df.set_index("mid", inplace=True)

    df_table_name = "body_clean_and_subject"
    # 1. Clean the body column first (Vectorized)
    cleaned_body = (
        df["body_clean"].astype(str).str.replace(r"[\n\r\t]", " ", regex=True)
    )

    # 2. Concatenate strings element-wise (Vectorized)
    df[df_table_name] = (
        "subject: " + df["subject"].astype(str) + " body: " + cleaned_body
    )

    new_sql_table_name = sql_table_name + "_and_subject"

    write_to_db(df, new_sql_table_name)


if __name__ == "__main__":
    main()
