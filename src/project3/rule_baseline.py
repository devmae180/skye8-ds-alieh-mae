import numpy as np

from data_cleaning import clean_lots, time_split


def grading_rule(df):
    """Apply the published cocoa grading standard."""
    return (
        (df["moisture_pct"] > 8.0)
        | (df["defect_pct"] > 6.0)
        | (df["bean_count_per_100g"] > 110)
        | (df["fermentation_days"] < 4)
    ).astype(int)


def precision_recall(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    true_positive = ((y_true == 1) & (y_pred == 1)).sum()
    false_positive = ((y_true == 0) & (y_pred == 1)).sum()
    false_negative = ((y_true == 1) & (y_pred == 0)).sum()

    precision = (
        true_positive / (true_positive + false_positive)
        if true_positive + false_positive
        else 0.0
    )

    recall = (
        true_positive / (true_positive + false_negative)
        if true_positive + false_negative
        else 0.0
    )

    return precision, recall


def average_precision(y_true, scores):
    """Calculate average precision for binary scores."""
    y_true = np.asarray(y_true)
    scores = np.asarray(scores)

    order = np.argsort(-scores)
    y_true = y_true[order]

    positives = y_true.sum()

    if positives == 0:
        return 0.0

    cumulative_tp = np.cumsum(y_true)
    ranks = np.arange(1, len(y_true) + 1)

    precision_at_rank = cumulative_tp / ranks

    return float((precision_at_rank * y_true).sum() / positives)


if __name__ == "__main__":
    df = clean_lots()
    _, validation, _ = time_split(df)

    y_true = validation["rejected"].to_numpy()
    predictions = grading_rule(validation).to_numpy()

    precision, recall = precision_recall(y_true, predictions)
    pr_auc = average_precision(y_true, predictions)

    always_accept = np.zeros(len(validation), dtype=int)
    always_accept_accuracy = (always_accept == y_true).mean()

    print("PUBLISHED GRADING STANDARD")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"PR-AUC:    {pr_auc:.4f}")

    print("\nALWAYS-ACCEPT BASELINE")
    print(f"Accuracy:  {always_accept_accuracy:.4f}")
    print("Recall:    0.0000")

    print(
        "\nAccuracy alone is misleading: always accepting lots "
        "can achieve high accuracy while detecting no rejected lots."
    )