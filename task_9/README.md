# Task 9 – Statistical Analysis and Feature Engineering

## Project Overview

This project is part of the **TaskPhase Student Project** and focuses on performing statistical analysis and feature engineering on calibration data collected from three different experimental domains:

- Biochemistry
- Electronics
- Mechanical

The objective is to analyse replicate measurements, study correlations between input variables and sensor outputs, engineer useful features, and generate datasets suitable for further data analysis and machine learning applications.

---

## Objectives

- Perform descriptive statistical analysis on replicate measurements.
- Evaluate calibration quality using statistical metrics.
- Analyse relationships between input variables and measured signals.
- Generate calibration curves and correlation plots.
- Engineer meaningful features from raw experimental data.
- Prepare an ML-ready dataset for future modelling tasks.

---

## Project Structure

```
task_9/
│
├── data/
│   └── calibration_measurements.csv
│
├── output/
│   ├── replicate_summary.csv
│   ├── correlation_summary.csv
│   ├── calibration_summary.csv
│   ├── engineered_features.csv
│   ├── ml_ready_dataset.csv
│   ├── calibration_curve_biochem.png
│   ├── calibration_curve_electronics.png
│   ├── calibration_curve_mechanical.png
│   ├── correlation_signal_input.png
│   ├── replicate_analysis.md
│   ├── correlation_limitations.md
│   ├── feature_dictionary.md
│   └── feature_summary.md
│
├── src/
│   ├── replicate_statistics.py
│   ├── correlation_analysis.py
│   ├── feature_engineering.py
│   └── main.py
│
└── README.md
```

---

## Features Implemented

### Replicate Statistics

The following statistical measures are computed for every calibration condition:

- Mean
- Median
- Variance
- Standard Deviation
- Standard Error
- 95% Confidence Interval
- Coefficient of Variation (CV)
- Stability Classification

---

### Correlation Analysis

The project evaluates relationships between calibration variables using:

- Pearson Correlation
- Spearman Correlation
- Linear Regression
- Coefficient of Determination (R²)
- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)

Calibration plots are generated for each experimental domain.

---

### Feature Engineering

The following derived features are generated:

- Normalized Signal
- Percentage Error
- Electrical Power
- Stress Ratio
- Rolling Average
- Machine Learning Readiness Flag

These engineered features enhance the dataset and improve its suitability for statistical modelling and future machine learning applications.

---

## Output Files

Running the project automatically generates:

### CSV Files

- replicate_summary.csv
- correlation_summary.csv
- calibration_summary.csv
- engineered_features.csv
- ml_ready_dataset.csv

### Visualizations

- calibration_curve_biochem.png
- calibration_curve_electronics.png
- calibration_curve_mechanical.png
- correlation_signal_input.png

### Reports

- replicate_analysis.md
- correlation_limitations.md
- feature_dictionary.md
- feature_summary.md

---

## Technologies Used

- Python 3
- Pandas
- NumPy
- SciPy
- Matplotlib
- Scikit-learn

---

## How to Run

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the project from the root directory:

```bash
python task_9/src/main.py task_9/data/calibration_measurements.csv task_9/output
```

---

## Learning Outcomes

This project demonstrates the application of:

- Descriptive Statistics
- Correlation Analysis
- Linear Regression
- Data Preprocessing
- Feature Engineering
- Data Visualization
- Modular Python Programming
- Scientific Computing using Python

---

## Author

**Atharva Nischal**

Department of Cyber Physical Systems

MIT Manipal

TaskPhase Student Project