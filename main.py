from src.agent.gold_agent import GoldAgent
import os


def main():
    agent = GoldAgent()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 40)
    print("\nWelcome to the Gold Market Assistant!\n")
    print("=" * 40 + "\n")

    while True:
        answer = agent.ask(input("What information do you need about the gold market?\nYou:\n"))
        print("Agent:")

        print(answer)

if __name__ == "__main__":
    main()