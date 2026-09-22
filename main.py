import os
from pathlib import Path

from dotenv import load_dotenv

from src.analysis import summarize_prices
from src.api_client import fetch_daily_prices
from src.processing import create_price_dataframe
from src.visualization import save_price_chart


def main() -> None:
    load_dotenv()

    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    symbol = "IBM"

    try:
        time_series = fetch_daily_prices(
            symbol=symbol,
            api_key=api_key,
        )

        df = create_price_dataframe(time_series)

        data_path = (
            Path("data")
            / f"{symbol.lower()}_daily_prices.csv"
        )

        data_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_csv(
            data_path,
            index=False,
        )

        summary = summarize_prices(df)

        print(
            f"Period: "
            f"{summary['first_date'].date()} till "
            f"{summary['last_date'].date()}"
        )

        print(
            f"Första stängningskurs: "
            f"{summary['first_close']:.2f}"
        )

        print(
            f"Senaste stängningskurs: "
            f"{summary['last_close']:.2f}"
        )

        print(
            f"Högsta stängningskurs: "
            f"{summary['highest_close']:.2f}"
        )

        print(
            f"Lägsta stängningskurs: "
            f"{summary['lowest_close']:.2f}"
        )

        print(
            f"Förändring: "
            f"{summary['percentage_change']:.2f} %"
        )

        chart_path = (
            Path("output")
            / f"{symbol.lower()}_price_chart.png"
        )

        save_price_chart(
            df=df,
            symbol=symbol,
            output_path=chart_path,
        )

        print(f"Graf sparad: {chart_path}")
        print(f"Data sparad: {data_path}")

    except (ValueError, ConnectionError) as error:
        print(f"Fel: {error}")


if __name__ == "__main__":
    main()