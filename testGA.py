from src.agent.gold_agent import GoldAgent


agent = GoldAgent()


# market_data = {
#     "dollar": "1,578,000 تومان",
#     "gold_18k": "160,221,000 تومان",
#     "gold_ounce": "4182 دلار",
#     "trend": "صعودی",
# }


answer = agent.ask(
    "قیمت نفت چند ریاله؟"
)


print("\n--- Agent Answer ---\n")

print(answer)
