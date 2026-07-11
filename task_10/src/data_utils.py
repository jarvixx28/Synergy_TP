import numpy as np
import pandas as pd

DROP_COLUMNS = [
    "Unnamed: 15",
    "Unnamed: 16",
]

NUMERIC_COLUMNS = [
    "CO(GT)",
    "PT08.S1(CO)",
    "NMHC(GT)",
    "C6H6(GT)",
    "PT08.S2(NMHC)",
    "NOx(GT)",
    "PT08.S3(NOx)",
    "NO2(GT)",
    "PT08.S4(NO2)",
    "PT08.S5(O3)",
    "T",
    "RH",
    "AH",
]

REGRESSION_TARGET = "CO(GT)"

REGRESSION_FEATURES = [
    "PT08.S1(CO)",
    "PT08.S2(NMHC)",
    "T",
    "RH",
    "AH",
]

CLASSIFICATION_THRESHOLD = 2.0

CLASSIFICATION_FEATURES = [
    "PT08.S1(CO)",
    "PT08.S2(NMHC)",
    "PT08.S3(NOx)",
    "PT08.S4(NO2)",
    "PT08.S5(O3)",
    "T",
    "RH",
    "AH",
]

CLUSTERING_FEATURES = [
    "PT08.S1(CO)",
    "PT08.S2(NMHC)",
    "PT08.S3(NOx)",
    "PT08.S4(NO2)",
    "PT08.S5(O3)",
]

TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15

RANDOM_SEED = 42

if not np.isclose(
    TRAIN_RATIO +
    VALIDATION_RATIO +
    TEST_RATIO,
    1.0,
):
    raise ValueError(
        "Dataset split ratios must sum to 1."
    )


def load_data(
    file_path: str,
) -> pd.DataFrame:

    return pd.read_csv(
        file_path,
        sep=";",
        decimal=",",
        encoding="latin1",
        skip_blank_lines=True,
    )


def clean_dataset(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    dataframe = dataframe.copy()

    dataframe.drop(
        columns=DROP_COLUMNS,
        errors="ignore",
        inplace=True,
    )

    dataframe.replace(
        -200.0,
        np.nan,
        inplace=True,
    )

    for column in NUMERIC_COLUMNS:

        if column in dataframe.columns:

            dataframe[column] = pd.to_numeric(
                dataframe[column],
                errors="coerce",
            )

    return dataframe


def create_classification_target(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    dataframe = dataframe.copy()

    dataframe["high_pollution"] = (
        dataframe["CO(GT)"]
        > CLASSIFICATION_THRESHOLD
    ).astype(int)

    return dataframe


def prepare_regression_dataset(
    dataframe: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray]:

    required_columns = (
        REGRESSION_FEATURES +
        [REGRESSION_TARGET]
    )

    dataset = (
        dataframe[
            required_columns
        ]
        .dropna()
        .copy()
    )

    X = dataset[
        REGRESSION_FEATURES
    ].to_numpy(dtype=float)

    y = dataset[
        REGRESSION_TARGET
    ].to_numpy(dtype=float)

    return X, y


def prepare_classification_dataset(
    dataframe: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray]:

    dataframe = create_classification_target(
        dataframe
    )

    required_columns = (
        CLASSIFICATION_FEATURES +
        ["high_pollution"]
    )

    dataset = (
        dataframe[
            required_columns
        ]
        .dropna()
        .copy()
    )

    X = dataset[
        CLASSIFICATION_FEATURES
    ].to_numpy(dtype=float)

    y = dataset[
        "high_pollution"
    ].to_numpy(dtype=int)

    return X, y

def prepare_clustering_dataset(
    dataframe: pd.DataFrame,
) -> np.ndarray:

    dataset = (
        dataframe[
            CLUSTERING_FEATURES
        ]
        .dropna()
        .copy()
    )

    return dataset.to_numpy(
        dtype=float,
    )


def train_validation_test_split(
    X: np.ndarray,
    y: np.ndarray,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:

    if X.shape[0] != y.shape[0]:
        raise ValueError(
            "X and y must contain the same number of samples."
        )

    rng = np.random.default_rng(
        RANDOM_SEED,
    )

    indices = np.arange(
        X.shape[0],
    )

    rng.shuffle(
        indices,
    )

    X = X[
        indices
    ]

    y = y[
        indices
    ]

    train_end = int(
        TRAIN_RATIO *
        X.shape[0]
    )

    validation_end = (
        train_end
        +
        int(
            VALIDATION_RATIO *
            X.shape[0]
        )
    )

    X_train = X[
        :train_end
    ]

    y_train = y[
        :train_end
    ]

    X_validation = X[
        train_end:validation_end
    ]

    y_validation = y[
        train_end:validation_end
    ]

    X_test = X[
        validation_end:
    ]

    y_test = y[
        validation_end:
    ]

    return (
        X_train,
        X_validation,
        X_test,
        y_train,
        y_validation,
        y_test,
    )


def compute_standardization_parameters(
    X_train: np.ndarray,
) -> tuple[
    np.ndarray,
    np.ndarray,
]:

    mean = np.mean(
        X_train,
        axis=0,
    )

    std = np.std(
        X_train,
        axis=0,
    )

    std = np.where(
        std == 0,
        1.0,
        std,
    )

    return (
        mean,
        std,
    )

def apply_standardization(
    X: np.ndarray,
    mean: np.ndarray,
    std: np.ndarray,
) -> np.ndarray:

    if X.shape[1] != mean.shape[0]:
        raise ValueError(
            "Number of features does not match the standardization parameters."
        )

    return (
        X - mean
    ) / std