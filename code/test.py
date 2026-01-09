import json


def main():
    # 1. Setup Argument Parsing

    input_path = "data/test.N10k_text_rank_d2q_q1.docTquery"
    output_path = "data/test_examples.txt"

    key_to_keep = ["text_id", "text"]

    with open(input_path, "r") as fr, open(output_path, "w") as fw:
        for i, line in enumerate(fr, 1):
            line = line.strip()
            if not line:
                continue

            # Parse the individual JSON object on this line
            row = json.loads(line)
            output = {k: row[k] for k in key_to_keep}
            fw.write(json.dumps(output) + "\n")
            if i % 3 == 0:
                fw.write("=" * 20 + "\n")
                fw.write("=" * 20 + "\n")
            else:
                fw.write("-" * 20 + "\n")

    print(f"\n[Success] File saved to {output_path}")


if __name__ == "__main__":
    main()
