import requests
import time


class TGJUAPI:
    # Client for fetching raw market data from the TGJU API.

    def __init__(self, api_urls):
        self.api_urls = api_urls

    def get_data(self):
        """
        Fetch raw data from TGJU.
        Tries each URL in order, retrying up to 3 times if all fail.
        """

        max_attempts = 3
        attempt = 0

        while attempt < max_attempts:
            attempt += 1

            for url in self.api_urls:
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    # print(response.json())

                    return response.json()

                except Exception as error:
                    continue

            print(f"All URLs failed in attempt {attempt}")

            if attempt < max_attempts:
                time.sleep(2)

        print("All attempts failed. No data received.")
        return None


class TGJUParser:
    """Converts raw TGJU data into a clean dict for the agent."""

    def __init__(self, data):
        self.data = data.get("current", {})

    def get_price(self, key):
        """Read a price field and convert it to a float."""
        try:
            price = self.data[key]["p"]
            price = price.replace(",", "")
            return float(price)

        except Exception as error:
            print(f"Error reading {key}: {error}")
            return None

    def parse(self):
        """Return the set of market prices used by the agent."""
        return {
            "Dollar price to Rial": self.get_price("price_dollar_rl"),
            "usdt price to rial": self.get_price("usdt-irr"),
            "gold_18k price to rial": self.get_price("tgju_gold_irg18"),
            "melted_gold price to rial": self.get_price("mesghal"),
            "xaut price to dollar": self.get_price("tether_gold_xaut"),
            "Oil Brent price to Dollar": self.get_price("oil_brent"),
            "Oil WTI price to Dollar": self.get_price("oil"),
            "Gold to Oil ratio": self.get_price("ratio_crudeoil"),
        }
