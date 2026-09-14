from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import brier_score_loss

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


def main():
    df = clean_lots()

    train, validation, _ = time_split(df)

    X_train, y_train = prepare_data(train)
    X_val, y_val = prepare_data(validation)

    base_model = GradientBoostingClassifier(
        random_state=42,
        n_estimators=150,
        learning_rate=0.05,
        max_depth=3,
    )

    # Raw model
    base_model.fit(X_train, y_train)

    raw_probabilities = base_model.predict_proba(X_val)[:, 1]

    raw_brier = brier_score_loss(
        y_val,
        raw_probabilities,
    )

    # Calibrated model
    calibrated_model = CalibratedClassifierCV(
        estimator=GradientBoostingClassifier(
            random_state=42,
            n_estimators=150,
            learning_rate=0.05,
            max_depth=3,
        ),
        method="sigmoid",
        cv=5,
    )

    calibrated_model.fit(X_train, y_train)

    calibrated_probabilities = calibrated_model.predict_proba(
        X_val
    )[:, 1]

    calibrated_brier = brier_score_loss(
        y_val,
        calibrated_probabilities,
    )

    print("CALIBRATION RESULTS")
    print("-" * 45)
    print(f"Raw Brier score:        {raw_brier:.4f}")
    print(f"Calibrated Brier score: {calibrated_brier:.4f}")

    if calibrated_brier < raw_brier:
        print("Calibration improved the Brier score.")
    else:
        print("Calibration did not improve the Brier score.")


if __name__ == "__main__":
    main()