import pandas as pd


EXPECTED_COLUMNS = {
    "1. open",
    "2. high",
    "3. low",
    "4. close",
    "5. volume",
}


def create_price_dataframe(
    time_series: dict,
) -> pd.DataFrame:
    if not time_series:
        raise ValueError("Tidsserien är tom")

    df = pd.DataFrame.from_dict(
        time_series,
        orient="index",
    )

    missing_columns = EXPECTED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            "API-datan saknar förväntade kolumner: "
            + ", ".join(sorted(missing_columns))
        )

    df = df.rename(
        columns={
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume",
        }
    )

    df.index.name = "date"
    df = df.reset_index()

    df["date"] = pd.to_datetime(df["date"])

    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    df[numeric_columns] = df[numeric_columns].apply(
        pd.to_numeric
    )

    required_columns = ["date", *numeric_columns]

    if df[required_columns].isna().any().any():
        raise ValueError(
            "API-datan innehåller saknade datum "
            "eller numeriska värden"
        )
    
    df = df.sort_values("date").reset_index(drop=True)

    return df