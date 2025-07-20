import requests
from bs4 import BeautifulSoup
import time
import asyncio
from telegram import Bot

BOT_TOKEN = "7531307637:AAE66Yu_TOQV6TegAamJ8QWVkX5Q_xFzRHk"
CHAT_ID = 612299504
SPREAD_LIMIT = 1.0  # понижен для теста
CHECK_INTERVAL = 60

bot = Bot(token=BOT_TOKEN)

def get_spreads():
    url = "https://uainvest.com.ua/arbitrage?type=spread&exchanges=whitebit_mexc_okx_bybit_bitget_gate_binance"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    print("HTML длина:", len(response.text))

    table = soup.find("table")
    if not table:
        print("Таблица не найдена!")
        return []

    rows = table.find("tbody").find_all("tr")
    print("Найдено строк:", len(rows))

    result = []
    for row in rows:
        cols = row.find_all("td")
        if not cols or len(cols) < 6:
            continue

        name = cols[0].text.strip()
        spread_str = cols[-1].text.strip().replace('%', '').replace(',', '.')
        try:
            spread = float(spread_str)
            if spread >= SPREAD_LIMIT:
                result.append((name, spread))
        except:
            continue

    return result

async def main_loop():
    print("Бот запущен на Railway.")
    while True:
        try:
            found = get_spreads()
            if found:
                message = f"🔔 Найдены спреды выше {SPREAD_LIMIT}%:\n\n"
                message += "\n".join([f"{name}: {spread:.2f}%" for name, spread in found])
                await bot.send_message(chat_id=CHAT_ID, text=message)
                print("Сообщение отправлено.")
            else:
                print("Ничего не найдено.")
        except Exception as e:
            print("Ошибка:", e)

        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main_loop())

if __name__ == "__main__":
    asyncio.run(main_loop())
