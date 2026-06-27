import pandas as pd


def validate_cleaned_data(df: pd.DataFrame) -> bool:
    """
    Validate the cleaned dataset according to the Task 4 requirements.

    Returns:
        True if all validation checks pass.
        False otherwise.
    """

    # 1. student_id must be unique
    if df["student_id"].duplicated().any():
        print("Validation Failed: Duplicate student IDs found.")
        return False

    # 2. attendance_percent must be numeric
    if not pd.api.types.is_numeric_dtype(df["attendance_percent"]):
        print("Validation Failed: attendance_percent is not numeric.")
        return False

    # 3. attendance_percent must be between 0 and 100
    if not df["attendance_percent"].between(0, 100).all():
        print("Validation Failed: Invalid attendance values found.")
        return False

    # 4. score must be numeric
    if not pd.api.types.is_numeric_dtype(df["score"]):
        print("Validation Failed: score is not numeric.")
        return False

    # 5. study_hours must be numeric
    if not pd.api.types.is_numeric_dtype(df["study_hours"]):
        print("Validation Failed: study_hours is not numeric.")
        return False

    # 6. height_cm must be numeric
    if not pd.api.types.is_numeric_dtype(df["height_cm"]):
        print("Validation Failed: height_cm is not numeric.")
        return False

    # 7. weight_kg must be numeric
    if not pd.api.types.is_numeric_dtype(df["weight_kg"]):
        print("Validation Failed: weight_kg is not numeric.")
        return False

    # 8. submitted values
    allowed_submission = {"yes", "no"}

    if not set(df["submitted"]).issubset(allowed_submission):
        print("Validation Failed: Invalid submitted values.")
        return False

    # 9. domain values
    allowed_domains = {
        "ML",
        "Web",
        "Electronics",
        "Mechanical",
    }

    if not set(df["domain"]).issubset(allowed_domains):
        print("Validation Failed: Invalid domain values.")
        return False

    # 10. Critical columns must not contain missing values
    critical_columns = [
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

    if df[critical_columns].isnull().any().any():
        print("Validation Failed: Missing values remain.")
        return False

    print("Validation Successful.")

    return True