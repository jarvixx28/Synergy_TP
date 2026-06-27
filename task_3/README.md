# Task 3: Manual CSV Parser and Pandas Comparison

## Objective

The objective of this task is to understand how CSV data can be parsed manually using Python file handling before using high-level libraries such as pandas. The same dataset is processed using both approaches and the generated summaries are compared.

---

## Folder Structure

```
task_3/
│
├── README.md
├── data/
│   └── submissions.csv
├── output/
│   ├── manual_summary.json
│   ├── pandas_summary.json
│   └── comparison_report.md
└── src/
    ├── manual_parser.py
    ├── pandas_parser.py
    └── main.py
```

---

## Required Packages

* pandas

---

## Setup Instructions

1. Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Run Command

From the repository root:

```bash
python task_3/src/main.py task_3/data/submissions.csv
```

---

## Expected Output Files

Running the program generates:

* task_3/output/manual_summary.json
* task_3/output/pandas_summary.json
* task_3/output/comparison_report.md

---

## Implemented Logic

The program reads the student submission CSV file using two different approaches.

The manual parser uses Python file handling and string operations to convert raw CSV text into structured dictionaries.

The pandas implementation performs the same analysis using the pandas library.

Both implementations generate identical summaries, which are compared to verify correctness.
