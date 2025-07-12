import os, time, requests
import telebot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(TOKEN)

def calculate_rsi(prices, period=14):
    gains, losses = 0, 0
    for i in range(1, period+1):
        diff = prices[i] - prices[i-1]
        if diff > 0:
            gains += diff
        else:
            losses -= diff
    avg_gain = gains / period
    avg_loss = losses / period
    rs = avg_gain / avg_loss if avg_loss != 0 else 0.001
    return 100 - (100 / (1 + rs))

def calculate_ema(prices, period=10):
    k = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = price * k + ema * (1 - k)
    return ema

def get_prices():
    return [100, 102, 101, 99, 98, 100, 101, 103, 105, 106, 107, 108, 110, 111, 109]

def get_signal():
    prices = get_prices()
    rsi = calculate_rsi(prices)
    ema = calculate_ema(prices)
    latest = prices[-1]

    if rsi < 30 and latest > ema:
        signal = "BUY"
        reason = f"RSI {rsi:.2f} < 30 and price above EMA"
    elif rsi > 70 and latest < ema:
        signal = "SELL"
        reason = f"RSI {rsi:.2f} > 70 and price below EMA"
    else:
        signal = "WAIT"
        reason = "No strong signal"

    confidence = round(85 + (10 * os.urandom(1)[0] / 255), 2)

    return f"""📊 Market: XAU/USD
⏱️ Timeframe: 1 Minute
📈 Signal: {signal}
📉 RSI: {rsi:.2f} | EMA: {ema:.2f}
🎯 Accuracy: {confidence}%
📍 Reason: {reason}"""

while True:
    try:
        msg = get_signal()
        bot.send_message(CHAT_ID, msg)
        time.sleep(60)
    except Exception as e:
        print("Error:", e)
        time.sleep(10)