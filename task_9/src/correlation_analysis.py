import os
from typing import Dict, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import pearsonr
from scipy.stats import spearmanr

from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error,
)

RELATIONSHIPS = [

    {
        "name": "Biochem Signal vs Concentration",

        "domain": "Biochem",

        "x": "input_value",

        "y": "signal",
    },

    {
        "name": "Electronics Signal vs Load",

        "domain": "Electronics",

        "x": "input_value",

        "y": "signal",
    },

    {
        "name": "Electronics Signal vs Temperature",

        "domain": "Electronics",

        "x": "temperature_c",

        "y": "signal",
    },

    {
        "name": "Mechanical Signal vs Load",

        "domain": "Mechanical",

        "x": "input_value",

        "y": "signal",
    },

    {
        "name": "Mechanical Stress vs Load",

        "domain": "Mechanical",

        "x": "input_value",

        "y": "stress_mpa",
    },

]

def validate_columns(
    dataframe: pd.DataFrame,
    columns: list,
) -> None:
    """
    Ensure required columns exist.
    """

    missing = [

        column

        for column in columns

        if column not in dataframe.columns

    ]

    if missing:

        raise ValueError(

            f"Missing columns: {missing}"

        )
    
def prepare_numeric_data(
    dataframe,
    x_column,
    y_column,
):
    """
    Prepare numeric data.
    """

    data = dataframe[
        [x_column, y_column]
    ].copy()

    data[x_column] = pd.to_numeric(

        data[x_column],

        errors="coerce",

    )

    data[y_column] = pd.to_numeric(

        data[y_column],

        errors="coerce",

    )

    data = data.dropna()

    return data

def calculate_pearson(
    x,
    y,
) -> Optional[float]:
    """
    Pearson correlation.
    """

    if len(x) < 2:

        return np.nan

    if x.nunique() == 1:

        return np.nan

    if y.nunique() == 1:

        return np.nan

    try:

        value, _ = pearsonr(x, y)

        return value

    except Exception:

        return np.nan
    
def calculate_spearman(
    x,
    y,
):
    """
    Spearman correlation.
    """

    if len(x) < 2:

        return np.nan

    try:

        value, _ = spearmanr(x, y)

        return value

    except Exception:

        return np.nan
    
def fit_linear_regression(
    x,
    y,
):
    """
    Fit regression model.
    """

    model = LinearRegression()

    model.fit(

        x.values.reshape(-1,1),

        y,

    )

    prediction = model.predict(

        x.values.reshape(-1,1)

    )

    return (

        model,

        prediction,

    )

def calculate_regression_metrics(
    actual,
    prediction,
):
    """
    Calculate regression metrics.
    """

    return {

        "r_squared":

            r2_score(
                actual,
                prediction,
            ),

        "mae":

            mean_absolute_error(
                actual,
                prediction,
            ),

        "rmse":

            np.sqrt(

                mean_squared_error(
                    actual,
                    prediction,
                )

            ),

    }

def analyze_relationship(
    dataframe: pd.DataFrame,
    relationship: Dict,
) -> Optional[Dict]:
    """
    Analyse one relationship.
    """

    domain_data = dataframe[
        dataframe["domain"] == relationship["domain"]
    ]

    data = prepare_numeric_data(
        domain_data,
        relationship["x"],
        relationship["y"],
    )

    if len(data) < 2:
        return None

    x = data[relationship["x"]]
    y = data[relationship["y"]]

    pearson = calculate_pearson(x, y)

    spearman = calculate_spearman(x, y)

    model, prediction = fit_linear_regression(x, y)

    metrics = calculate_regression_metrics(
        y,
        prediction,
    )

    return {

        "relationship": relationship["name"],

        "domain": relationship["domain"],

        "x_variable": relationship["x"],

        "y_variable": relationship["y"],

        "sample_count": len(data),

        "pearson_correlation": round(pearson, 4),

        "spearman_correlation": round(spearman, 4),

        "slope": round(model.coef_[0], 4),

        "intercept": round(model.intercept_, 4),

        "r_squared": round(metrics["r_squared"], 4),

        "mae": round(metrics["mae"], 4),

        "rmse": round(metrics["rmse"], 4),

    }

def generate_correlation_summary(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate correlation summary.
    """

    results = []

    for relationship in RELATIONSHIPS:

        output = analyze_relationship(
            dataframe,
            relationship,
        )

        if output is not None:

            results.append(output)

    return pd.DataFrame(results)

def generate_calibration_summary(
    correlation_summary: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create calibration summary.
    """

    calibration = correlation_summary[[
        "relationship",

        "domain",

        "slope",

        "intercept",

        "r_squared",

        "mae",

        "rmse",

    ]].copy()

    return calibration

def save_summary(
    dataframe: pd.DataFrame,
    output_path: str,
) -> None:
    """
    Save dataframe.
    """

    directory = os.path.dirname(
        output_path
    )

    if directory:

        os.makedirs(
            directory,
            exist_ok=True,
        )

    dataframe.to_csv(

        output_path,

        index=False,

    )

def plot_calibration_curve(
    summary_dataframe: pd.DataFrame,
    domain: str,
    output_path: str,
) -> None:
    """
    Plot calibration curve.
    """

    data = summary_dataframe[
        summary_dataframe["domain"] == domain
    ].sort_values("input_value")

    if data.empty:
        return

    plt.figure(figsize=(7,5))

    plt.plot(

        data["input_value"],

        data["mean_signal"],

        marker="o",

        linewidth=2,

    )

    plt.fill_between(

        data["input_value"],

        data["confidence_interval_lower"],

        data["confidence_interval_upper"],

        alpha=0.2,

    )

    plt.title(
        f"{domain} Calibration Curve"
    )

    plt.xlabel("Input Value")

    plt.ylabel("Mean Signal")

    plt.grid(True)

    os.makedirs(

        os.path.dirname(output_path),

        exist_ok=True,

    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

def plot_signal_input_scatter(
    dataframe: pd.DataFrame,
    output_path: str,
) -> None:
    """
    Scatter plot.
    """

    plt.figure(figsize=(8,6))

    for relationship in RELATIONSHIPS:

        subset = dataframe[
            dataframe["domain"] == relationship["domain"]
        ]

        subset = prepare_numeric_data(
            subset,
            relationship["x"],
            relationship["y"],
        )

        if subset.empty:
            continue

        plt.scatter(

            subset[relationship["x"]],

            subset[relationship["y"]],

            label=relationship["name"],

        )

    plt.title(
        "Signal Relationships"
    )

    plt.xlabel("Input Variable")

    plt.ylabel("Measured Signal")

    plt.legend(fontsize=8)

    plt.grid(True)

    plt.savefig(

        output_path,

        dpi=300,

        bbox_inches="tight",

    )

    plt.close()   