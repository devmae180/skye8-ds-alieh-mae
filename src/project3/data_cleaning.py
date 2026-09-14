from pathlib import Path

import pandas as pd


RAW_DIR = Path("data/raw")


def clean_lots() -> pd.DataFrame:
    lots = pd.read_csv(RAW_DIR / "lots.csv")
    cooperatives = pd.read_csv(RAW_DIR / "cooperatives.csv")

    # Parse the mixed date formats supplied in the raw data.
    lots["delivered_on"] = pd.to_datetime(
        lots["delivered_on"],
        format="mixed",
        errors="coerce",
    )

    # Clean numeric fields that may contain formatting characters or units.
    lots["lot_weight_kg"] = pd.to_numeric(
        lots["lot_weight_kg"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.extract(r"([-+]?\d*\.?\d+)")[0],
        errors="coerce",
    )

    lots["defect_pct"] = pd.to_numeric(
        lots["defect_pct"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.extract(r"([-+]?\d*\.?\d+)")[0],
        errors="coerce",
    )

    lots["moisture_pct"] = pd.to_numeric(
        lots["moisture_pct"], errors="coerce"
    )
    lots["fermentation_days"] = pd.to_numeric(
        lots["fermentation_days"], errors="coerce"
    )
    lots["bean_count_per_100g"] = pd.to_numeric(
        lots["bean_count_per_100g"], errors="coerce"
    )
    lots["transport_days"] = pd.to_numeric(
        lots["transport_days"], errors="coerce"
    )

    lots["rejected"] = (
        lots["rejected"]
        .astype(str)
        .str.strip()
        .str.upper()
        .map({"YES": 1, "NO": 0})
    )

    # Remove duplicate lot IDs, retaining the first recorded delivery.
    lots = lots.drop_duplicates(subset="lot_id", keep="first")

    # Remove lots referring to cooperatives absent from the register.
    valid_cooperatives = set(cooperatives["cooperative_id"])
    lots = lots[lots["cooperative_id"].isin(valid_cooperatives)].copy()

    required = [
        "lot_id",
        "cooperative_id",
        "delivered_on",
        "lot_weight_kg",
        "moisture_pct",
        "fermentation_days",
        "bean_count_per_100g",
        "defect_pct",
        "rejected",
    ]

    lots = lots.dropna(subset=required).copy()

    # Add cooperative attributes.
    lots = lots.merge(
        cooperatives,
        on="cooperative_id",
        how="left",
        validate="many_to_one",
    )

    return lots.sort_values("delivered_on").reset_index(drop=True)


def time_split(
    lots: pd.DataFrame,
    train_fraction: float = 0.70,
    validation_fraction: float = 0.15,
):
    """Split chronologically so future deliveries are never used for training."""
    n = len(lots)

    train_end = int(n * train_fraction)
    validation_end = int(n * (train_fraction + validation_fraction))

    train = lots.iloc[:train_end].copy()
    validation = lots.iloc[train_end:validation_end].copy()
    final_test = lots.iloc[validation_end:].copy()

    return train, validation, final_test


if __name__ == "__main__":
    df = clean_lots()
    train, validation, final_test = time_split(df)

    print(f"Cleaned rows: {len(df):,}")
    print(f"Rejected: {df['rejected'].sum():,}")
    print(f"Prevalence: {df['rejected'].mean():.2%}")
    print(
        f"Date range: {df['delivered_on'].min().date()} "
        f"to {df['delivered_on'].max().date()}"
    )

    print("\nTIME SPLIT")
    print(
        f"Train: {len(train):,} | "
        f"{train.delivered_on.min().date()} to "
        f"{train.delivered_on.max().date()}"
    )
    print(
        f"Validation: {len(validation):,} | "
        f"{validation.delivered_on.min().date()} to "
        f"{validation.delivered_on.max().date()}"
    )
    print(
        f"Final test: {len(final_test):,} | "
        f"{final_test.delivered_on.min().date()} to "
        f"{final_test.delivered_on.max().date()}"
    )