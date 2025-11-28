import argparse
import os
import time


def main():
    # 1. Setup Argument Parsing
    parser = argparse.ArgumentParser(
        description="Test remote execution with arguments."
    )
    parser.add_argument("--name", type=str, required=True, help="Your name")
    parser.add_argument(
        "--count", type=int, default=1, help="Number of times to repeat"
    )
    parser.add_argument(
        "--sleep", type=int, default=0, help="Simulate long running process (seconds)"
    )

    args = parser.parse_args()

    # 2. Simulate work (useful to test connection stability)
    if args.sleep > 0:
        print(f"Simulating heavy task for {args.sleep} seconds...")
        time.sleep(args.sleep)

    # 3. Ensure output directory exists (Critical for the rsync script)
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "test.txt")

    # 4. Write to file
    with open(file_path, "w") as f:
        for i in range(args.count):
            line = f"Row {i+1}: Hello {args.name}, this was generated on the remote machine.\n"
            f.write(line)
            print(f"Processing... {i+1}/{args.count}")

    print(f"\n[Success] File saved to {file_path}")


if __name__ == "__main__":
    main()
