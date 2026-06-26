from src.apis.yahoo_api import YahooFinanceAPI
from src.core.market_analyzer import MarketAnalyzer


yahoo = YahooFinanceAPI("GC=F")


data = yahoo.get_market_data()


analyzer = MarketAnalyzer()
summary = analyzer.analyze_history(data["history"])


print(summary)
