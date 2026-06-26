import os
from dotenv import load_dotenv
from tavily import TavilyClient
from src.llm.llm_manager import LLMManager

load_dotenv()


class TavilyNewsAPI:
    """Fetches gold market news via Tavily and summarizes it with an LLM."""
    def __init__(self):
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self.llm = LLMManager()

    def search_news(self, query):
        """Search Tavily for news matching the query."""
        try:
            return self.tavily_client.search(
                query=query, search_depth="advanced", topic="news", max_results=5
            )
        except Exception as error:
            print(error)
            return None

    def summarize(self, query=None):
        """Run a news search and return an LLM-generated summary."""
        if not query:
            query = "gold price XAU/USD analysis Federal Reserve interest rates inflation geopolitical risks"

        data = self.search_news(query)

        if data and "results" in data:
            # Keep the 5 most relevant results by Tavily score
            news_data = sorted(
                data["results"], key=lambda x: x.get("score", 0), reverse=True
            )[:5]
        else:
            return "No news found"

        # Combine all news titles and content into one block
        combined_text = ""
        for item in news_data:
            title = item.get("title", "")
            content = item.get("content", "")
            combined_text += f"Title: {title}\nContent: {content}\n\n"

        if not combined_text.strip():
            return "No content to summarize"

        # Prompt asking the LLM to summarize the gold market news
        prompt = f"""
        You are a financial analyst.

        Summarize these gold market news in 150-200 words.

        Requirements:
        - Explain gold market impact.
        - Mention USD, Fed, inflation, and geopolitics.
        - Include expert forecasts if available.
        - Do not invent prices or data.
        - End with a clear conclusion.

        News:
        {combined_text}

        Summary:
        """

        try:
            summary = self.llm.generate(prompt, temperature=0.3)
            if summary:
                # print(summary)
                return summary
            else:
                return "Failed to generate summary"
        except Exception as e:
            # Fall back to raw text if summarization fails
            print(f"Summarization error: {e}")
            return combined_text[:500] + "..."
