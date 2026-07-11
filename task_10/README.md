# Task 10: Machine Learning from Scratch

## Overview

This project implements three fundamental machine learning algorithms from scratch using only NumPy, Pandas, and Matplotlib. No machine learning libraries such as Scikit-learn have been used. The project demonstrates data preprocessing, model implementation, evaluation, visualization, and comparison using the Air Quality dataset.

---

## Dataset

**Dataset:** Air Quality UCI Dataset

The dataset contains hourly averaged responses from chemical sensors along with meteorological variables collected in an Italian city.

Regression, classification, and clustering tasks are performed using different feature subsets extracted from this dataset.

---

## Implemented Algorithms

### 1. Linear Regression (Gradient Descent)

- Implemented completely from scratch
- Batch Gradient Descent optimization
- Mean Squared Error loss
- Used for predicting continuous CO concentration

Evaluation Metrics:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

---

### 2. Logistic Regression (Gradient Descent)

- Implemented completely from scratch
- Sigmoid activation
- Binary Cross Entropy loss
- Gradient Descent optimization
- Used for binary air pollution classification

Evaluation Metrics:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

---

### 3. K-Means Clustering

- Implemented completely from scratch
- Random centroid initialization
- Euclidean distance
- Iterative centroid updates

Evaluation Metrics:

- Inertia
- Silhouette Score
- Cluster Counts

---

## Baseline Models

Two baseline models are implemented for comparison.

### Regression Baseline

Predicts the mean of the training target for every sample.

### Classification Baseline

Predicts the majority class found in the training dataset.

---

## Project Structure

```
task_10/

│

├── data/
│   └── AirQualityUCI.csv
│
├── output/
│   ├── regression_metrics.json
│   ├── classification_metrics.json
│   ├── clustering_metrics.json
│   ├── regression_predictions.csv
│   ├── classification_predictions.csv
│   ├── clustering_assignments.csv
│   ├── regression_loss_curve.png
│   ├── classification_loss_curve.png
│   ├── actual_vs_predicted.png
│   ├── confusion_matrix.png
│   ├── clustering_plot.png
│   ├── model_comparison.md
│   └── error_analysis.md
│
└── src/
    ├── main.py
    ├── data_utils.py
    ├── baselines.py
    ├── linear_regression_gd.py
    ├── logistic_regression_gd.py
    ├── kmeans.py
    └── metrics.py
```

---

## Requirements

- Python 3.10+
- NumPy
- Pandas
- Matplotlib

Install dependencies:

```bash
pip install numpy pandas matplotlib
```

---

## Running the Project

Run the following command from the project root:

```bash
python task_10/src/main.py task_10/data/AirQualityUCI.csv task_10/output
```

---

## Outputs Generated

### JSON Files

- regression_metrics.json
- classification_metrics.json
- clustering_metrics.json

These files contain the evaluation metrics for each implemented model.

### CSV Files

- regression_predictions.csv
- classification_predictions.csv
- clustering_assignments.csv

These contain prediction results and cluster assignments.

### Visualizations

- Regression Loss Curve
- Classification Loss Curve
- Actual vs Predicted Plot
- Confusion Matrix
- K-Means Cluster Visualization

### Reports

- model_comparison.md
- error_analysis.md

These contain qualitative analysis and discussion of the implemented models.

---

## Data Preprocessing

The preprocessing pipeline includes:

- Removal of unnecessary columns
- Handling missing values
- Conversion of numeric columns
- Feature selection
- Creation of binary classification labels
- Train–Validation–Test split
- Standardization using training statistics only to prevent data leakage

---

## Implementation Details

The project uses:

- NumPy for numerical computations
- Pandas for dataset handling
- Matplotlib for visualization

No external machine learning libraries have been used.

---

## Learning Objectives

This project demonstrates:

- Gradient Descent optimization
- Linear Regression
- Logistic Regression
- K-Means Clustering
- Model evaluation
- Feature standardization
- Data preprocessing
- Baseline model comparison
- Data visualization
- Preventing data leakage
