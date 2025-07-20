import time
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from telegram import Bot

# === НАСТРОЙКИ ===
BOT_TOKEN = "7531307637:AAE66Yu_TOQV6TegAamJ8QWVkX5Q_xFzRHk"
CHAT_ID = 612299504
SPREAD_LIMIT = 2.0  # пока оставим 0.0 для проверки
CHECK_INTERVAL = 60

# === НАСТРОЙКА CHROMEDRIVER ===
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service("C:/selenium/driver/chromedriver.exe")  # Укажи здесь свой путь!
driver = webdriver.Chrome(service=service, options=chrome_options)
bot = Bot(token=BOT_TOKEN)

# === ФУНКЦИЯ ПРОВЕРКИ ===
def get_spreads():
    url = "https://uainvest.com.ua/arbitrage?type=spread&exchanges=whitebit_mexc_okx_bybit_bitget_gate_binance"
    driver.get(url)
    time.sleep(5)

    rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
    result = []

    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, 'td')
            name = cells[0].text.strip()
            spread_text = cells[-1].text.strip().replace('%', '').replace(',', '.')
            spread = float(spread_text)
            if spread >= SPREAD_LIMIT:
                result.append((name, spread))
        except:
            continue

    return result

# === АСИНХРОННЫЙ ЦИКЛ ===
async def main_loop():
    print("Бот запущен. Проверка раз в минуту.")
    while True:
        try:
            found = get_spreads()
            if found:
                message = "🔔 Найдены спреды выше 2%:\n\n"
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
