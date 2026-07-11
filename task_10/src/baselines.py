import numpy as np


class RegressionBaseline:

    def __init__(
        self,
    ) -> None:

        self.mean_target = None

    def fit(
        self,
        y_train: np.ndarray,
    ) -> None:

        y_train = np.asarray(
            y_train,
            dtype=float,
        )

        self.mean_target = float(
            np.mean(
                y_train
            )
        )

    def predict(
        self,
        X: np.ndarray,
    ) -> np.ndarray:

        if self.mean_target is None:
            raise ValueError(
                "Model has not been fitted yet."
            )

        return np.full(
            X.shape[0],
            self.mean_target,
            dtype=float,
        )


class ClassificationBaseline:

    def __init__(
        self,
    ) -> None:

        self.majority_class = None

    def fit(
        self,
        y_train: np.ndarray,
    ) -> None:

        y_train = np.asarray(
            y_train,
            dtype=int,
        )

        values, counts = np.unique(
            y_train,
            return_counts=True,
        )

        self.majority_class = int(
            values[
                np.argmax(
                    counts
                )
            ]
        )

    def predict(
        self,
        X: np.ndarray,
    ) -> np.ndarray:

        if self.majority_class is None:
            raise ValueError(
                "Model has not been fitted yet."
            )

        return np.full(
            X.shape[0],
            self.majority_class,
            dtype=int,
        )