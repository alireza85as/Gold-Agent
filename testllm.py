from src.llm.llm_manager import LLMManager



llm = LLMManager()

prompt = """
به صورت کوتاه توضیح بده چه عواملی باعث افزایش قیمت طلا می‌شوند؟
"""

response = llm.generate(prompt)

print(response)