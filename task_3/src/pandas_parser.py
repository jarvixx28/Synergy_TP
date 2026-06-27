import os
import json
import pandas as pd


def read_csv_pandas(file_path: str):
    """
    Reads the CSV file using pandas.
    """
    df = pd.read_csv(file_path)

    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)

    df["submitted"] = (
        df["submitted"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace({"y": "yes", "true": "yes"})
    )

    df.loc[~df["submitted"].isin(["yes"]), "submitted"] = "no"

    return df


def calculate_summary_pandas(df) -> dict:
    submitted = df[df["submitted"] == "yes"]
    missing = df[df["submitted"] == "no"]

    domain_average = (
        submitted.groupby("domain")["score"]
        .mean()
        .round(2)
        .to_dict()
    )

    summary = {
        "total_students": len(df),
        "submitted_students": len(submitted),
        "missing_submissions": len(missing),
        "average_score": round(submitted["score"].mean(), 2),
        "highest_scorer": submitted.loc[
            submitted["score"].idxmax(), "name"
        ],
        "lowest_scorer": submitted.loc[
            submitted["score"].idxmin(), "name"
        ],
        "domain_wise_average": domain_average,
        "students_not_submitted": missing["name"].tolist(),
        "students_below_5": submitted.loc[
            submitted["score"] < 5, "name"
        ].tolist(),
    }

    return summary


def write_json(data: dict, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)