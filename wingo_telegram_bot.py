# =========================================================
# 🤖 WINGO AI MODULAR TREND BOT
# Logic: Modular + Simple AI Trend Adjustment
# Author: Ritesh Verma
# =========================================================

import telebot
from collections import deque
import os

# ================================
# 🔐 Secure BOT Token Management
# ================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "7677423658:AAH-F8AP6XoZrleihOjjAXROzEEp-mq7_xA")
bot = telebot.TeleBot(7677423658:AAH-F8AP6XoZrleihOjjAXROzEEp-mq7_xA)

# Store last 5 predictions for trend learning
prediction_history = deque(maxlen=5)

# ================================
# ⚙️ Core Modular Logic
# ================================
def modular_base_prediction(period_last3):
    """
    Basic modular arithmetic logic:
    - 0–4 → SMALL
    - 5–9 → BIG
    """
    num = int(period_last3)
    mod = num % 10
    return "SMALL" if mod <= 4 else "BIG"

# ================================
# 🧠 AI Trend Adjustment
# ================================
def ai_trend_adjusted_prediction(period_last3):
    base_prediction = modular_base_prediction(period_last3)

    if len(prediction_history) >= 3:
        big_count = prediction_history.count("BIG")
        small_count = prediction_history.count("SMALL")

        # Trend balancing logic
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

# ================================
# 💬 Telegram Bot Handlers
# ================================
@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(
        msg,
        "🔮 *Wingo AI Modular Bot Online!*\n\n"
        "Send last 3 digits of the period number to get a prediction.\n\n"
        "Logic: `0–4 → SMALL`, `5–9 → BIG`",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: True)
def handle_message(msg):
    text = msg.text.strip()
    if len(text) == 3 and text.isdigit():
        result = ai_trend_adjusted_prediction(text)
        bot.reply_to(
            msg,
            f"🧮 Period `{text}` → Prediction: *{result}*\n📊 Trend: {list(prediction_history)}",
            parse_mode="Markdown"
        )
    else:
        bot.reply_to(msg, "⚠️ Please send exactly *3 digits* (e.g. 123).", parse_mode="Markdown")

# ================================
# 🚀 Bot Runner
# ================================
if __name__ == "__main__":
    print("🤖 Wingo Modular Bot is running...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
