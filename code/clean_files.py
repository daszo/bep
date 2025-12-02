import sqlite3
import pandas as pd
import re


def remove_legal_disclaimer(text: str) -> str:
    """
    Removes the specific legal disclaimer from a text string.
    Uses regex to handle varying whitespace (newlines, spaces) between words.
    """

    # The specific text to remove
    disclaimer_text = """This e-mail message may contain legally privileged and/or confidential
    information. If you are not the intended recipient(s), or the employee
    or agent responsible for delivery of this message to the intended
    recipient(s), you are hereby notified that any dissemination,
    distribution or copying of this e-mail message is strictly prohibited.
    If you have received this message in error, please immediately notify
    the sender and delete this e-mail message from your computer."""

    # 1. Split disclaimer into individual words
    # 2. Escape regex special chars (like parens in 'recipient(s)')
    # 3. Join with \s+ to match any sequence of whitespace (space, tab, newline)
    pattern_parts = [re.escape(word) for word in disclaimer_text.split()]
    regex_pattern = r"\s*".join(pattern_parts)

    # Compile pattern with IGNORECASE to catch capitalization variations
    # The pattern matches the sequence of words regardless of how they are wrapped
    compiled_pattern = re.compile(regex_pattern, re.IGNORECASE)

    # Replace found instances with an empty string
    cleaned_text = compiled_pattern.sub("", text)

    return cleaned_text.strip()


def clean_email_body(text):
    """
    Cleans email body by removing replies, headers, and specific legal disclaimers.
    """
    if pd.isna(text) or not isinstance(text, str):
        return ""

    text = remove_legal_disclaimer(text)
    # 1. Remove the Enron Disclaimer Block
    # Matches a block starting and ending with 10+ asterisks
    text = re.sub(r"\*{10,}[\s\S]*?\*{10,}", "", text)

    # 2. Remove "Original Message" separator lines
    # Replaces the separator with an empty string instead of splitting the text
    text = re.sub(r"-+\s*Original\s*Message\s*-+", "", text, flags=re.IGNORECASE)

    # 3. Remove Quoted text markers (>)
    # Only remove the '>' characters and leading whitespace, preserving the text content
    text = re.sub(r"^[\s>]+", "", text, flags=re.MULTILINE)

    # 4. Remove Header lines (From, Sent, To, Subject)
    # Replaces individual header lines with empty strings.
    # We do this after removing '>' so we catch headers that were inside quotes.
    # Uses MULTILINE to match the start of lines.
    header_pattern = r"^\s*(?:From|Sent|To|Cc|Subject):\s+.*$"
    text = re.sub(header_pattern, "", text, flags=re.MULTILINE | re.IGNORECASE)

    # 5. Clean up extra whitespace created by removals
    # Collapse multiple newlines into two
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def main():
    DB_PATH = "enron.db"

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    sql_query = "SELECT * FROM Message"

    df = pd.read_sql_query(sql_query, conn)

    conn.commit()
    conn.close()

    print(f"loaded database {DB_PATH}")

    # Apply cleaning
    df["body_clean"] = df["body"].apply(clean_email_body)
    df = df[df["body_clean"].str.strip() != ""]

    print(f"Cleaned database {DB_PATH} of shape {df.shape}")

    # 100x faster
    df["clean_length_character"] = df["body_clean"].str.len()
    df["clean_length_word"] = df["body_clean"].str.split().str.len()

    conn = sqlite3.connect(DB_PATH)

    # Write to new table 'similarities'
    # if_exists='replace' drops the table if it exists and creates a new one
    # if_exists='append' adds to it
    df.to_sql(
        name="Message",
        con=conn,
        if_exists="replace",
        index=False,
        chunksize=10000,  # Write in batches to save memory
    )

    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sim_mid ON Message (mid)")
    conn.commit()

    conn.close()

    print("written table Message back to {DB_PATH}")


if __name__ == "__main__":
    main()

