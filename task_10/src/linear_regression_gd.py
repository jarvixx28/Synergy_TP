import numpy as np


class LinearRegressionGD:

    def __init__(
        self,
        learning_rate: float = 0.01,
        iterations: int = 1000,
    ) -> None:

        if learning_rate <= 0:
            raise ValueError(
                "Learning rate must be greater than zero."
            )

        if iterations <= 0:
            raise ValueError(
                "Iterations must be greater than zero."
            )

        self.learning_rate = learning_rate
        self.iterations = iterations

        self.weights_ = None
        self.bias_ = 0.0

        self.loss_history_ = []

    def _compute_loss(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
    ) -> float:

        return float(
            np.mean(
                (
                    y_true -
                    y_pred
                ) ** 2
            )
        )

    def _compute_gradients(
        self,
        X: np.ndarray,
        y: np.ndarray,
        predictions: np.ndarray,
    ) -> tuple[
        np.ndarray,
        float,
    ]:

        samples = X.shape[0]

        errors = (
            predictions -
            y
        )

        dw = (
            2.0 /
            samples
        ) * (
            X.T @
            errors
        )

        db = (
            2.0 /
            samples
        ) * np.sum(
            errors
        )

        return (
            dw,
            float(db),
        )

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
    ) -> None:

        if X.shape[0] != y.shape[0]:
            raise ValueError(
                "X and y must contain the same number of samples."
            )

        _, features = X.shape

        self.weights_ = np.zeros(
            features,
            dtype=float,
        )

        self.bias_ = 0.0

        self.loss_history_ = []

        for _ in range(
            self.iterations
        ):

            predictions = (
                X @
                self.weights_
            ) + self.bias_

            loss = self._compute_loss(
                y,
                predictions,
            )

            self.loss_history_.append(
                loss
            )

            dw, db = self._compute_gradients(
                X,
                y,
                predictions,
            )

            self.weights_ -= (
                self.learning_rate *
                dw
            )

            self.bias_ -= (
                self.learning_rate *
                db
            )

    def predict(
        self,
        X: np.ndarray,
    ) -> np.ndarray:

        if self.weights_ is None:
            raise ValueError(
                "Model has not been fitted yet."
            )

        return (
            X @
            self.weights_
        ) + self.bias_