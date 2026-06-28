import os
import sys

from visualize import (
    load_cleaned_data,
    plot_domain_average_score,
    plot_attendance_vs_score,
    plot_submission_status_count,
    write_plot_summary,
)


def main():

    if len(sys.argv) != 3:
        print("Usage:")
        print(
            "python task_5/src/main.py "
            "task_4/output/cleaned_students.csv "
            "task_5/output"
        )
        return

    input_file = sys.argv[1]
    output_folder = sys.argv[2]

    os.makedirs(output_folder, exist_ok=True)

    # Load cleaned dataset
    df = load_cleaned_data(input_file)

    # Generate plots
    plot_domain_average_score(
        df,
        os.path.join(output_folder, "domain_average_score.png"),
    )

    plot_attendance_vs_score(
        df,
        os.path.join(output_folder, "attendance_vs_score.png"),
    )

    plot_submission_status_count(
        df,
        os.path.join(output_folder, "submission_status_count.png"),
    )

    # Generate summary
    write_plot_summary(
        os.path.join(output_folder, "plot_summary.md")
    )

    print("\nTask 5 completed successfully.\n")

    print("Generated files:")
    print("- domain_average_score.png")
    print("- attendance_vs_score.png")
    print("- submission_status_count.png")
    print("- plot_summary.md")


if __name__ == "__main__":
    main()