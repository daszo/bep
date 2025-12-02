from utils.database import load_db


def main():

    experiments = True

    if experiments == True:
        table = "N10k_text_rank"
    else:
        table = "N100k_text_rank"

    df = load_db(table)

    df[["mid", "body_clean"]].to_csv("data/N10k_text_rank.tsv", sep="\t")
