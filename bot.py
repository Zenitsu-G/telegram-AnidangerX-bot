import telebot
import sqlite3
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8525843502:AAG0E9Bc5Tk1RP1axTWzl0Gr7RDZgvRBi30"
ADMIN_ID = 7562283220

bot = telebot.TeleBot(TOKEN)
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def admin_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("➕ Video qo‘shish"),
        KeyboardButton("📂 Videolar"),
        KeyboardButton("📊 Statistika"),
        KeyboardButton("⬅️ Orqaga")
    )
    return kb

# 📦 DATABASE
db = sqlite3.connect("videos.db", check_same_thread=False)
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id TEXT
)
""")
db.commit()

# 🔹 Asosiy menyu
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("🎥 Videolar"),
        KeyboardButton("📤 Video qo‘shish")
    )
    return kb

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Asosiy menyu 👇",
        reply_markup=main_menu()
    )

# 🎥 Videolarni ko‘rish
@bot.message_handler(func=lambda m: m.text == "🎥 Videolar")
def show_videos(message):
    cursor.execute("SELECT file_id FROM videos")
    rows = cursor.fetchall()

    if not rows:
        bot.send_message(message.chat.id, "❌ Hozircha video yo‘q")
    else:
        for row in rows:
            bot.send_video(message.chat.id, row[0])

# 📤 Video qo‘shish (admin)
@bot.message_handler(func=lambda m: m.text == "📤 Video qo‘shish")
def add_video(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "🎥 Video yuboring")
    else:
        bot.send_message(message.chat.id, "❌ Siz admin emassiz")

# 🎥 Videoni saqlash
@bot.message_handler(content_types=['video'])
def save_video(message):
    if message.from_user.id == ADMIN_ID:
        file_id = message.video.file_id
        cursor.execute("INSERT INTO videos (file_id) VALUES (?)", (file_id,))
        db.commit()
        bot.send_message(message.chat.id, "✅ Video saqlandi")
    else:
        bot.send_message(message.chat.id, "❌ Video yuborish mumkin emas")

print(">>> Doimiy video bot ishga tushdi")
bot.infinity_polling()
