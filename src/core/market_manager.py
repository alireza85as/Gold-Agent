from src.apis.tgju_api import TGJUAPI, TGJUParser
from src.apis.yahoo_api import YahooFinanceAPI
from .market_analyzer import MarketAnalyzer


class MarketDataManager:
    """Coordinates all market data sources."""

    def __init__(self):
        # TGJU provides Iran/oil market data with multiple fallback URLs
        self.tgju = TGJUAPI(
            [
                "https://call2.tgju.org/ajax.json",
                "https://call3.tgju.org/ajax.json",
                "https://call4.tgju.org/ajax.json",
            ]
        )

        # GC=F is the gold futures symbol on Yahoo Finance
        self.yahoo = YahooFinanceAPI("GC=F")
        self.analyzer = MarketAnalyzer()

    def get_market_context(self):
        """Collect and combine data from all sources into one context dict."""
        context = {}

        # Iran + oil market from TGJU
        tgju_data = self.tgju.get_data()
        if tgju_data:
            parser = TGJUParser(tgju_data)
            context["iran_and_oil_market"] = parser.parse()

        # Global gold + technical analysis from Yahoo
        yahoo_data = self.yahoo.get_market_data()
        if yahoo_data:
            context["global_gold"] = {
                "price": yahoo_data["price"],
                "open": yahoo_data["open"],
                "high": yahoo_data["high"],
                "low": yahoo_data["low"],
                "volume": yahoo_data["volume"],
            }

            context["technical_analysis"] = self.analyzer.analyze_history(
                yahoo_data["history"]
            )

        return context
