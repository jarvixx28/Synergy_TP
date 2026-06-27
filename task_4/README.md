# Task 4 - Data Cleaning and Validation

## Objective

The objective of this task is to clean a messy student dataset, standardize inconsistent values, handle missing and invalid data, validate the cleaned dataset, and generate output files for further analysis.

---

## Folder Structure

```
task_4/
│
├── README.md
├── data/
│   └── messy_students.csv
├── output/
│   ├── cleaned_students.csv
│   ├── summary_before.json
│   ├── summary_after.json
│   └── cleaning_report.md
└── src/
    ├── clean_data.py
    ├── validate_data.py
    └── main.py
```

---

## Requirements

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## How to Run

From the root of the repository (`Synergy_TP`), execute:

```bash
python task_4/src/main.py task_4/data/messy_students.csv task_4/output/cleaned_students.csv
```

---

## Cleaning Operations

The program performs the following operations:

* Removes duplicate records.
* Standardizes domain names.
* Cleans attendance values.
* Converts textual scores to numeric values.
* Converts textual study hours to numeric values.
* Converts heights to centimetres.
* Converts weights to kilograms.
* Standardizes submitted values.
* Handles missing values using the column median.
* Validates the cleaned dataset.

---

## Validation

The cleaned dataset is checked for:

* Duplicate student IDs
* Attendance values between 0 and 100
* Numeric score values
* Numeric study hours
* Numeric height values
* Numeric weight values
* Valid domain names
* Valid submitted values
* Missing values in critical columns

---

## Output Files

Running the program generates:

* `cleaned_students.csv`
* `summary_before.json`
* `summary_after.json`
* `cleaning_report.md`

These files are saved inside the `task_4/output` directory.
