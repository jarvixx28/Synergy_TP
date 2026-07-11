import numpy as np


class KMeans:

    def __init__(
        self,
        n_clusters: int = 3,
        max_iterations: int = 300,
        random_seed: int = 42,
    ) -> None:

        if n_clusters <= 0:
            raise ValueError(
                "Number of clusters must be greater than zero."
            )

        if max_iterations <= 0:
            raise ValueError(
                "Maximum iterations must be greater than zero."
            )

        self.n_clusters = n_clusters
        self.max_iterations = max_iterations
        self.random_seed = random_seed

        self.centroids_ = None
        self.labels_ = None

    def _initialize_centroids(
        self,
        X: np.ndarray,
    ) -> np.ndarray:

        rng = np.random.default_rng(
            self.random_seed
        )

        indices = rng.choice(
            X.shape[0],
            size=self.n_clusters,
            replace=False,
        )

        return X[
            indices
        ].copy()

    def _compute_distances(
        self,
        X: np.ndarray,
        centroids: np.ndarray,
    ) -> np.ndarray:

        differences = (
            X[:, np.newaxis, :] -
            centroids
        )

        return np.sqrt(
            np.sum(
                differences ** 2,
                axis=2,
            )
        )

    def _assign_clusters(
        self,
        distances: np.ndarray,
    ) -> np.ndarray:

        return np.argmin(
            distances,
            axis=1,
        )

    def _update_centroids(
        self,
        X: np.ndarray,
        labels: np.ndarray,
        previous_centroids: np.ndarray,
    ) -> np.ndarray:

        rng = np.random.default_rng(
            self.random_seed
        )

        centroids = []

        for cluster in range(
            self.n_clusters
        ):

            cluster_points = X[
                labels == cluster
            ]

            if cluster_points.shape[0] == 0:

                centroids.append(
                    previous_centroids[
                    cluster
                ]
                )

            else:

                centroids.append(
                    np.mean(
                        cluster_points,
                        axis=0,
                    )
                )

        return np.asarray(
            centroids,
            dtype=float,
        )
    
    def fit(
        self,
        X: np.ndarray,
    ) -> None:

        if self.n_clusters > X.shape[0]:
            raise ValueError(
                "Number of clusters cannot exceed the number of samples."
            )

        self.centroids_ = self._initialize_centroids(
            X
        )

        for _ in range(
            self.max_iterations
        ):

            distances = self._compute_distances(
                X,
                self.centroids_,
            )

            labels = self._assign_clusters(
                distances,
            )

            new_centroids = self._update_centroids(
                X,
                labels,
                self.centroids_,
            )

            if np.allclose(
                self.centroids_,
                new_centroids,
                atol=1e-6,
            ):
                break

            self.centroids_ = new_centroids

        final_distances = self._compute_distances(
            X,
            self.centroids_,
        )

        self.labels_ = self._assign_clusters(
            final_distances,
        )

    def predict(
        self,
        X: np.ndarray,
    ) -> np.ndarray:

        if self.centroids_ is None:
            raise ValueError(
                "Model has not been fitted yet."
            )

        distances = self._compute_distances(
            X,
            self.centroids_,
        )

        return self._assign_clusters(
            distances,
        )