import json
import os
import sys

from clean_data import (
    load_data,
    generate_summary,
    remove_duplicates,
    standardize_domains,
    clean_attendance,
    clean_scores,
    clean_study_hours,
    clean_height,
    clean_weight,
    clean_submitted,
    handle_missing_values,
    save_cleaned_data,
    write_report,
)

from validate_data import validate_cleaned_data


def save_json(data: dict, output_path: str) -> None:
    """
    Save dictionary as a JSON file.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def main():

    if len(sys.argv) != 3:

        print("Usage:")
        print(
            "python task_4/src/main.py "
            "task_4/data/messy_students.csv "
            "task_4/output/cleaned_students.csv"
        )

        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # -------------------------
    # Load Data
    # -------------------------

    df = load_data(input_file)

    summary_before = generate_summary(df)

    # -------------------------
    # Cleaning Pipeline
    # -------------------------

    df = remove_duplicates(df)

    df = standardize_domains(df)

    df = clean_attendance(df)

    df = clean_scores(df)

    df = clean_study_hours(df)

    df = clean_height(df)

    df = clean_weight(df)

    df = clean_submitted(df)

    df = handle_missing_values(df)

    df = df.reset_index(drop=True)

    # -------------------------
    # Summary After Cleaning
    # -------------------------

    summary_after = generate_summary(df)

    # -------------------------
    # Validation
    # -------------------------

    if not validate_cleaned_data(df):

        print("Validation failed.")

        return

    # -------------------------
    # Save Outputs
    # -------------------------

    df = df[
        [
        "student_id",
        "name",
        "domain",
        "attendance_percent",
        "score",
        "study_hours",
        "height_cm",
        "weight_kg",
        "submitted",
        ]
    ]

    save_cleaned_data(df, output_file)

    save_json(
        summary_before,
        "task_4/output/summary_before.json",
    )

    save_json(
        summary_after,
        "task_4/output/summary_after.json",
    )

    write_report(
        "task_4/output/cleaning_report.md"
    )

    print("\nTask 4 completed successfully.\n")

    print("Generated Files:")

    print("- cleaned_students.csv")

    print("- summary_before.json")

    print("- summary_after.json")

    print("- cleaning_report.md")


if __name__ == "__main__":
    main()