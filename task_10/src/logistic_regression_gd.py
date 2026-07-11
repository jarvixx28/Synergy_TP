import numpy as np


class LogisticRegressionGD:

    def __init__(
        self,
        learning_rate: float = 0.01,
        iterations: int = 1000,
        threshold: float = 0.5,
    ) -> None:

        if learning_rate <= 0:
            raise ValueError(
                "Learning rate must be greater than zero."
            )

        if iterations <= 0:
            raise ValueError(
                "Iterations must be greater than zero."
            )

        if not (
            0.0 <
            threshold <
            1.0
        ):
            raise ValueError(
                "Threshold must be between 0 and 1."
            )

        self.learning_rate = learning_rate
        self.iterations = iterations
        self.threshold = threshold

        self.weights_ = None
        self.bias_ = 0.0

        self.loss_history_ = []

    def _sigmoid(
        self,
        z: np.ndarray,
    ) -> np.ndarray:

        z = np.clip(
            z,
            -500,
            500,
        )

        return (
            1.0 /
            (
                1.0 +
                np.exp(-z)
            )
        )

    def _predict_probability(
        self,
        X: np.ndarray,
    ) -> np.ndarray:

        linear_output = (
            X @
            self.weights_
        ) + self.bias_

        return self._sigmoid(
            linear_output
        )

    def _compute_loss(
        self,
        y_true: np.ndarray,
        predictions: np.ndarray,
    ) -> float:

        predictions = np.clip(
            predictions,
            1e-15,
            1.0 - 1e-15,
        )

        return float(
            -np.mean(
                (
                    y_true *
                    np.log(
                        predictions
                    )
                )
                +
                (
                    (
                        1 -
                        y_true
                    )
                    *
                    np.log(
                        1 -
                        predictions
                    )
                )
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
            X.T @
            errors
        ) / samples

        db = np.mean(
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

            predictions = self._predict_probability(
                X
            )

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

    def predict_proba(
        self,
        X: np.ndarray,
    ) -> np.ndarray:

        if self.weights_ is None:
            raise ValueError(
                "Model has not been fitted yet."
            )

        return self._predict_probability(
            X
        )

    def predict(
        self,
        X: np.ndarray,
    ) -> np.ndarray:

        probabilities = self.predict_proba(
            X
        )

        return (
            probabilities >=
            self.threshold
        ).astype(
            int
        )