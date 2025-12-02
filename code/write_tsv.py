from utils.database import load_db


def main():

    experiments = True

    if experiments == True:
        table = "N10k_text_rank"
    else:
        table = "N100k_text_rank"

    df = load_db(table)

    df[["mid", "body_clean"]].set_index("mid", inplace=True)

    df.to_csv("data/N10k_text_rank.tsv", sep="\t")


if __name__ == "__main__":
    main()
