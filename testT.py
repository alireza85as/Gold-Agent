from src.apis.tavily_api import TavilyNewsAPI


news = TavilyNewsAPI()


result = news.summarize()
print(result)
