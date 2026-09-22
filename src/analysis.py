import pandas as pd


def summarize_prices(
    df: pd.DataFrame,
) -> dict:
    first_date = df.iloc[0]["date"]
    last_date = df.iloc[-1]["date"]

    first_close = df.iloc[0]["close"]
    last_close = df.iloc[-1]["close"]

    highest_close = df["close"].max()
    lowest_close = df["close"].min()

    percentage_change = (
        (last_close - first_close) / first_close
    ) * 100

    return {
        "first_date": first_date,
        "last_date": last_date,
        "first_close": first_close,
        "last_close": last_close,
        "highest_close": highest_close,
        "lowest_close": lowest_close,
        "percentage_change": percentage_change,
    }