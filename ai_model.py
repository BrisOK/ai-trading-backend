from typing import Literal, Tuple
import yfinance as yf
import requests

MarketType = Literal["stock", "crypto"]


def _stock_closes(symbol: str, limit: int = 10) -> list[float]:
        """
        Get last `limit` daily close prices for a stock using Yahoo Finance.
        """
        data = yf.download(symbol, period="1mo", interval="1d", progress=False)
        if data.empty:
                return []
        closes = data["Close"].tail(limit)
        return list(closes)


def _crypto_closes(symbol: str, limit: int = 10) -> list[float]:
        """
        Get last `limit` daily close prices for a crypto using Binance.

        Example symbols:
            - BTCUSDT
            - ETHUSDT
        """
        base_url = "https://api.binance.com"
        url = f"{base_url}/api/v3/klines"
        params = {
                "symbol": symbol.upper(),
                "interval": "1d",
                "limit": limit,
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data:
                return []
        closes = [float(candle[4]) for candle in data]    # index 4 = close price
        return closes


def get_signal_for_symbol(
        symbol: str,
        market: MarketType = "stock",
) -> Tuple[float, Literal["buy", "sell", "hold"]]:
        """
        Simple moving-average-based demo strategy.

        - If last price > moving average → 'buy'
        - If last price  < moving average → 'sell'
        - Else → 'hold'

        NOTE: Demo only. NOT financial advice.
        """

        if market == "crypto":
                closes = _crypto_closes(symbol, 10)
        else:
                closes = _stock_closes(symbol, 10)

        if not closes or len(closes)  < 5:
                return 0.0, "hold"

        last_price = closes[-1]
        ma = sum(closes) / len(closes)

        diff = last_price - ma
        score = float(diff / ma)    # relative distance

        if score > 0.01:
                rec = "buy"
        elif score  < -0.01:
                rec = "sell"
        else:
                rec = "hold"

        return score, rec