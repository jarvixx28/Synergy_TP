import sys

from analyzer import (
    read_submissions,
    get_submitted_students,
    calculate_average_score,
    get_domain_wise_average,
    get_missing_submissions,
    write_summary,
)


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python task_2/src/main.py "
            "task_2/data/submissions.csv "
            "task_2/output/summary.json"
        )
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    data = read_submissions(input_file)

    if not data:
        return

    submitted_students = get_submitted_students(data)
    missing_students = get_missing_submissions(data)

    highest_scorer = max(
        submitted_students,
        key=lambda student: student["score"]
    )

    lowest_scorer = min(
        submitted_students,
        key=lambda student: student["score"]
    )

    below_five = [
        student["name"]
        for student in submitted_students
        if student["score"] < 5
    ]

    summary = {
        "total_students": len(data),
        "submitted_students": len(submitted_students),
        "missing_submissions": len(missing_students),
        "average_score": calculate_average_score(data),
        "highest_scorer": highest_scorer["name"],
        "lowest_scorer": lowest_scorer["name"],
        "domain_wise_average": get_domain_wise_average(data),
        "students_not_submitted": missing_students,
        "students_below_5": below_five,
    }

    print(f"Total Students: {len(data)}")
    print(f"Submitted: {len(submitted_students)}")
    print(f"Missing: {len(missing_students)}")
    print(f"Average Score: {calculate_average_score(data)}")
    print(f"Highest Scorer: {highest_scorer['name']}")
    print(f"Missing Submissions: {missing_students}")

    write_summary(summary, output_file)

    print(f"Summary written to {output_file}")


if __name__ == "__main__":
    main()