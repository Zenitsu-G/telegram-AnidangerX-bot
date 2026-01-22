import telebot
import sqlite3
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ================== SOZLAMALAR ==================
TOKEN = "8525843502:AAH82QJd6r32mNnUE1VCbkiJn3CWxdnGWJs"
ADMIN_ID = 7562283220

bot = telebot.TeleBot(TOKEN)

# ================== DATABASE ==================
db = sqlite3.connect("videos.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id TEXT
)
""")
db.commit()

# ================== MENYULAR ==================
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("📂 Videolar")
    )
    return kb


def admin_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("➕ Video qo‘shish"),
        KeyboardButton("📂 Videolar"),
        KeyboardButton("📊 Statistika"),
        KeyboardButton("⬅️ Orqaga")
    )
    return kb

# ================== START ==================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Asosiy menyu 👇",
        reply_markup=main_menu()
    )

# ================== ADMIN PANEL ==================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(
            message.chat.id,
            "👑 Admin panel",
            reply_markup=admin_menu()
        )
    else:
        bot.send_message(
            message.chat.id,
            "⛔ Siz admin emassiz"
        )

# ================== VIDEO QO‘SHISH (ADMIN) ==================
@bot.message_handler(func=lambda m: m.text == "➕ Video qo‘shish")
def add_video_step(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.send_message(message.chat.id, "🎥 Video yuboring")

@bot.message_handler(content_types=['video'])
def save_video(message):
    if message.from_user.id != ADMIN_ID:
        return

    file_id = message.video.file_id
    cursor.execute("INSERT INTO videos (file_id) VALUES (?)", (file_id,))
    db.commit()

    bot.send_message(message.chat.id, "✅ Video saqlandi")

# ================== VIDEO RO‘YXATI ==================
@bot.message_handler(func=lambda m: m.text == "📂 Videolar")
def show_videos(message):
    cursor.execute("SELECT file_id FROM videos")
    rows = cursor.fetchall()

    if not rows:
        bot.send_message(message.chat.id, "❌ Hozircha video yo‘q")
        return

    for row in rows:
        bot.send_video(message.chat.id, row[0])

# ================== STATISTIKA ==================
@bot.message_handler(func=lambda m: m.text == "📊 Statistika")
def stats(message):
    if message.from_user.id != ADMIN_ID:
        return

    cursor.execute("SELECT COUNT(*) FROM videos")
    count = cursor.fetchone()[0]

    bot.send_message(
        message.chat.id,
        f"📊 Statistika:\n\n🎥 Videolar soni: {count}"
    )

# ================== ORQAGA ==================
@bot.message_handler(func=lambda m: m.text == "⬅️ Orqaga")
def back(message):
    bot.send_message(
        message.chat.id,
        "Asosiy menyu 👇",
        reply_markup=main_menu()
    )

# ================== OXIRI ==================
print(">>> Bot ishga tushdi")
bot.infinity_polling()
