from utils.database import load_db


def main():

    experiments = True

    if experiments == True:
        table = "N10k_text_rank"
    else:
        table = "N100k_text_rank"

    df = load_db(table)

    df.set_index("mid", inplace=True)

    # Clean the text: Replace newlines/tabs with spaces to prevent breaking the TSV structure
    df["body_clean_and_subject"] = (
        f"subject: {df["subject"]} body: {df["body_clean"].astype(str).str.replace(r"[\n\r\t]", " ", regex=True)}"
    )

    df["body_clean_and_subject"].to_csv(
        "data/N10k_text_rank_and_subject_msmarco.tsv", sep="\t", header=False
    )


if __name__ == "__main__":
    main()
