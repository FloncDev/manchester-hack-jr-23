from dotenv import dotenv_values, find_dotenv
import aiohttp

env = dotenv_values(find_dotenv())
api_key, secret_key = env["ALPACA_API_KEY"], env["ALPACA_API_SECRET"]
if None in [api_key, secret_key]:
    raise Exception("ALPACA_API_KEY or ALPACA_API_SECRET are not set.")

headers = {"APCA-API-KEY-ID": api_key, "APCA-API-SECRET-KEY": secret_key}


async def get_stock_price(listing: str) -> float:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://data.alpaca.markets/v2/stocks/{listing}/bars/latest",
            headers=headers,
        ) as resp:
            data = await resp.json()

            return data["bar"]["c"]  # Closing price


async def get_news():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://data.alpaca.markets/v1beta1/news", headers=headers
        ) as resp:
            data = await resp.json()

            headlines = []

            for news in data["news"]:
                headlines.append(news["headline"])

            return headlines
