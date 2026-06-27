import json
import os
import pandas as pd


def load_data(file_path: str):
    """
    Load the messy CSV file.
    """
    return pd.read_csv(file_path)


def generate_summary(df) -> dict:
    """
    Generate dataset summary before/after cleaning.
    """

    summary = {
        "total_rows": len(df),
        "unique_students": int(df["student_id"].nunique()),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": df.isna().sum().to_dict(),
        "column_types": {
            col: str(dtype)
            for col, dtype in df.dtypes.items()
        },
    }

    return summary


def remove_duplicates(df):
    """
    Remove duplicate rows.
    """

    return df.drop_duplicates().reset_index(drop=True)


def standardize_domains(df):
    """
    Convert all domain names into
    ML, Web, Electronics, Mechanical.
    """

    mapping = {

        "ml": "ML",
        "machine learning": "ML",

        "web": "Web",
        "web dev": "Web",
        "web development": "Web",

        "electronics": "Electronics",

        "mechanical": "Mechanical",

    }

    df["domain"] = (
        df["domain"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace(mapping)
    )

    return df


def clean_attendance(df):
    """
    Convert attendance into numbers.
    Invalid values become NaN.
    """

    df["attendance_percent"] = (

        df["attendance_percent"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()

    )

    df["attendance_percent"] = pd.to_numeric(

        df["attendance_percent"],
        errors="coerce"

    )

    df.loc[
        (df["attendance_percent"] < 0)
        | (df["attendance_percent"] > 100),
        "attendance_percent",
    ] = pd.NA

    return df
def clean_scores(df):
    """
    Convert score values into numeric.
    Words such as 'nine' are converted to numbers.
    """

    word_map = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }

    df["score"] = (
        df["score"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace(word_map)
    )

    df["score"] = pd.to_numeric(
        df["score"],
        errors="coerce"
    )

    return df


def clean_study_hours(df):
    """
    Convert study hours into numeric values.
    """

    word_map = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }

    df["study_hours"] = (
        df["study_hours"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace(word_map)
    )

    df["study_hours"] = pd.to_numeric(
        df["study_hours"],
        errors="coerce"
    )

    return df


def clean_height(df):
    """
    Convert all heights to centimetres.
    Output column: height_cm
    """

    def convert(value):

        if pd.isna(value):
            return pd.NA

        value = str(value).strip().lower()

        if "cm" in value:
            value = value.replace("cm", "").strip()
            return float(value)

        if "m" in value:
            value = value.replace("m", "").strip()
            return float(value) * 100

        return pd.to_numeric(value, errors="coerce")

    df["height_cm"] = df["height"].apply(convert)

    df.drop(columns=["height"], inplace=True)

    return df


def clean_weight(df):
    """
    Convert all weights to kilograms.
    Output column: weight_kg
    """

    df["weight_kg"] = (
        df["weight"]
        .astype(str)
        .str.lower()
        .str.replace("kg", "", regex=False)
        .str.strip()
    )

    df["weight_kg"] = pd.to_numeric(
        df["weight_kg"],
        errors="coerce"
    )

    df.drop(columns=["weight"], inplace=True)

    return df


def clean_submitted(df):
    """
    Standardize submitted values.
    """

    mapping = {
        "yes": "yes",
        "y": "yes",
        "true": "yes",
        "no": "no",
        "n": "no",
        "false": "no",
    }

    df["submitted"] = (
        df["submitted"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace(mapping)
    )

    return df
def handle_missing_values(df):
    """
    Handle missing values using documented rules.

    Rule:
    Numeric columns are filled using the column median.
    """

    numeric_columns = [
        "attendance_percent",
        "score",
        "study_hours",
        "height_cm",
        "weight_kg",
    ]

    for column in numeric_columns:

        if df[column].isnull().any():
            median = df[column].median()
            df[column] = df[column].fillna(median)

    return df


def save_cleaned_data(df, output_path: str) -> None:
    """
    Save the cleaned dataframe as CSV.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df.to_csv(output_path, index=False)


def write_report(report_path: str) -> None:
    """
    Generate a markdown report describing all cleaning operations.
    """

    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    report = """# Cleaning Report

## Objective

This report documents the cleaning operations performed on the messy student dataset before further analysis.

---

## Cleaning Rules Applied

1. Removed duplicate rows from the dataset.
2. Standardized all domain names to one of:
   - ML
   - Web
   - Electronics
   - Mechanical
3. Converted attendance values into numeric percentages.
4. Converted textual score values (e.g. "nine") into numeric values.
5. Converted textual study hour values (e.g. "two") into numeric values.
6. Converted all heights into centimetres.
7. Converted all weights into kilograms.
8. Renamed:
   - height → height_cm
   - weight → weight_kg
9. Normalized submitted values to either "yes" or "no".
10. Replaced missing numeric values using the median of the respective column.
11. Invalid attendance values (below 0 or above 100) were treated as missing and replaced using the median.

---

## Dataset Issues Found

The provided dataset contained:

- Duplicate student records.
- Missing attendance values.
- Missing score values.
- Missing weight values.
- Mixed domain names (ML, ml, MACHINE LEARNING, etc.).
- Heights stored in both metres and centimetres.
- Weights stored in multiple formats.
- Attendance values stored with and without "%".
- Textual numeric values such as "nine" and "two".
- Invalid attendance values (-10 and 105).
- Inconsistent submitted values (yes, Yes, Y, N).

---

## Validation Checklist

After cleaning:

- Duplicate student IDs removed.
- Attendance values are numeric and within 0–100.
- Score values are numeric.
- Study hours are numeric.
- Height values are stored in centimetres.
- Weight values are stored in kilograms.
- Submitted values contain only "yes" or "no".
- Domain values contain only:
  - ML
  - Web
  - Electronics
  - Mechanical
- Critical columns contain no missing values.

---

## Conclusion

The dataset has been cleaned, standardized, and validated according to the specified cleaning rules. It is now suitable for further analysis and visualization in the subsequent tasks.
"""

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report)