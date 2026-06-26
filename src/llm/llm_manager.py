import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

CONFIG_PATH = "config/llm_config.json"


class LLMManager:
    def __init__(self):
        self.providers = self.load_config()

    def load_config(self):
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            config = json.load(file)

        providers = [p for p in config.get("providers", []) if p.get("enabled", True)]

        providers.sort(key=lambda x: x.get("priority", 999))
        return providers

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048):
        """
        Tries each provider until one succeeds
        """

        for provider in self.providers:
            # print(f"Trying {provider['name']}...")

            result = self.send_request(provider, prompt, temperature, max_tokens)

            if result:
                # print(f"Success with {provider['name']}")
                return result

            # print(f"Failed {provider['name']}")

        print("All providers failed")
        return None

    def send_request(self, provider, prompt, temperature, max_tokens):
        try:
            api_key = os.getenv(provider["key"])
            if not api_key:
                print(f"API Key not found: {provider['key']}")
                return None

            if provider["type"] == "openai":
                return self._openai_request(provider, prompt, temperature, max_tokens)
            elif provider["type"] == "gemini":
                return self._gemini_request(provider, prompt, temperature, max_tokens)
            else:
                print(f"Unknown provider typee: {provider['type']}")
                return None

        except Exception as e:
            # print(f"Error with {provider['name']}: {e}")
            return None

    # ====================== OPENAI ====================
    def _openai_request(self, provider, prompt, temperature, max_tokens):
        response = requests.post(
            provider["url"],
            headers={
                "Authorization": f"Bearer {os.getenv(provider['key'])}",
                "Content-Type": "application/json",
            },
            json={
                "model": provider["model"],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
            timeout=40,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    # ====================== GEMINI ======================
    def _gemini_request(self, provider, prompt, temperature, max_tokens):
        url = f"{provider['url']}?key={os.getenv(provider['key'])}"

        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens,
                },
            },
            timeout=40,
        )
        response.raise_for_status()
        data = response.json()

        if "candidates" in data and data["candidates"]:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()

        return None
