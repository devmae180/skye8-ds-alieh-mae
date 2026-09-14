import numpy as np
import pandas as pd

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import average_precision_score, precision_score, recall_score

from data_cleaning import clean_lots, time_split


FEATURES = [
    "lot_weight_kg",
    "moisture_pct",
    "fermentation_days",
    "bean_count_per_100g",
    "defect_pct",
    "transport_days",
]


def prepare_data(df):
    X = df[FEATURES].copy()
    y = df["rejected"].astype(int)
    return X, y


def oversample_minority(X, y, random_state=42):
    """Oversample rejected lots using training data only."""
    rng = np.random.default_rng(random_state)

    positive_idx = np.flatnonzero(y.to_numpy() == 1)
    negative_idx = np.flatnonzero(y.to_numpy() == 0)

    extra_count = len(negative_idx) - len(positive_idx)

    sampled_positive = rng.choice(
        positive_idx,
        size=extra_count,
        replace=True,
    )

    selected_idx = np.concatenate(
        [np.arange(len(y)), sampled_positive]
    )

    return (
        X.iloc[selected_idx].reset_index(drop=True),
        y.iloc[selected_idx].reset_index(drop=True),
    )


def evaluate(
    name,
    model,
    X_train,
    y_train,
    X_val,
    y_val,
    sample_weight=None,
):
    if sample_weight is None:
        model.fit(X_train, y_train)
    else:
        model.fit(
            X_train,
            y_train,
            sample_weight=sample_weight,
        )

    probabilities = model.predict_proba(X_val)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    pr_auc = average_precision_score(
        y_val,
        probabilities,
    )

    precision = precision_score(
        y_val,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_val,
        predictions,
        zero_division=0,
    )

    print(
        f"{name:25} "
        f"PR-AUC: {pr_auc:.4f} | "
        f"Precision: {precision:.4f} | "
        f"Recall: {recall:.4f}"
    )


def main():
    df = clean_lots()

    train, validation, _ = time_split(df)

    X_train, y_train = prepare_data(train)
    X_val, y_val = prepare_data(validation)

    print("GRADIENT BOOSTING — IMBALANCE COMPARISON")
    print("-" * 70)
    print(f"Validation prevalence: {y_val.mean():.4f}")
    print()

    # 1. Leave the training data untouched.
    model = GradientBoostingClassifier(
        random_state=42,
        n_estimators=150,
        learning_rate=0.05,
        max_depth=3,
    )

    evaluate(
        "Untouched",
        model,
        X_train,
        y_train,
        X_val,
        y_val,
    )

    # 2. Give rejected lots more importance.
    weights = np.where(
        y_train.to_numpy() == 1,
        5.0,
        1.0,
    )

    model = GradientBoostingClassifier(
        random_state=42,
        n_estimators=150,
        learning_rate=0.05,
        max_depth=3,
    )

    evaluate(
        "Class weighted",
        model,
        X_train,
        y_train,
        X_val,
        y_val,
        sample_weight=weights,
    )

    # 3. Oversample rejected lots in the training data only.
    X_resampled, y_resampled = oversample_minority(
        X_train,
        y_train,
    )

    model = GradientBoostingClassifier(
        random_state=42,
        n_estimators=150,
        learning_rate=0.05,
        max_depth=3,
    )

    evaluate(
        "Oversampled",
        model,
        X_resampled,
        y_resampled,
        X_val,
        y_val,
    )


if __name__ == "__main__":
    main()