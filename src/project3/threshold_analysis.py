from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import average_precision_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


DATA_PATH = Path("data/raw/lots.csv")


def load_data():
    df = pd.read_csv(DATA_PATH)

    df["lot_weight_kg"] = pd.to_numeric(df["lot_weight_kg"], errors="coerce")
    df["defect_pct"] = pd.to_numeric(df["defect_pct"], errors="coerce")
    df["delivered_on"] = pd.to_datetime(
        df["delivered_on"], format="mixed", errors="coerce"
    )
    df["rejected"] = df["rejected"].map({"NO": 0, "YES": 1})

    df = df.drop_duplicates("lot_id")
    df = df.dropna(
        subset=[
            "delivered_on",
            "lot_weight_kg",
            "moisture_pct",
            "fermentation_days",
            "bean_count_per_100g",
            "defect_pct",
            "transport_days",
            "rejected",
        ]
    )

    df = df.sort_values("delivered_on").reset_index(drop=True)
    return df


def main():
    df = load_data()

    features = [
        "lot_weight_kg",
        "moisture_pct",
        "fermentation_days",
        "bean_count_per_100g",
        "defect_pct",
        "transport_days",
    ]

    X = df[features]
    y = df["rejected"]

    train_end = int(len(df) * 0.70)
    validation_end = int(len(df) * 0.85)

    X_train = X.iloc[:train_end]
    y_train = y.iloc[:train_end]

    X_validation = X.iloc[train_end:validation_end]
    y_validation = y.iloc[train_end:validation_end]

    model = GradientBoostingClassifier(random_state=42)
    model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_validation)[:, 1]

    print("STAGE C — THRESHOLD ANALYSIS")
    print("-" * 50)
    print(f"Validation prevalence: {y_validation.mean():.4f}")
    print(f"PR-AUC: {average_precision_score(y_validation, probabilities):.4f}")
    print()
    print("Threshold | Precision | Recall")
    print("-" * 35)

    results = []

    for threshold in np.arange(0.10, 0.91, 0.05):
        predictions = (probabilities >= threshold).astype(int)

        precision = precision_score(
            y_validation, predictions, zero_division=0
        )
        recall = recall_score(
            y_validation, predictions, zero_division=0
        )

        results.append(
            {
                "threshold": threshold,
                "precision": precision,
                "recall": recall,
            }
        )

        print(
            f"{threshold:9.2f} | "
            f"{precision:9.4f} | "
            f"{recall:6.4f}"
        )

    result_df = pd.DataFrame(results)

    result_df.to_csv(
        "docs/project3/threshold_results.csv",
        index=False,
    )


if __name__ == "__main__":
    main()