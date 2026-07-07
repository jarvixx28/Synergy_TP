import os

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = [

    "signal",

    "baseline_signal",

    "expected_signal",

    "voltage_v",

    "current_a",

    "stress_mpa",

    "reference_stress_mpa",

]

def validate_dataset(
    dataframe: pd.DataFrame,
):

    """
    Validate feature engineering input.
    """

    missing = [

        column

        for column in REQUIRED_COLUMNS

        if column not in dataframe.columns

    ]

    if missing:

        raise ValueError(

            f"Missing columns: {missing}"

        )
    
def calculate_normalized_signal(
    signal,
    baseline,
):

    """
    Normalize signal.
    """

    if (

        pd.isna(signal)

        or pd.isna(baseline)

        or baseline == 0

    ):

        return np.nan

    return signal / baseline

def calculate_signal_error(
    signal,
    expected,
):

    """
    Percentage error.
    """

    if (

        pd.isna(signal)

        or pd.isna(expected)

        or expected == 0

    ):

        return np.nan

    return (

        (signal - expected)

        / expected

    ) * 100

def calculate_power(
    voltage,
    current,
):

    """
    Electrical power.
    """

    if (

        pd.isna(voltage)

        or pd.isna(current)

    ):

        return np.nan

    return voltage * current

def calculate_stress_ratio(
    measured,
    reference,
):

    """
    Stress ratio.
    """

    if (

        pd.isna(measured)

        or pd.isna(reference)

        or reference == 0

    ):

        return np.nan

    return measured / reference

def calculate_rolling_average(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate rolling average of signal within each
    domain and condition.
    """

    dataframe = dataframe.copy()

    dataframe = dataframe.sort_values(
        ["domain", "condition", "time_step"]
    )

    dataframe["rolling_average"] = (
        dataframe
        .groupby(["domain", "condition"])["signal"]
        .transform(
            lambda signal: signal.rolling(
                window=3,
                min_periods=1,
            ).mean()
        )
    )

    return dataframe

def assign_ml_ready_flag(
    row,
):

    """
    ML readiness.
    """

    important = [

        row["normalized_signal"],

        row["error_percent"],

    ]

    if all(

        not pd.isna(x)

        for x in important

    ):

        return True

    return False

def engineer_features(
    dataframe,
):

    """
    Generate engineered features.
    """

    validate_dataset(dataframe)

    dataframe = dataframe.copy()

    dataframe["normalized_signal"] = dataframe.apply(

        lambda row:

        calculate_normalized_signal(

            row["signal"],

            row["baseline_signal"],

        ),

        axis=1,

    )

    dataframe["error_percent"] = dataframe.apply(

        lambda row:

        calculate_signal_error(

            row["signal"],

            row["expected_signal"],

        ),

        axis=1,

    )

    dataframe["power"] = dataframe.apply(

        lambda row:

        calculate_power(

            row["voltage_v"],

            row["current_a"],

        ),

        axis=1,

    )

    dataframe["stress_ratio"] = dataframe.apply(

        lambda row:

        calculate_stress_ratio(

            row["stress_mpa"],

            row["reference_stress_mpa"],

        ),

        axis=1,

    )

    dataframe = calculate_rolling_average(

        dataframe

    )

    dataframe["ml_ready"] = dataframe.apply(

        assign_ml_ready_flag,

        axis=1,

    )

    return dataframe

def save_dataset(
    dataframe,
    output_path,
):

    """
    Save engineered dataset.
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