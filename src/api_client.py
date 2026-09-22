import requests


def fetch_daily_prices(
    symbol: str,
    api_key: str,
) -> dict:
    if not api_key:
        raise ValueError("API-nyckel saknas")

    if not symbol.strip():
        raise ValueError("Aktiesymbol saknas")

    url = "https://www.alphavantage.co/query"

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

    except requests.RequestException as error:
        raise ConnectionError(
            "Kunde inte ansluta till Alpha Vantage"
        ) from error

    try:
        data = response.json()

    except requests.exceptions.JSONDecodeError as error:
        raise ValueError(
            "API:t returnerade inte giltig JSON"
        ) from error

    if "Error Message" in data:
        raise ValueError(
            f"API-fel: {data['Error Message']}"
        )

    if "Time Series (Daily)" not in data:
        message = (
            data.get("Information")
            or data.get("Note")
            or "Okänt svar från API"
        )

        raise ValueError(
            f"Kunde inte hämta aktiedata: {message}"
        )

    return data["Time Series (Daily)"]