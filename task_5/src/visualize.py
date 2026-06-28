import os
import pandas as pd
import matplotlib.pyplot as plt


def load_cleaned_data(file_path: str) -> pd.DataFrame:
    """
    Load the cleaned dataset produced in Task 4.
    """
    return pd.read_csv(file_path)


def plot_domain_average_score(df: pd.DataFrame, output_path: str) -> None:
    """
    Generate a bar chart showing average score by domain.
    """

    avg_scores = df.groupby("domain")["score"].mean()

    plt.figure(figsize=(6, 4))
    plt.bar(avg_scores.index, avg_scores.values)
    plt.title("Average Score by Domain")
    plt.xlabel("Domain")
    plt.ylabel("Average Score")
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()


def plot_attendance_vs_score(df: pd.DataFrame, output_path: str) -> None:
    """
    Generate a scatter plot showing attendance vs score.
    """

    plt.figure(figsize=(6, 4))

    plt.scatter(
        df["attendance_percent"],
        df["score"]
    )

    plt.title("Attendance vs Score")
    plt.xlabel("Attendance (%)")
    plt.ylabel("Score")

    plt.tight_layout()

    plt.savefig(output_path)

    plt.close()


def plot_submission_status_count(df: pd.DataFrame, output_path: str) -> None:
    """
    Generate a bar chart showing submitted vs not submitted.
    """

    counts = df["submitted"].value_counts()

    plt.figure(figsize=(6, 4))

    plt.bar(
        counts.index,
        counts.values
    )

    plt.title("Submission Status Count")
    plt.xlabel("Submission Status")
    plt.ylabel("Number of Students")

    plt.tight_layout()

    plt.savefig(output_path)

    plt.close()


def write_plot_summary(output_path: str) -> None:
    """
    Generate a short markdown summary describing the plots.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    summary = """# Plot Summary

## Domain Average Score

The bar chart compares the average score obtained by students in each domain.
It helps identify which domain has the highest and lowest average performance.

---

## Attendance vs Score

The scatter plot visualizes the relationship between attendance percentage and score.
It helps observe whether higher attendance is associated with better academic performance.

---

## Submission Status Count

The bar chart shows the number of students who submitted and did not submit the task.
It provides a quick overview of overall submission participation.
"""

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(summary)