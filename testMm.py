from src.core.market_manager import MarketDataManager

manager = MarketDataManager()
market = manager.get_market_context()
print(market)
