import os
import sys

from replicate_statistics import (
    load_data,
    calculate_replicate_statistics,
    save_replicate_summary,
)

from correlation_analysis import (
    generate_correlation_summary,
    generate_calibration_summary,
    plot_calibration_curve,
    plot_signal_input_scatter,
    save_summary,
)

from feature_engineering import (
    engineer_features,
    save_dataset,
)

def create_output_directory(output_directory: str) -> None:
    """
    Create output directory if it does not exist.
    """

    os.makedirs(
        output_directory,
        exist_ok=True,
    )

def save_markdown_report(
    file_path: str,
    title: str,
    content: str,
) -> None:
    """
    Save markdown report.
    """

    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(f"# {title}\n\n")

        file.write(content)

def generate_reports(
    output_directory: str,
) -> None:
    """
    Generate markdown reports.
    """

    reports = {

        "replicate_analysis.md": (

            "Replicate Analysis",

            "This report summarizes replicate statistics and "
            "measurement stability for each experimental condition.",

        ),

        "correlation_limitations.md": (

            "Correlation Limitations",

            "Correlation indicates association but does not imply causation. "
            "Experimental conditions and sample size should always be considered.",

        ),

        "feature_dictionary.md": (

            "Feature Dictionary",

            "- normalized_signal\n"
            "- error_percent\n"
            "- power\n"
            "- stress_ratio\n"
            "- rolling_average\n"
            "- ml_ready",

        ),

        "feature_summary.md": (

            "Feature Engineering Summary",

            "Feature engineering generated derived variables to improve "
            "machine learning readiness of the dataset.",

        ),

    }

    for filename, (title, content) in reports.items():

        save_markdown_report(

            os.path.join(output_directory, filename),

            title,

            content,

        )

def main() -> None:
    """
    Execute complete Task 9 pipeline.
    """

    if len(sys.argv) != 3:

        print(
            "Usage:\n"
            "python task_9/src/main.py "
            "task_9/data/calibration_measurements.csv "
            "task_9/output"
        )

        sys.exit(1)

    try:

        input_file = sys.argv[1]

        output_directory = sys.argv[2]

        create_output_directory(output_directory)

        print("Loading dataset...")

        dataframe = load_data(input_file)

        print("Calculating replicate statistics...")

        replicate_summary = calculate_replicate_statistics(
            dataframe
        )

        save_replicate_summary(
            replicate_summary,
            os.path.join(
                output_directory,
                "replicate_summary.csv",
            ),
        )

        print("Performing correlation analysis...")

        correlation_summary = generate_correlation_summary(
            dataframe
        )

        calibration_summary = generate_calibration_summary(
            correlation_summary
        )

        save_summary(
            correlation_summary,
            os.path.join(
                output_directory,
                "correlation_summary.csv",
            ),
        )

        save_summary(
            calibration_summary,
            os.path.join(
                output_directory,
                "calibration_summary.csv",
            ),
        )

        print("Generating engineered features...")

        engineered = engineer_features(dataframe)

        save_dataset(
            engineered,
            os.path.join(
                output_directory,
                "engineered_features.csv",
            ),
        )

        save_dataset(
            engineered,
            os.path.join(
                output_directory,
                "ml_ready_dataset.csv",
            ),
        )

        print("Creating plots...")

        for domain in [
            "Biochem",
            "Electronics",
            "Mechanical",
        ]:

            plot_calibration_curve(
                replicate_summary,
                domain,
                os.path.join(
                    output_directory,
                    f"calibration_curve_{domain.lower()}.png",
                ),
            )

        plot_signal_input_scatter(
            dataframe,
            os.path.join(
                output_directory,
                "correlation_signal_input.png",
            ),
        )

        print("Generating reports...")

        generate_reports(output_directory)

        print()
        print("=" * 50)
        print("Task 9 completed successfully.")
        print(f"Output saved to: {output_directory}")
        print("=" * 50)

    except Exception as error:

        print()
        print("=" * 50)
        print("Task 9 failed!")
        print(f"Reason: {error}")
        print("=" * 50)

        sys.exit(1)

if __name__ == "__main__":
    main()