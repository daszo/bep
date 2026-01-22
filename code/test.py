import pandas as pd
import os
import io
import re
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "../../snellius-code"))

from CE.utils.database import load_db


def clean_for_latex_macro(text):
    """Converts strings into CamelCase for LaTeX command names."""
    text = text.replace("1.0", "OneZero").replace("1.2", "OneTwo")
    text = re.sub(r"[^a-zA-Z0-9]", " ", text).title().replace(" ", "")
    return text


def get_tabular_latex(pivot_df, dataset_order):
    """
    Returns the raw LaTeX string for the tabular environment (content only).
    """
    metrics_order = ["mrr_3", "mrr_20", "hits_1", "hits_10"]
    final_columns = []

    # Filter columns to ensure we only include what exists in the dataframe
    for dataset in dataset_order:
        for metric in metrics_order:
            if (metric, dataset) in pivot_df.columns:
                final_columns.append((metric, dataset))

    sub_df = pivot_df[final_columns].copy()
    if sub_df.empty:
        return ""

    latex = []
    latex.append(r"\resizebox{\textwidth}{!}{%")
    col_def = "l" + "c" * len(sub_df.columns)
    latex.append(f"\\begin{{tabular}}{{{col_def}}}")
    latex.append(r"\toprule")

    # -- Header Row 1 --
    header_row_1 = [""]
    current_dataset = None
    colspan = 0
    dataset_headers = []

    for col in sub_df.columns:
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
    if current_dataset:
        dataset_headers.append(
            f"\\multicolumn{{{colspan}}}{{c}}{{\\textbf{{{current_dataset.upper()}}}}}"
        )

    latex.append(" & ".join(header_row_1 + dataset_headers) + r" \\")

    # -- CMidrules --
    cmidrules = []
    start_idx = 2
    for _ in dataset_headers:
        cols_in_group = 4  # Assumes 4 metrics
        end_idx = start_idx + cols_in_group - 1
        cmidrules.append(f"\\cmidrule(lr){{{start_idx}-{end_idx}}}")
        start_idx = end_idx + 1
    latex.append(" ".join(cmidrules))

    # -- Header Row 2 --
    header_row_2 = ["Methods"]
    for col in sub_df.columns:
        metric = col[0]
        metric_name = metric.replace("_", "@").upper().replace("HITS", "Hits")
        header_row_2.append(metric_name)

    latex.append(" & ".join(header_row_2) + r" \\")
    latex.append(r"\midrule")

    # -- Data Rows --
    for method, row in sub_df.iterrows():
        row_str = [method.replace("_", "\\_")]
        for val in row:
            if pd.isna(val):
                row_str.append("-")
            else:
                # Format differently if the value is very large (likely a ratio) vs small
                if val > 100:
                    row_str.append(f"{val:.1f}")
                else:
                    row_str.append(f"{val:.4f}")
        latex.append(" & ".join(row_str) + r" \\")

    latex.append(r"\bottomrule")
    latex.append(r"\end{tabular}")
    latex.append(r"}")
    return "\n".join(latex)


def write_single_table_file(content, caption, label, filepath):
    latex = []
    latex.append(r"\begin{table*}[t]")
    latex.append(r"\centering")
    latex.append(f"\\caption{{{caption}}}")
    latex.append(f"\\label{{{label}}}")
    latex.append(content)
    latex.append(r"\end{table*}")

    with open(filepath, "w") as f:
        f.write("\n".join(latex))
    print(f"Generated single table: {filepath}")


def write_combined_table_file(contents_list, caption, label, filepath):
    latex = []
    latex.append(r"\begin{table*}[t]")
    latex.append(r"\centering")
    latex.append(f"\\caption{{{caption}}}")
    latex.append(f"\\label{{{label}}}")

    for i, content in enumerate(contents_list):
        if i > 0:
            latex.append(r"\vspace{1em}")
            latex.append(r"\\")
        latex.append(content)

    latex.append(r"\end{table*}")

    with open(filepath, "w") as f:
        f.write("\n".join(latex))
    print(f"Generated combined table: {filepath}")


def write_results(df, output_dir="tbls"):
    df = df.iloc[2:].copy()

    # ---------------------------------------------------------
    # FILTER: Keep only highest version per System/Size/Exp
    # ---------------------------------------------------------
    def parse_version(v_str):
        try:
            parts = v_str.lower().replace("v", "").split(".")
            return tuple(map(int, parts))
        except:
            return (0, 0)

    df["version_tuple"] = df["version"].apply(parse_version)
    df = df.sort_values(
        by=["system", "size", "experiment_type", "version_tuple"],
        ascending=[True, True, True, True],
    )
    df = df.drop_duplicates(subset=["system", "size", "experiment_type"], keep="last")
    df = df.drop(columns=["version_tuple"])

    os.makedirs(output_dir, exist_ok=True)

    # ---------------------------------------------------------
    # GENERATE VARIABLES
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # PREPARE MAIN RESULTS PIVOT
    # ---------------------------------------------------------
    df["dataset_label"] = df["size"] + " " + df["experiment_type"].str.replace("_", " ")

    def format_method_no_version(row):
        return row["system"].replace("-base", "")

    df["method_label"] = df.apply(format_method_no_version, axis=1)

    pivot_df = df.pivot(
        index="method_label",
        columns="dataset_label",
        values=["mrr_3", "mrr_20", "hits_1", "hits_10"],
    )

    # Table 1 Content (Main Results)
    order_1 = ["10k thread same mid", "10k no thread"]
    tabular_1 = get_tabular_latex(pivot_df, order_1)

    # Table 2 Content (Main Results)
    order_2 = ["10k thread", "100k thread"]
    tabular_2 = get_tabular_latex(pivot_df, order_2)

    # Write Combined File for Main Results
    write_combined_table_file(
        [tabular_1, tabular_2],
        "Comprehensive Results: (Top) Thread settings comparison; (Bottom) Scale comparison.",
        "tab:combined_results",
        os.path.join(output_dir, "table_combined.tex"),
    )

# ---------------------------------------------------------
    # CALCULATE RATIOS (DSI / BM25)
    # ---------------------------------------------------------
    # We split into BM25 and DSI subsets
    bm25_df = df[df["system"].str.contains("BM25")].copy()
    dsi_df = df[df["system"].str.contains("DSI")].copy()

    # Merge on shared configuration keys to align pairs
    merged_df = pd.merge(
        bm25_df, dsi_df, on="dataset_label", suffixes=("_bm25", "_dsi")
    )

    # Calculate ratios
    metrics = ["mrr_3", "mrr_20", "hits_1", "hits_10"]
    ratio_rows = []

    for _, row in merged_df.iterrows():
        new_row = {
            "method_label": "Ratio (DSI / BM25)", # Updated label
            "dataset_label": row["dataset_label"],
        }
        for m in metrics:
            val_bm25 = row[f"{m}_bm25"]
            val_dsi = row[f"{m}_dsi"]
            
            # Prevent division by zero
            if val_bm25 and val_bm25 != 0:
                new_row[m] = val_dsi / val_bm25 # CORRECT: DSI divided by BM25
            else:
                new_row[m] = 0.0
        ratio_rows.append(new_row)

    ratio_df = pd.DataFrame(ratio_rows)

    if not ratio_df.empty:
        # Pivot the ratio dataframe for LaTeX formatting
        pivot_ratio = ratio_df.pivot(
            index="method_label", columns="dataset_label", values=metrics
        )

        all_ratio_datasets = sorted(ratio_df["dataset_label"].unique())

        tabular_ratio = get_tabular_latex(pivot_ratio, all_ratio_datasets)

        write_single_table_file(
            tabular_ratio,
            "Ratio of DSI scores to BM25 scores.", # Updated Caption
            "tab:ratio_results",
            os.path.join(output_dir, "table_ratios.tex"),
        )


if __name__ == "__main__":
    data = """
    BM25-base|10k|base|v1.0|0.9209|0.9262|0.9058|0.966
    DSI-base|10k|base|v1.0|0.0031|0.0047|0.0021|0.012
    BM25-base|10k|no_thread|v1.0|0.8522|0.8607|0.8262|0.9248
    DSI-base|10k|no_thread|v1.0|0.0998|0.1172|0.0716|0.2296
    DSI-base|10k|no_thread|v1.2|0.1500|0.1600|0.1000|0.3000
    BM25-base|10k|thread|v1.0|0.4498|0.4503|0.4404|0.4618
    BM25-base|100k|thread|v1.0|0.4178|0.4233|0.3807|0.4859
    DSI-base|10k|thread|v1.0|0.0439|0.0507|0.0326|0.0954
    DSI-base|100k|thread|v1.0|0.0308|0.0342|0.025|0.0546
    DSI-base|10k|thread_same_mid|v1.0|0.0884|0.1086|0.0639|0.2234
    BM25-base|10k|thread_same_mid|v1.0|0.8403|0.8498|0.8124|0.9202
    """

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
    # df = pd.read_csv(io.StringIO(data.strip()), sep="|", names=cols, header=None)

    df = load_db("experiment_results")

    write_results(df)
