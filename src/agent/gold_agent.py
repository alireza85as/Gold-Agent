from src.core.prompt_builder import PromptBuilder
from src.llm.llm_manager import LLMManager
from src.core.market_manager import MarketDataManager
from src.apis.tavily_api import TavilyNewsAPI
from src.memory.chat_memory import ChatMemory


class GoldAgent:
    """ A specialized AI agent for providing gold market insights and analysis."""

    def __init__(self):
        self.llm = LLMManager()
        self.prompt_builder = PromptBuilder()
        self.manager = MarketDataManager()
        self.news = TavilyNewsAPI()
        self.memory = ChatMemory()

    def ask(self, question):
        market_data = self.manager.get_market_context()
        news_summary = self.news.summarize()
        chat_history = self.memory.get_history()

        # build a structured prompt with all context
        prompt = self.prompt_builder.build(
            user_question=question,
            market_context=market_data,
            news_summary=news_summary,
            chat_history=chat_history,
        )
        # print(prompt)
        response = self.llm.generate(prompt)

        self.memory.save(question, response)
        # print(chat_history)

        # print()
        return response + "\n"
