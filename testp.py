from src.core.prompt_builder import PromptBuilder


market = {"gold_18k": 160221000, "dollar": 1578000, "ounce": 4182, "trend": "bullish"}


builder = PromptBuilder()
prompt = builder.build("آیا الان خرید طلا خوب است؟", market, "",[])


print(prompt)
