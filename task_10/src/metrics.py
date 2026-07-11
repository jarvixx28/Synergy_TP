import numpy as np


def mae(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> float:

    return float(
        np.mean(
            np.abs(
                y_true - y_pred
            )
        )
    )


def mse(
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


def rmse(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> float:

    return float(
        np.sqrt(
            mse(
                y_true,
                y_pred,
            )
        )
    )


def r2_score(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> float:

    ss_res = np.sum(
        (
            y_true -
            y_pred
        ) ** 2
    )

    ss_tot = np.sum(
        (
            y_true -
            np.mean(
                y_true
            )
        ) ** 2
    )

    if np.isclose(
        ss_tot,
        0.0,
    ):
        return 0.0

    return float(
        1.0 -
        (
            ss_res /
            ss_tot
        )
    )


def _confusion_matrix_counts(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> tuple[
    int,
    int,
    int,
    int,
]:

    tp = np.sum(
        (
            y_true == 1
        )
        &
        (
            y_pred == 1
        )
    )

    tn = np.sum(
        (
            y_true == 0
        )
        &
        (
            y_pred == 0
        )
    )

    fp = np.sum(
        (
            y_true == 0
        )
        &
        (
            y_pred == 1
        )
    )

    fn = np.sum(
        (
            y_true == 1
        )
        &
        (
            y_pred == 0
        )
    )

    return (
        int(tp),
        int(tn),
        int(fp),
        int(fn),
    )


def confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> np.ndarray:

    tp, tn, fp, fn = _confusion_matrix_counts(
        y_true,
        y_pred,
    )

    return np.array(
        [
            [
                tn,
                fp,
            ],
            [
                fn,
                tp,
            ],
        ],
        dtype=int,
    )

def accuracy(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> float:

    tp, tn, fp, fn = _confusion_matrix_counts(
        y_true,
        y_pred,
    )

    total = (
        tp +
        tn +
        fp +
        fn
    )

    if total == 0:
        return 0.0

    return (
        tp +
        tn
    ) / total


def precision(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> float:

    tp, _, fp, _ = _confusion_matrix_counts(
        y_true,
        y_pred,
    )

    denominator = (
        tp +
        fp
    )

    if denominator == 0:
        return 0.0

    return tp / denominator


def recall(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> float:

    tp, _, _, fn = _confusion_matrix_counts(
        y_true,
        y_pred,
    )

    denominator = (
        tp +
        fn
    )

    if denominator == 0:
        return 0.0

    return tp / denominator


def f1_score(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> float:

    p = precision(
        y_true,
        y_pred,
    )

    r = recall(
        y_true,
        y_pred,
    )

    if np.isclose(
        p + r,
        0.0,
    ):
        return 0.0

    return (
        2.0 *
        p *
        r
    ) / (
        p +
        r
    )


def inertia(
    X: np.ndarray,
    labels: np.ndarray,
    centroids: np.ndarray,
) -> float:

    return float(
        np.sum(
            (
                X -
                centroids[
                    labels
                ]
            ) ** 2
        )
    )


def cluster_counts(
    labels: np.ndarray,
) -> dict[int, int]:

    unique, counts = np.unique(
        labels,
        return_counts=True,
    )

    return {
        int(cluster): int(count)
        for cluster, count in zip(
            unique,
            counts,
        )
    }

def silhouette_score(
    X: np.ndarray,
    labels: np.ndarray,
) -> float:

    unique_clusters = np.unique(
        labels
    )

    if unique_clusters.size < 2:
        return 0.0

    scores = []

    for i in range(
        X.shape[0]
    ):

        same_cluster = (
            labels == labels[i]
        )

        same_cluster[i] = False

        if np.sum(
            same_cluster
        ) == 0:
            continue

        a = np.mean(
            np.linalg.norm(
                X[same_cluster] - X[i],
                axis=1,
            )
        )

        b = np.inf

        for cluster in unique_clusters:

            if cluster == labels[i]:
                continue

            other_cluster = (
                labels == cluster
            )

            if np.sum(
                other_cluster
            ) == 0:
                continue

            distance = np.mean(
                np.linalg.norm(
                    X[other_cluster] - X[i],
                    axis=1,
                )
            )

            b = min(
                b,
                distance,
            )

        denominator = max(
            a,
            b,
        )

        if np.isclose(
            denominator,
            0.0,
        ):
            scores.append(
                0.0
            )
        else:
            scores.append(
                (b - a) /
                denominator
            )

    if len(scores) == 0:
        return 0.0

    return float(
        np.mean(
            scores
        )
    )