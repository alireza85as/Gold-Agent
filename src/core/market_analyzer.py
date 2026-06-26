import pandas as pd


class MarketAnalyzer:
    """Analyzes market history to build a summary for the LLM."""

    def analyze_history(self, history):
        """Build a trend summary from a Yahoo price history list."""
        df = pd.DataFrame(history)
        if df.empty:
            return None

        close = df["Close"]
        current_price = float(close.iloc[-1])
        first_price = float(close.iloc[0])
        highest = float(close.max())
        lowest = float(close.min())
        change_percent = ((current_price - first_price) / first_price) * 100

        # Classify the trend based on the overall change
        if change_percent > 2:
            trend = "bullish"
        elif change_percent < -2:
            trend = "bearish"
        else:
            trend = "neutral"

        return {
            "current_price": round(current_price, 2),
            "highest_price": round(highest, 2),
            "lowest_price": round(lowest, 2),
            "period_change_percent": round(change_percent, 2),
            "trend": trend,
        }
