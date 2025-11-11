import telebot
from collections import deque
import os

# ✅ Load your bot token (use environment variable on Render for security)
BOT_TOKEN = os.getenv("BOT_TOKEN", "7677423658:AAH-F8AP6XoZrleihOjjAXROzEEp-mq7_xA")

# ✅ Create the bot instance correctly
bot = telebot.TeleBot(BOT_TOKEN)

# Store the last 5 predictions
prediction_history = deque(maxlen=5)

def modular_base_prediction(period_last3):
    num = int(period_last3)
    mod = num % 10
    return "SMALL" if mod <= 4 else "BIG"

def ai_trend_adjusted_prediction(period_last3):
    base_prediction = modular_base_prediction(period_last3)
    if len(prediction_history) >= 3:
        big_count = prediction_history.count("BIG")
        small_count = prediction_history.count("SMALL")
        if big_count > small_count + 2 and base_prediction == "BIG":
            adjusted = "SMALL"
        elif small_count > big_count + 2 and base_prediction == "SMALL":
            adjusted = "BIG"
        else:
            adjusted = base_prediction
    else:
        adjusted = base_prediction
    prediction_history.append(adjusted)
    return adjusted

@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, "🔮 Wingo AI Modular Trend Bot Online!\nSend last 3 digits to get prediction.")

@bot.message_handler(func=lambda m: True)
def handle_message(msg):
    text = msg.text.strip()
    if len(text) == 3 and text.isdigit():
        result = ai_trend_adjusted_prediction(text)
        bot.reply_to(msg, f"🧮 Period {text} → Prediction: {result}")
    else:
        bot.reply_to(msg, "⚠️ Please send exactly 3 digits (e.g. 123).")

if __name__ == "__main__":
    print("🤖 Bot is running on Render...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

