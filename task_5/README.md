# Task 5 - Data Visualization using Matplotlib

## Objective

Generate visualizations from the cleaned dataset produced in Task 4 using matplotlib.

---

## Folder Structure

```text
task_5/
│
├── README.md
├── output/
│   ├── domain_average_score.png
│   ├── attendance_vs_score.png
│   ├── submission_status_count.png
│   └── plot_summary.md
└── src/
    ├── visualize.py
    └── main.py
```

---

## Required Packages

* pandas
* matplotlib

Install using:

```bash
pip install -r requirements.txt
```

---

## Run Command

From the repository root:

```bash
python task_5/src/main.py task_4/output/cleaned_students.csv task_5/output
```

---

## Generated Outputs

Running the program generates:

* `domain_average_score.png`
* `attendance_vs_score.png`
* `submission_status_count.png`
* `plot_summary.md`

All files are saved inside `task_5/output/`.

---

## Implementation Summary

The program loads the cleaned dataset from Task 4, generates three matplotlib visualizations, and writes a short markdown summary explaining what each plot represents.
