import yfinance as yf
from datetime import datetime


class YahooFinanceAPI:
    """Fetches global market data (gold futures) from Yahoo Finance."""

    def __init__(self, symbol):
        self.symbol = symbol

    def get_market_data(self):
        """Return today's price snapshot plus 6-month history for analysis."""
        try:
            ticker = yf.Ticker(self.symbol)
            # Today's snapshot
            daily = ticker.history(period="1d")
            # History used for trend analysis
            history = ticker.history(period="6mo")

            latest = daily.iloc[-1]
            close_price = float(latest["Close"])
            open_price = float(latest["Open"])
            high_price = float(latest["High"])
            low_price = float(latest["Low"])
            volume = int(latest["Volume"])

            change_percent = ((close_price - open_price) / open_price) * 100

            return {
                "symbol": self.symbol,
                "price": close_price,
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "volume": volume,
                "change_percent": round(change_percent, 2),
                "history": history.reset_index().to_dict("records"),
                "timestamp": datetime.now(),
            }
        except Exception as error:
            print(f"Yahoo Error: {error}")
            return None
