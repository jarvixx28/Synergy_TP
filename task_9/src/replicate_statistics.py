import os
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from scipy.stats import t

CONFIDENCE_LEVEL = 0.95

STABLE_THRESHOLD = 0.05

MODERATE_THRESHOLD = 0.15

REQUIRED_COLUMNS = [

    "domain",
    "condition",
    "input_type",
    "input_value",
    "input_unit",
    "signal",
    "signal_unit",

]

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load calibration dataset.

    Parameters
    ----------
    file_path : str
        Path to CSV file.

    Returns
    -------
    pd.DataFrame
    """

    if not os.path.exists(file_path):

        raise FileNotFoundError(

            f"Dataset not found: {file_path}"

        )

    dataframe = pd.read_csv(file_path)

    return dataframe

def validate_dataset(
    dataframe: pd.DataFrame,
) -> None:
    """
    Validate input dataset.
    """

    if dataframe.empty:

        raise ValueError(

            "Dataset is empty."

        )

    missing = [

        column

        for column in REQUIRED_COLUMNS

        if column not in dataframe.columns

    ]

    if missing:

        raise ValueError(

            f"Missing columns: {missing}"

        )

    dataframe["signal"] = pd.to_numeric(

        dataframe["signal"],

        errors="coerce",

    )

    dataframe["input_value"] = pd.to_numeric(

        dataframe["input_value"],

        errors="coerce",

    )

def calculate_confidence_interval(
    mean: float,
    std: float,
    sample_size: int,
) -> Tuple[float, float]:
    """
    Calculate 95% confidence interval.
    """

    if (

        sample_size < 2

        or pd.isna(mean)

        or pd.isna(std)

    ):

        return (

            np.nan,

            np.nan,

        )

    alpha = 1 - CONFIDENCE_LEVEL

    critical_value = t.ppf(

        1 - alpha / 2,

        df=sample_size - 1,

    )

    margin = (

        critical_value

        * std

        / np.sqrt(sample_size)

    )

    return (

        mean - margin,

        mean + margin,

    )

def calculate_coefficient_of_variation(
    mean: float,
    std: float,
) -> float:
    """
    Calculate coefficient of variation.
    """

    if (

        pd.isna(mean)

        or mean == 0

        or pd.isna(std)

    ):

        return np.nan

    return std / mean

def assign_stability_flag(
    cv: float,
) -> str:
    """
    Assign stability label.
    """

    if pd.isna(cv):

        return "unreliable"

    if cv <= STABLE_THRESHOLD:

        return "stable"

    if cv <= MODERATE_THRESHOLD:

        return "moderate"

    return "unstable"

def calculate_group_statistics(
    group: pd.DataFrame,
) -> Dict:
    """
    Calculate statistics for one replicate group.
    """

    signal = group["signal"].dropna()

    sample_size = len(signal)

    mean = signal.mean()

    median = signal.median()

    minimum = signal.min()

    maximum = signal.max()

    variance = signal.var(ddof=1)

    std = signal.std(ddof=1)

    standard_error = (

        std / np.sqrt(sample_size)

        if sample_size > 1

        else np.nan

    )

    lower, upper = calculate_confidence_interval(

        mean,

        std,

        sample_size,

    )

    cv = calculate_coefficient_of_variation(

        mean,

        std,

    )

    return {

        "replicate_count": sample_size,

        "mean_signal": round(mean, 4),

        "median_signal": round(median, 4),

        "variance_signal": round(variance, 4),

        "standard_deviation_signal": round(std, 4),

        "standard_error_signal": round(standard_error, 4),

        "confidence_interval_lower": round(lower, 4),

        "confidence_interval_upper": round(upper, 4),

        "coefficient_of_variation": round(cv, 4),

        "minimum_signal": round(minimum, 4),

        "maximum_signal": round(maximum, 4),

        "stability_flag": assign_stability_flag(cv),

    }

def calculate_replicate_statistics(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate replicate statistics for all groups.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Input calibration dataset.

    Returns
    -------
    pd.DataFrame
        Replicate statistics summary.
    """

    validate_dataset(dataframe)

    grouping_columns = [
        "domain",
        "condition",
        "input_type",
        "input_value",
        "input_unit",
        "signal_unit",
    ]

    summary = []

    grouped = dataframe.groupby(
        grouping_columns,
        dropna=False,
    )

    for group_key, group in grouped:

        statistics = calculate_group_statistics(group)

        row = dict(zip(grouping_columns, group_key))

        row.update(statistics)

        summary.append(row)

    summary_dataframe = pd.DataFrame(summary)

    return summary_dataframe

def save_replicate_summary(
    summary_dataframe: pd.DataFrame,
    output_path: str,
) -> None:
    """
    Save replicate statistics summary as CSV.

    Parameters
    ----------
    summary_dataframe : pd.DataFrame
        Statistics summary.

    output_path : str
        Output CSV path.
    """

    output_directory = os.path.dirname(output_path)

    if output_directory:

        os.makedirs(
            output_directory,
            exist_ok=True,
        )

    summary_dataframe.to_csv(
        output_path,
        index=False,
    )