from typing import List, Dict
import json
import os


def read_csv_manual(file_path: str) -> List[Dict]:
    """
    Reads a CSV file manually without using csv or pandas.
    Returns a list of dictionaries.
    """

    rows = []

    with open(file_path, "r", encoding="utf-8") as file:

        lines = file.readlines()

        if not lines:
            return rows

        header = lines[0].strip().split(",")

        for line in lines[1:]:

            line = line.strip()

            if line == "":
                continue

            values = line.split(",")

            if len(values) != len(header):
                continue

            row = {}

            for i in range(len(header)):
                row[header[i]] = values[i]

            rows.append(row)

    return rows


def convert_types(rows: List[Dict]) -> List[Dict]:
    """
    Converts score to int
    Normalizes submitted values.
    """

    converted = []

    for row in rows:

        new_row = row.copy()

        try:
            new_row["score"] = int(new_row["score"])
        except:
            new_row["score"] = 0

        submitted = new_row["submitted"].strip().lower()

        if submitted in ["yes", "y", "true"]:
            new_row["submitted"] = "yes"
        else:
            new_row["submitted"] = "no"

        converted.append(new_row)

    return converted


def calculate_summary(rows: List[Dict]) -> Dict:

    total_students = len(rows)

    submitted_rows = []

    missing_students = []

    domain_scores = {}

    total_score = 0

    below_five = []

    highest = None

    lowest = None

    for row in rows:

        if row["submitted"] == "yes":

            submitted_rows.append(row)

            total_score += row["score"]

            if highest is None or row["score"] > highest["score"]:
                highest = row

            if lowest is None or row["score"] < lowest["score"]:
                lowest = row

            domain = row["domain"]

            if domain not in domain_scores:
                domain_scores[domain] = []

            domain_scores[domain].append(row["score"])

            if row["score"] < 5:
                below_five.append(row["name"])

        else:
            missing_students.append(row["name"])

    average = 0

    if submitted_rows:
        average = round(total_score / len(submitted_rows), 2)

    domain_average = {}

    for domain in domain_scores:
        scores = domain_scores[domain]
        domain_average[domain] = round(sum(scores) / len(scores), 2)

    summary = {

        "total_students": total_students,

        "submitted_students": len(submitted_rows),

        "missing_submissions": len(missing_students),

        "average_score": average,

        "highest_scorer": highest["name"] if highest else None,

        "lowest_scorer": lowest["name"] if lowest else None,

        "domain_wise_average": domain_average,

        "students_not_submitted": missing_students,

        "students_below_5": below_five

    }

    return summary


def write_json(data: Dict, output_path: str) -> None:

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:

        json.dump(data, file, indent=4)