import pandas as pd
import os
import io
import re


def clean_for_latex_macro(text):
    """Converts strings into CamelCase for LaTeX command names."""
    # Remove version dots (v1.0 -> vOneZero) or simple replacements
    text = text.replace("1.0", "OneZero").replace("1.2", "OneTwo")
    text = re.sub(r"[^a-zA-Z0-9]", " ", text).title().replace(" ", "")
    return text


def write_results(df, output_dir="tbls"):

    df = df.iloc[2:].copy()

    os.makedirs(output_dir, exist_ok=True)  # Creates folder if it doesn't exist

    latex_vars = []
    for _, row in df.iterrows():
        sys = clean_for_latex_macro(row["system"])
        exp = clean_for_latex_macro(row["experiment_type"])
        ver = clean_for_latex_macro(row["version"])
        sz = clean_for_latex_macro(row["size"])
        for metric in ["mrr_3", "mrr_20", "hits_1", "hits_10"]:
            val = row[metric]
            macro_name = f"\\Res{sys}{exp}{sz}{ver}{clean_for_latex_macro(metric)}"
            latex_vars.append(f"\\newcommand{{{macro_name}}}{{{val}}}")

    with open(os.path.join(output_dir, "variables.tex"), "w") as f:
        f.write("% Auto-generated variables\n")
        f.write("\n".join(latex_vars))

    # ==========================================
    # Task 2: Generate results_table.tex (The Table)
    # ==========================================

    # 1. Create a "Dataset Label" combining Size and Experiment Type
    # This creates headers like "10k Base", "10k Thread", etc.
    df["dataset_label"] = df["size"] + " " + df["experiment_type"].str.replace("_", " ")

    # 2. Create a clean "Method Label" for the rows
    # Clean "BM25-base" -> "BM25" and append version if it's distinct (like v1.2)
    def format_method(row):
        name = row["system"].replace("-base", "")
        if row["version"] != "v1.0":
            return f"{name} ({row['version']})"
        return name

    df["method_label"] = df.apply(format_method, axis=1)

    # 3. Pivot: Rows=Method, Cols=Dataset, Values=Metrics
    pivot_df = df.pivot(
        index="method_label",
        columns="dataset_label",
        values=["mrr_3", "mrr_20", "hits_1", "hits_10"],
    )

    # 4. Sort Columns logically
    # We want 10k before 100k, and maybe Base < No Thread < Thread
    # We define an explicit order list for the dataset labels found in your data
    desired_order = ["10k base", "10k no thread", "10k thread", "100k thread"]

    # Rebuild the columns list in the correct order (Metric, Dataset)
    final_columns = []
    metrics_order = ["mrr_3", "mrr_20", "hits_1", "hits_10"]

    for dataset in desired_order:
        for metric in metrics_order:
            if (metric, dataset) in pivot_df.columns:
                final_columns.append((metric, dataset))

    pivot_df = pivot_df[final_columns]

    # 5. Build LaTeX
    latex = []
    latex.append(r"\begin{table*}[t]")
    latex.append(r"\centering")
    latex.append(
        r"\caption{Main experimental results. Datasets are grouped by size and thread setting.}"
    )
    latex.append(r"\label{tab:main_results}")
    # Resizebox is useful if the table gets too wide
    latex.append(r"\resizebox{\textwidth}{!}{%")
    col_def = "l" + "c" * len(pivot_df.columns)
    latex.append(f"\\begin{{tabular}}{{{col_def}}}")
    latex.append(r"\toprule")

    # -- Header Row 1: Dataset Names --
    header_row_1 = [""]  # Corner cell
    current_dataset = None
    colspan = 0

    dataset_headers = []
    for col in pivot_df.columns:
        metric, dataset = col
        if dataset != current_dataset:
            if current_dataset:
                dataset_headers.append(
                    f"\\multicolumn{{{colspan}}}{{c}}{{\\textbf{{{current_dataset.upper()}}}}}"
                )
            current_dataset = dataset
            colspan = 1
        else:
            colspan += 1
    # Append last group
    dataset_headers.append(
        f"\\multicolumn{{{colspan}}}{{c}}{{\\textbf{{{current_dataset.upper()}}}}}"
    )

    latex.append(" & ".join(header_row_1 + dataset_headers) + r" \\")

    # -- CMidrules (Lines under dataset names) --
    cmidrules = []
    start_idx = 2  # Start after first column
    for _ in dataset_headers:
        cols_in_group = 4  # Assumes 4 metrics per dataset
        end_idx = start_idx + cols_in_group - 1
        cmidrules.append(f"\\cmidrule(lr){{{start_idx}-{end_idx}}}")
        start_idx = end_idx + 1
    latex.append(" ".join(cmidrules))

    # -- Header Row 2: Metrics --
    header_row_2 = ["Methods"]
    for col in pivot_df.columns:
        metric = col[0]
        metric_name = metric.replace("_", "@").upper().replace("HITS", "Hits")
        header_row_2.append(metric_name)

    latex.append(" & ".join(header_row_2) + r" \\")
    latex.append(r"\midrule")

    # -- Data Rows --
    for method, row in pivot_df.iterrows():
        row_str = [method.replace("_", "\\_")]
        for val in row:
            if pd.isna(val):
                row_str.append("-")
            else:
                # Bold the highest numbers? (Optional logic could go here)
                row_str.append(f"{val:.4f}")
        latex.append(" & ".join(row_str) + r" \\")

    latex.append(r"\bottomrule")
    latex.append(r"\end{tabular}")
    latex.append(r"}")  # End resizebox
    latex.append(r"\end{table*}")

    with open(os.path.join(output_dir, "results_table.tex"), "w") as f:
        f.write("\n".join(latex))

    print(f"Done. Files saved to {output_dir}/")


if __name__ == "__main__":

    data = """
    BM25-base|10k|base|v1.0|0.9209|0.9262|0.9058|0.966
    DSI-base|10k|base|v1.0|0.0031|0.0047|0.0021|0.012
    BM25-base|10k|no_thread|v1.0|0.8522|0.8607|0.8262|0.9248
    DSI-base|10k|no_thread|v1.0|0.0998|0.1172|0.0716|0.2296
    DSI-base|10k|no_thread|v1.2|0.0998|0.1172|0.0716|0.2296
    BM25-base|10k|thread|v1.0|0.4498|0.4503|0.4404|0.4618
    BM25-base|100k|thread|v1.0|0.4178|0.4233|0.3807|0.4859
    DSI-base|10k|thread|v1.0|0.0439|0.0507|0.0326|0.0954
    DSI-base|100k|thread|v1.0|0.0308|0.0342|0.025|0.0546
    """

    # Define column names based on your schema
    cols = [
        "system",
        "size",
        "experiment_type",
        "version",
        "mrr_3",
        "mrr_20",
        "hits_1",
        "hits_10",
    ]

    # Read data, skipping the first two rows as requested
    df = pd.read_csv(io.StringIO(data.strip()), sep="|", names=cols, header=None)

    write_results(df)
