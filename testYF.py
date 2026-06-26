from src.apis.yahoo_api import YahooFinanceAPI


yahoo = YahooFinanceAPI("GC=F")
data = yahoo.get_market_data()


print(data)
