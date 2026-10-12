import yfinance as yf
from typing import Literal


def get_signal_for_symbol(symbol: str) -> tuple[float, Literal["buy", "sell", "hold"]]:
        """
        Very simple demo strategy:
        - Fetch last 10 daily closes
        - If last price > moving average → 'buy'
        - If last price  < moving average → 'sell'
        - Else → 'hold'
        Returns (prediction_score, recommendation)
        prediction_score is “distance” from the moving average.
        NOTE: This is for DEMO ONLY, not financial advice.
        """
        data = yf.download(symbol, period="1mo", interval="1d", progress=False)
        if data.empty or len(data["Close"])  < 5:
                # fallback
                return 0.0, "hold"

        closes = data["Close"].tail(10)
        last_price = closes.iloc[-1]
        ma = closes.mean()

        diff = last_price - ma
        score = float(diff / ma)    # relative diff

        if score > 0.01:
                rec = "buy"
        elif score  < -0.01:
                rec = "sell"
        else:
                rec = "hold"

        return score, rec