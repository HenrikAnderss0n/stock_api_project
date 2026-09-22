from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_price_chart(
    df: pd.DataFrame,
    symbol: str,
    output_path: Path,
) -> None:
    plt.figure(figsize=(10, 5))

    plt.plot(
        df["date"],
        df["close"],
    )

    plt.title(
        f"{symbol} - daglig stängningskurs"
    )

    plt.xlabel("Datum")
    plt.ylabel("Stängningskurs (USD)")

    plt.tight_layout()

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.savefig(
        output_path,
        dpi=150,
    )

    plt.close()