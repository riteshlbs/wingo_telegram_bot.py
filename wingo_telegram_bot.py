# =========================================================
# 🤖 WINGO MODULAR + AI TREND TELEGRAM BOT
# Logic: Modular Prediction (0–4 = SMALL, 5–9 = BIG)
# AI Trend Adjustment Based on Last 5 Predictions
# =========================================================

import telebot
from collections import deque
import os

# 🔐 Secure Token Handling
BOT_TOKEN = os.getenv("BOT_TOKEN", "7677423658:AAH-F8AP6XoZrleihOjjAXROzEEp-mq7_xA")

# Initialize bot
bot = telebot.TeleBot("7677423658:AAH-F8AP6XoZrleihOjjAXROzEEp-mq7_xA")

# Store the last 5 results for trend balancing
prediction_history = deque(maxlen=5)

# =========================================================
# ⚙️ CORE MODULAR LOGIC
# =========================================================
def modular_base_prediction(period_last3):
    """
    Basic modular logic for Wingo:
    - 0–4 → SMALL
    - 5–9 → BIG
    """
    num = int(period_last3)
    mod = num % 10
    return "SMALL" if mod <= 4 else "BIG"

# =========================================================
# 🧠 AI TREND-ADJUSTED LOGIC
# =========================================================
def ai_trend_adjusted_prediction(period_last3):
    base_prediction = modular_base_prediction(period_last3)

    if len(prediction_history) >= 3:
        big_count = prediction_history.count("BIG")
        small_count = prediction_history.count("SMALL")

        # Trend adjustment logic
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

# =========================================================
# 💬 TELEGRAM COMMAND HANDLERS
# =========================================================
@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(
        msg,
        "🔮 *Wingo AI Modular Trend Bot Online!*\n\n"
        "Send the *last 3 digits* of the period number to get a prediction.\n\n"
        "Logic: `0–4 → SMALL`, `5–9 → BIG`.\n"
        "AI also adjusts based on recent trend history.",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: True)
def handle_message(msg):
    text = msg.text.strip()

    # Validate input
    if len(text) == 3 and text.isdigit():
        result = ai_trend_adjusted_prediction(text)
        bot.reply_to(
            msg,
            f"🧮 Period `{text}` → *{result}*\n📊 Trend: {list(prediction_history)}",
            parse_mode="Markdown"
        )
    else:
        bot.reply_to(msg, "⚠️ Please send exactly *3 digits* (e.g. 123).", parse_mode="Markdown")

# =========================================================
# 🚀 BOT EXECUTION
# =========================================================
if __name__ == "__main__":
    print("🤖 Wingo Modular Bot is running on Render...")
    bot.infinity_polling(timeout=60, long_polling_timeout=20)
